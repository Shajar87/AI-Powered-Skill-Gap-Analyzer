# Resume-Analyzer-
Project Overview

This project is a Retrieval Augmented Generation (RAG) based system designed to analyze resumes against job descriptions. It effectively identifies technical skills and tools mentioned in the job description that are missing from the resume. Additionally, it provides valuable resources like YouTube tutorials and courses to help users bridge these skill gaps.

## Key Features

- Skill Comparison: Compares resume skills against job description requirements.
- Missing Skill Identification: Accurately pinpoints technical skills and tools that are absent from the resume.
- Resource Recommendations: Offers relevant YouTube tutorials and online courses to assist users in acquiring missing skills.


## How Resume Analyzer Works
This Streamlit application analyzes a resume and job description to identify missing skills. Here's a step-by-step breakdown:

1. Upload Resume and Job Description:

The user uploads a PDF resume and enters the job description in the text area provided.

2. Preprocess Resume (if upload successful):
A temporary file is created to store the uploaded PDF.
The resume text is extracted using the "PyPDFLoader".
The extracted text is split into smaller chunks using a "CharacterTextSplitter" for better processing.

3. Generate Embeddings of the chunks:
A "GoogleGenerativeAIEmbeddings" model converts the extracted resume text chunks into numerical representations (embeddings) and stored in a FAISS vector store. This acts as a database that stores the generated resume embeddings for fast retrieval.

4. Generate Missing Skills Response:
The prompt template is filled with the user-provided job description and the preprocessed resume text.
A RetrievalQA chain is used:
The retriever searches the vector store for relevant information based on the job description.
The LLM (ChatGoogleGenerativeAI) processes the retrieved resume information (embeddings) and job description to identify missing skills.
The LLM's response is formatted according to the prompt template, resulting in a list of skills with their presence/absence in the resume.

5. Display Results:
The raw LLM response is displayed, providing an overall view (optional, commented out in the code).   
The response is parsed to extract only the skills listed as "missing" in the resume.
Finally, the missing skills list or a message indicating no missing skills is presented to the user.

6. Suggest YouTube Tutorials (for missing skills):
A function get_youtube_videos fetches relevant YouTube tutorials for each missing skill using the YouTube API.
If tutorials are found, they are displayed as hyperlinks under the corresponding skill.
If no tutorials are found, a message is displayed for that specific skill.
