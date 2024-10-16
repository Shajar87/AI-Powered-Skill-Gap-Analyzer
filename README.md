# Resume-JD Analyzer
Project Overview

This project is a Retrieval Augmented Generation (RAG) based system designed to analyze resumes against job descriptions. It effectively identifies technical skills and tools mentioned in the job description that are missing from the resume. Additionally, it provides valuable resources like YouTube tutorials and courses to help users bridge these skill gaps.

## Key Features

- Skill Comparison: Compares resume skills against job description requirements.
- Missing Skill Identification: Accurately pinpoints technical skills and tools that are absent from the resume.
- Resource Recommendations: Offers relevant YouTube tutorials and online courses to assist users in acquiring missing skills.


## **How Resume Analyzer Works**

1. **Upload Resume and Job Description:** User uploads PDF resume and enters job description.
2. **Preprocess Resume:** Extract resume text, split into chunks.
3. **Generate Embeddings:** Convert resume text chunks into embeddings, store in FAISS vector store.
4. **Identify Missing Skills:** Use RetrievalQA chain to compare job description with resume embeddings, identify missing skills.
5. **Display Results:** Show missing skills list and suggest YouTube tutorials for those skills.
