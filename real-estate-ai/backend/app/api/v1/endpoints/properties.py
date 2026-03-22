# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/")
# async def get_properties():
#     return {"message": "Property list endpoint"}
import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.services.document_processing.pdf_parser import PDFProcessor
from app.services.agents.lease_agent import LeaseAgent
from app.db.session import get_db
from app.services.data_ops import DataOperations

router = APIRouter()
lease_agent = LeaseAgent()

@router.post("/analyze-lease")
async def analyze_lease_document(
    file: UploadFile = File(...), 
    db = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # ১. ফাইলটি সাময়িকভাবে সেভ করা
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ২. পিডিএফ থেকে টেক্সট বের করা
        extracted_text = await PDFProcessor.extract_text_from_pdf(file_path)

        # ৩. জেমিনি এআই দিয়ে এনালাইসিস করা
        analysis_result = await lease_agent.analyze_lease_text(extracted_text)

        # ৪. ডাটাবেসে এনালাইসিস রিপোর্ট সেভ করা
        ops = DataOperations(db)
        property_data = {
            "filename": file.filename,
            "analysis_report": analysis_result,
            "status": "analyzed"
        }
        property_id = await ops.save_property(property_data)

        return {
            "property_id": property_id,
            "filename": file.filename,
            "analysis": analysis_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # ৫. প্রসেসিং শেষে টেম্পোরারি ফাইলটি মুছে ফেলা
        if os.path.exists(file_path):
            os.remove(file_path)