import os
import kagglehub
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq

def download_kaggle_data():
    """Downloads dataset from KaggleHub."""
    path = kagglehub.dataset_download("kazanova/sentiment140")
    print("✅ Kaggle dataset downloaded:", path)
    return path

def initialize_llm():
    """Initializes the Groq LLM with API Key."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ ERROR: GROQ_API_KEY environment variable not set.")
    
    return ChatGroq(
        temperature=0,
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile"
    )

def create_vector_db():
    """Loads PDF documents, splits text, and stores embeddings in ChromaDB."""
    data_dir = "data/"
    os.makedirs(data_dir, exist_ok=True)

    # Load PDF documents
    loader = DirectoryLoader(data_dir, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()

    if not documents:
        print("⚠️ No PDFs found in 'data/' directory. ChromaDB will be empty.")
        return None  # Return None if no documents found

    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Create embeddings and store in ChromaDB
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')  
    vector_db = Chroma.from_documents(texts, embeddings, persist_directory='chroma_db')

    print("✅ ChromaDB created successfully.")
    return vector_db

def setup_qa_chain(vector_db, llm):
    """Creates a QA retrieval chain with a structured prompt."""
    retriever = vector_db.as_retriever()

    prompt_template = """You are a compassionate mental health chatbot.
    Provide thoughtful and supportive responses based on the following context:
    
    Context: {context}
    ---
    User: {question}
    Chatbot:"""

    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

def get_chatbot_response(user_input):
    """Retrieves chatbot response based on user input."""
    if not user_input or user_input.strip() == "":
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

    print(f"📝 Received User Input: {user_input}")

    llm = initialize_llm()
    db_path = "chroma_db"

    # Load existing DB or create a new one
    if os.path.exists(db_path):
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    else:
        vector_db = create_vector_db()
        if not vector_db:
            return "⚠️ No data found. Please upload PDF files to the 'data/' directory."

    qa_chain = setup_qa_chain(vector_db, llm)

    try:
        response = qa_chain.invoke({"query": user_input})
        print(f"📝 Raw Response from LLM: {response}")

        response_text = response.get('result', '')  # Ensure correct response key
        return response_text.strip() if response_text else "I couldn't find relevant information."
    except Exception as e:
        print(f"🔥 Error: {e}")
        return "I'm experiencing technical difficulties. Please try again later."
