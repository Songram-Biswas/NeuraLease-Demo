# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/")
# async def get_properties():
#     return {"message": "Property list endpoint"}
# import os
# import shutil
# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
# from app.services.document_processing.pdf_parser import PDFProcessor
# from app.services.agents.lease_agent import LeaseAgent
# from app.db.session import get_db
# from app.services.data_ops import DataOperations

# router = APIRouter()
# lease_agent = LeaseAgent()

# @router.post("/analyze-lease")
# async def analyze_lease_document(
#     file: UploadFile = File(...), 
#     db = Depends(get_db)
# ):
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only PDF files are supported")

#     # ১. ফাইলটি সাময়িকভাবে সেভ করা
#     temp_dir = "temp_uploads"
#     os.makedirs(temp_dir, exist_ok=True)
#     file_path = os.path.join(temp_dir, file.filename)

#     try:
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # ২. পিডিএফ থেকে টেক্সট বের করা
#         extracted_text = await PDFProcessor.extract_text_from_pdf(file_path)

#         # ৩. জেমিনি এআই দিয়ে এনালাইসিস করা
#         analysis_result = await lease_agent.analyze_lease_text(extracted_text)

#         # ৪. ডাটাবেসে এনালাইসিস রিপোর্ট সেভ করা
#         ops = DataOperations(db)
#         property_data = {
#             "filename": file.filename,
#             "analysis_report": analysis_result,
#             "status": "analyzed"
#         }
#         property_id = await ops.save_property(property_data)

#         return {
#             "property_id": property_id,
#             "filename": file.filename,
#             "analysis": analysis_result
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
#     finally:
#         # ৫. প্রসেসিং শেষে টেম্পোরারি ফাইলটি মুছে ফেলা
#         if os.path.exists(file_path):
#             os.remove(file_path)
import os
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.document_processing.pdf_parser import PDFProcessor
from app.services.vector_db import VectorManager
from app.services.agents.graph import app_graph 
from app.services.data_ops import DataOperations
from app.db.session import get_db 

router = APIRouter()
pdf_processor = PDFProcessor()
vector_db = VectorManager()

@router.post("/analyze-lease")
async def analyze_lease(file: UploadFile = File(...), db = Depends(get_db)):
    print(f"\n🚀 Process is starting for: {file.filename}")
    # ১. ফাইলটি সাময়িকভাবে সেভ করা (পাথ পাওয়ার জন্য)
    # UploadFile অবজেক্ট থেকে সরাসরি পাথ পাওয়া যায় না, তাই এটি প্রয়োজন
    temp_file_path = f"temp_{file.filename}"
    try:
        import asyncio
        print("📁 Saving uploaded file temporarily...")
        content = await file.read()
        with open(temp_file_path, "wb") as buffer:
            buffer.write(content)

        # ২. পিডিএফ থেকে টেক্সট বের করা
        # নিশ্চিত করুন pdf_parser.py-তে extract_text_from_pdf মেথডটি আছে
        print("📄 Extracting text from PDF...")
        text = await pdf_processor.extract_text_from_pdf(temp_file_path) 
        if not text:
            raise HTTPException(status_code=400, detail="Could not read PDF text or PDF is empty")

        # ৩. RAG এর জন্য টেক্সট চাঙ্কিং ও ভেক্টর ডিবিতে সেভ করা
        # এটি এআই-কে নির্দিষ্ট সেকশন খুঁজে পেতে সাহায্য করে
        print("🧠 Creating text chunks for RAG...")
        chunks = pdf_processor.create_chunks(text)
        vector_db.add_document(chunks, doc_id=file.filename)
        print(f"✅ Text chunks created and added to vector DB for document: {file.filename}")
        print(f"📊 Total chunks created: {len(chunks)}")
        # ৪. LangGraph এজেন্ট রান করা (এজেন্টিক ওয়ার্কফ্লো)
        initial_state = {
            "raw_text": text, 
            "retrieved_context": [], 
            "analysis": "", 
            "risk_score": 0
        }
        
        # টাইমআউট এড়াতে ২ মিনিট সময় বরাদ্দ করা হয়েছে
        try:
             final_state = await asyncio.wait_for(app_graph.ainvoke(initial_state), timeout=120.0)
             print("✅ AI analysis completed successfully.")
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="AI Analysis took too long. Please try again.")

        # ৫. ডাটাবেসে সেভ করা (MongoDB)
        print("💾 Saving analysis report to MongoDB...")
        data_ops = DataOperations(db) 
        property_data = {
            "filename": file.filename,
            "analysis_report": final_state.get("analysis", "No analysis generated"),
            "status": "analyzed_with_rag"
        }
        
#         property_data = {
#     "filename": file.filename,
#     "analysis_report": "API Limit Exceeded - Showing Mock Data for Testing",
#     "status": "mock_mode"
# }
        
        # মঙ্গোডিবিতে সেভ করে আইডি রিটার্ন করা
        property_id = await data_ops.save_property(property_data) 
        print(f"✅ Analysis report saved to MongoDB with ID: {property_id}")    

        return {
            "id": property_id,
            "filename": file.filename,
            "status": "success",
            "analysis": final_state["analysis"]
        }
        

    except Exception as e:
        # যেকোনো ইন্টারনাল এরর ডিটেইলসহ রিটার্ন করা
        print(f"Error in analyze_lease: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # ৬. কাজ শেষে বা এরর হলেও টেম্পোরারি ফাইলটি মুছে ফেলা (Cleanup)
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)