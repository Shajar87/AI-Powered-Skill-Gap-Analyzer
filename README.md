# AI-Powered Skill Gap Analyzer
Project Overview

This project is a Retrieval Augmented Generation (RAG) based system designed to analyze resumes against job descriptions. It effectively identifies technical skills and tools mentioned in the job description that are missing from the resume. Additionally, it provides valuable resources like YouTube tutorials and courses to help users bridge these skill gaps.

## Key Features

- Skill Comparison: Compares resume skills against job description requirements.
- Missing Skill Identification: Accurately pinpoints technical skills and tools that are absent from the resume.
- Resource Recommendations: Offers relevant YouTube tutorials and online courses to assist users in acquiring missing and non-missing skills.


## **How AI-Powered Skill Gap Analyzer Works**

#### 1. Upload Resume and Job Description:
- The user uploads a PDF resume and enters the job description in the text area provided.
#### 2. Preprocess Resume (if upload successful):
- The resume text is extracted using the "PyPDFLoader".
-	The extracted text is split into smaller chunks using a "CharacterTextSplitter" for better processing.
#### 3. Generate Embeddings (if processing successful):
- A "GoogleGenerativeAIEmbeddings" model converts the extracted resume text chunks into numerical representations (embeddings) and stored in a FAISS vector store. 
#### 4. Define Prompt Template:
- The Prompt Template is created. 
#### 5. Generate Skills Gap Analysis Response:
-The prompt template is filled with the user-provided job description and the preprocessed resume text.
A RetrievalQA chain is used: 
-	The retriever searches the vector store (created in step 3) for relevant information based on the job description.
-	The LLM (ChatGoogleGenerativeAI) processes the retrieved resume information (embeddings) and job description to identify skills from JD and the retrieved resume.
#### 6. Display Results:
-	The LLM response is displayed, providing skills gap analysis.
#### 7. Suggest YouTube Tutorials (for missing skills):
-	A function get_youtube_videos fetches relevant YouTube tutorials for each missing skill using the YouTube API.


![Image Description](https://github.com/Shajar87/Resume-Analyzer-/blob/main/Skill%20Gap%20Analyzer%20Flow.png)
