// // frontend/src/app/page.tsx (বা আপনার ড্যাশবোর্ড ফাইল)
// "use client";

// import React, { useState } from 'react';
// import ReactMarkdown from 'react-markdown'; // মার্কডাউন সুন্দর করে দেখানোর জন্য

// export default function Home() {
//   const [file, setFile] = useState<File | null>(null);
//   const [analysis, setAnalysis] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleUpload = async () => {
//     if (!file) return alert("Please select a file first!");

//     setLoading(true);
//     const formData = new FormData();
//     formData.append("file", file);

//     try {
//       // আপনার ব্যাকএন্ড ইউআরএল (লোকালহোস্ট ৮০০০)
//       const res = await fetch("http://127.0.0.1:8000/api/v1/properties/analyze-lease", {
//         method: "POST",
//         body: formData,
//       });

//       const data = await res.json();
//       setAnalysis(data.analysis); // জেমিনির পাঠানো রিপোর্ট সেট করা
//     } catch (error) {
//       console.error("Error uploading file:", error);
//       alert("Something went wrong!");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <main className="p-10 bg-gray-50 min-h-screen">
//       <div className="max-w-4xl mx-auto bg-white p-8 rounded-2xl shadow-lg">
//         <h1 className="text-2xl font-bold text-blue-700 mb-4">NeuralLease AI Analyzer</h1>
        
//         {/* Input Section */}
//         <div className="flex gap-4 mb-8">
//           <input 
//             type="file" 
//             onChange={(e) => setFile(e.target.files?.[0] || null)}
//             className="border p-2 rounded w-full"
//           />
//           <button 
//             onClick={handleUpload}
//             disabled={loading}
//             className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
//           >
//             {loading ? "Analyzing..." : "Analyze PDF"}
//           </button>
//         </div>

//         {/* Results Section */}
//         {analysis && (
//           <div className="prose max-w-none border-t pt-6">
//             <h2 className="text-xl font-semibold mb-4 text-green-600">AI Detailed Report:</h2>
//             <ReactMarkdown className="leading-relaxed text-gray-800">
//               {analysis}
//             </ReactMarkdown>
//           </div>
//         )}
//       </div>
//     </main>
//   );
// }

// "use client";
// import React, { useState } from 'react';
// import ReactMarkdown from 'react-markdown';

// export default function LeaseAnalyzer() {
//   const [file, setFile] = useState<File | null>(null);
//   const [analysis, setAnalysis] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleAnalyze = async () => {
//     if (!file) return;
//     setLoading(true);
//     const formData = new FormData();
//     formData.append("file", file);

//     try {
//       const res = await fetch("http://127.0.0.1:8000/api/v1/properties/analyze-lease", {
//         method: "POST",
//         body: formData,
//       });
//       const data = await res.json();
//       setAnalysis(data.analysis);
//     } catch (err) {
//       alert("Backend start kora ache to, Sonu bhai?");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-slate-50 py-12 px-4">
//       <div className="max-w-3xl mx-auto bg-white shadow-2xl rounded-3xl overflow-hidden border border-slate-200">
//         <div className="bg-blue-700 p-8 text-white text-center">
//           <h1 className="text-3xl font-extrabold tracking-tight">NeuralLease AI</h1>
//           <p className="mt-2 text-blue-100 opacity-90">Instant Property Document Insights</p>
//         </div>

//         <div className="p-8">
//           <div className="flex flex-col items-center justify-center border-4 border-dashed border-slate-200 rounded-2xl p-10 hover:border-blue-400 transition-colors">
//             <input 
//               type="file" 
//               accept=".pdf"
//               onChange={(e) => setFile(e.target.files?.[0] || null)}
//               className="mb-4 text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
//             />
//             <button 
//               onClick={handleAnalyze}
//               disabled={loading || !file}
//               className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition-all transform active:scale-95 disabled:bg-slate-300"
//             >
//               {loading ? "🤖 AI is Thinking..." : "Analyze Document"}
//             </button>
//           </div>

//           {analysis && (
//             <div className="mt-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
//               <div className="flex items-center gap-2 mb-4">
//                 <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
//                 <h2 className="text-xl font-bold text-slate-800 uppercase tracking-wider">Analysis Report</h2>
//               </div>
//               <div className="bg-slate-50 p-8 rounded-2xl border border-slate-100 prose prose-blue max-w-none text-slate-700 shadow-inner">
//                 <ReactMarkdown>{analysis}</ReactMarkdown>
//               </div>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }
"use client";
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function LeaseAnalyzer() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);

  // সনু ভাই, এখানে আমরা ডাইনামিক ইউআরএল ব্যবহার করছি
  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // লোকালহোস্ট এর বদলে ${API_URL} ব্যবহার করছি
      const res = await fetch(`${API_URL}/api/v1/properties/analyze-lease`, {
        method: "POST",
        body: formData,
      });
      
      if (!res.ok) throw new Error("Backend response error");
      
      const data = await res.json();
      setAnalysis(data.analysis);
    } catch (err) {
      alert("সনু ভাই, ব্যাকএন্ড কি সচল আছে? এপিআই ইউআরএল টা চেক করুন।");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4">
      <div className="max-w-3xl mx-auto bg-white shadow-2xl rounded-3xl overflow-hidden border border-slate-200">
        <div className="bg-blue-700 p-8 text-white text-center">
          <h1 className="text-3xl font-extrabold tracking-tight">NeuralLease AI</h1>
          <p className="mt-2 text-blue-100 opacity-90">Instant Property Document Insights</p>
        </div>

        <div className="p-8">
          <div className="flex flex-col items-center justify-center border-4 border-dashed border-slate-200 rounded-2xl p-10 hover:border-blue-400 transition-colors">
            <input 
              type="file" 
              accept=".pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="mb-4 text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
            />
            <button 
              onClick={handleAnalyze}
              disabled={loading || !file}
              className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition-all transform active:scale-95 disabled:bg-slate-300"
            >
              {loading ? "🤖 AI is Thinking..." : "Analyze Document"}
            </button>
          </div>

          {analysis && (
            <div className="mt-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
              <div className="flex items-center gap-2 mb-4">
                <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
                <h2 className="text-xl font-bold text-slate-800 uppercase tracking-wider">Analysis Report</h2>
              </div>
              <div className="bg-slate-50 p-8 rounded-2xl border border-slate-100 prose prose-blue max-w-none text-slate-700 shadow-inner">
                <ReactMarkdown>{analysis}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}