import streamlit as st
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os
import dotenv
from googleapiclient.discovery import build  # For YouTube API
import tempfile
import re


# Load environment variables
dotenv.load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
youtube_api_key = os.getenv('YOUTUBE_API_KEY')  # Consistent naming

# Check if YouTube API key is loaded and initialize YouTube client
if not youtube_api_key:
    st.error("YouTube API key is missing. Please set it in the .env file.")
    st.stop()

try:
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
except Exception as e:
    st.error(f"Failed to initialize YouTube API client: {e}")
    st.stop()

# Streamlit app setup
st.title("Resume - Job Description Skills Analyzer")

# Ensure the GEMINI API key is present
if gemini_api_key is None:
    st.error("GEMINI_API_KEY not found in environment variables.")
    st.stop()

# Upload the resume PDF
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
missing_skills = []  # Initialize missing_skills outside the try block

if uploaded_file is not None:
    # Create a temporary file to save the uploaded PDF
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # Load the PDF from the temporary file
        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()

        # Extract text from the PDF and split into chunks
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=30)
        docs = text_splitter.split_documents(documents)
        texts = [doc.page_content for doc in documents]
        resume_text = "\n".join(texts)  # Combine the extracted resume text

        # Generate embeddings
        embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=gemini_api_key
        )

        # Create FAISS vector store
        db = FAISS.from_documents(docs, embedding_model)

        # Define prompt template for analyzing missing skills
        promptTemplate = """
        Your task is as a helpful assistant is to identify technical skills and tools mentioned in the following Job Description:
        {job_description_text}
        that are not present in the retrieved context from vector database:
        {resume_text}
        Please output the skills in a structured format.

        For example sql is mentioned in the resume but python and Power BI are not present, then your response should be as below:
        1. SQL: present in the resume  
        2. Python: missing from the resume
        3. Power BI: missing from the resume
        And don't try to explain the response. Only output the response in the specified format.

        """

        prompt = PromptTemplate(
            input_variables=["job_description", "resume_text"],
            template=promptTemplate
        )
        # Create retriever
        retriever = db.as_retriever()

        # Create QA chain with the LLM and retriever
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0,
                max_output_tokens=300,
                google_api_key=gemini_api_key
            ),
            retriever=retriever
        )

        # User input: job description
        job_description_text = st.text_area("Enter the job description:")
        if job_description_text:
            # Handle job description and generate missing skills response
            with st.spinner("Analyzing resume and job description..."):
                query_input = promptTemplate.format(job_description_text=job_description_text, resume_text=resume_text)
                result = qa_chain({"query": query_input})
            # Display the missing skills
            response = result.get("result", "No skills found.")
            st.subheader("Resume Skills Analysis Result Against The Job Description:")
            st.write(result["result"])  

            # # Debugging: Show the raw response
            # st.write("### Raw Response from the model")
            # st.write(response)

            # Parsing the response into missing skills
            lines = response.split("\n")
            for line in response.split('\n'):
                if re.search(r"missing", line):
                    match = re.search(r"^\d+\.\s(.*?):", line)
                    if match:
                        skill_name = match.group(1).strip()
                        missing_skills.append(skill_name)

            # Display the missing skills or a fallback message
            # st.subheader("Missing Skills from the Resume")
            # st.write([skill_name for skill_name in missing_skills] if missing_skills else "No missing skills found.")
    except Exception as e:
        st.error(f"Error processing the uploaded PDF: {e}")
        st.stop()

    # Function to get YouTube video suggestions for missing skills
    def get_youtube_videos(skill):
        try:
            request = youtube.search().list(
                q=skill + " tutorial",
                part="snippet",
                type="video",
                maxResults=1
            )
            response = request.execute()
            videos = []
            for item in response.get('items', []):
                video_id = item['id'].get('videoId')
                if video_id:
                    videos.append((item['snippet']['title'], f"https://www.youtube.com/watch?v={video_id}"))
            return videos
        except Exception as e:
            st.error(f"Error fetching YouTube videos: {e}")
            return []

    # Fetch and display YouTube tutorials for missing skills
    st.subheader("Suggested YouTube Tutorials for Missing Skills")
    for skill in missing_skills:
        st.write(f"**Skill:** {skill}")
        videos = get_youtube_videos(skill)
        if videos:
            for title, url in videos:
                st.markdown(f"[{title}]({url})")
        else:
            st.write(f"No YouTube videos found for {skill}.")
else:
    st.warning("Please upload a resume and enter a job description to get a response.")
