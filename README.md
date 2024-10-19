# AI-Powered Skill Gap Analyzer
Project Overview

This project is a Retrieval Augmented Generation (RAG) based system designed to analyze resumes against job descriptions. It effectively identifies technical skills and tools mentioned in the job description that are missing from the resume. Additionally, it provides valuable resources like YouTube tutorials and courses to help users bridge these skill gaps.

## Key Features

- Skill Comparison: Compares resume skills against job description requirements.
- Missing Skill Identification: Accurately pinpoints technical skills and tools that are absent from the resume.
- Resource Recommendations: Offers relevant YouTube tutorials or courses to assist users in acquiring missing skills.

## Curious to try it? Click the link: https://huggingface.co/spaces/Mohd0509/Resume-JD-Analyzer

## How AI-Powered Skill Gap Analyzer Works

![Image Description](https://github.com/Shajar87/Resume-Analyzer-/blob/main/rag_flowchart.png)
--- 
#### 1. Upload Resume and Job Description:
- The user uploads a PDF resume and enters the job description in the text area provided.
#### 2. Preprocess Resume (if upload successful):
-	The uploaded resume is split into smaller chunks using a "CharacterTextSplitter" for better processing.
#### 3. Generate Embeddings (if processing successful):
- A "GoogleGenerativeAIEmbeddings" model converts the resume chunks into numerical representations (embeddings) and stored in a FAISS vector store. 
#### 4. Define Prompt Template:
- The Prompt Template is created prompt with context set as user-provided job description. 
#### 5. Generate Skills Gap Analysis Response:
A RetrievalQA chain is used: 
-	The retriever searches the vector store (created in step 3) for relevant information based on the job description.
-	The LLM (ChatGoogleGenerativeAI) processes the retrieved resume information (embeddings) and job description to identify skills from JD and the retrieved resume.
#### 6. Display Results:
-	The LLM response is displayed, providing skills gap analysis.
#### 7. Suggest YouTube Tutorials (for missing skills):
-	A function get_youtube_videos fetches relevant YouTube tutorials for each missing skill using the YouTube API.

