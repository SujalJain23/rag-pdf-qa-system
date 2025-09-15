#  step -1) jd generate karega ye code 

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load model & tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 2. Build pipeline
hf_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=256
)

# 3. Wrap into LangChain
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# 4. Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Create a professional job description for {role} with skills: {skills}. Include responsibilities, requirements, and benefits."),
])

# 5. Chain
chain = prompt | llm | StrOutputParser()

# 6. ✅ YE PART ADD KARNA HAI
print("................................................................Step-1.........................................................")
print("Generating JD...")
jd = chain.invoke({
    "role": "Backend Developer",
    "skills": "Node.js, Express.js, MongoDB, AWS"
})
print("✅ Done!\n")
print(jd)

# step - 2) ye jd ko post karega linkedin pai through api

print("................................................................Step-2.........................................................")

def post_job_to_portal(jd_title, jd_description, portal="indeed"):
    """
    Mock function for testing - actual API ke jagah use karo
    """
    print(f"✅ Mock: Job posted to {portal}!")
    print(f"Title: {jd_title}")
    print(f"Description: {jd_description[:1000]}...")
    return {"status": "success", "job_id": "test_123"}

# Use karo
result = post_job_to_portal("Backend Developer", "JD:We are seeking a Backend Developer skilled in Node.js, Express.js, MongoDB, and REST APIs. Responsibilities include building scalable server-side applications, integrating databases, ensuring security, and collaborating with frontend teams to deliver efficient, reliable, and high-performance systems.")
print(result)

#step-3 

import os
import PyPDF2

# 1. JD REQUIREMENTS (Yahi change karna hai)
JD_SKILLS = ["Python", "Node.js", "MongoDB", "AWS", "Express.js"]

# 2. RESUMES FOLDER (Yahi change karna hai) 
RESUMES_FOLDER = "C:/Users/Admin/Desktop/resume/Sujal_jainn_cv.pdf"

def read_resume(file_path):
    """Resume se text nikalta hai"""
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text.lower()
        return ""
    except:
        return ""

print("🤖 Automated Resume Shortlister Started!")
print("🔍 Checking resumes...")

# Sab resumes check karo
shortlisted = []
for filename in os.listdir(RESUMES_FOLDER):
    if filename.endswith('.pdf'):
        resume_path = os.path.join(RESUMES_FOLDER, filename)
        resume_text = read_resume(resume_path)
        
        if resume_text:
            # Score calculate karo
            score = 0
            for skill in JD_SKILLS:
                if skill.lower() in resume_text:
                    score += 1
            
            # Shortlist karo
            if score >= 2:
                shortlisted.append({
                    'name': filename.replace('.pdf', ''),
                    'score': score,
                    'file': filename
                })

# Results dikhao
print(f"\n✅ **RESULTS:** {len(shortlisted)} candidates shortlisted!")
print("=" * 50)

for candidate in shortlisted:
    print(f"🎯 {candidate['name']}")
    print(f"   ⭐ Score: {candidate['score']}/{len(JD_SKILLS)}")
    print(f"   📁 File: {candidate['file']}")
    print("-" * 40)

print("\n🚀 Shortlisting complete!")