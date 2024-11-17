import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def load_document(file):
    import os 
    name, extension = os.path.splitext(file)

    if extension == '.pdf':
        from langchain_community.document_loaders import PyMuPDFLoader
        print(f"Loading {file}")
        loader = PyMuPDFLoader(file)
    elif extension == '.docx':
        from langchain_community.document_loaders import Docx2txtLoader
        print(f"Loading {file}")
        loader = Docx2txtLoader(file)
    else:
        print("Document format is not supported")
        return None

        
    data = loader.load()
    return data


def chunk_data(data, ChunkSize = 256):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = ChunkSize, chunk_overlap = 0)
    chunks = text_splitter.split_documents(data)
    return chunks


def Create_Embedding_VectorDB(chunks):
    from langchain_huggingface.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS

    model = "sentence-transformers/all-mpnet-base-v2"
    Embedding = HuggingFaceEmbeddings(model_name=model, model_kwargs={})
    vector_store = FAISS.from_documents(documents = chunks, embedding = Embedding)

    return vector_store
    

def ask_and_get_answer(vector_store, question, k = 3):
    from langchain.chains import RetrievalQA
    from langchain_google_genai import GoogleGenerativeAI

    GOOGLE_API_KEY = "AIzaSyAAOvSrnt3nb6Cqf81ipDAgKInVG9tm62w"

    # Initialize the LLM model from Google Generative AI
    llm = GoogleGenerativeAI(model='gemini-pro', google_api_key=GOOGLE_API_KEY, temperature = 0.7)

    # Set up retriever from the vector store
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs = {'k' : k})

    # Create the RetrievalQA chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever  # Correctly passed retriever
    )

    # Run the chain to get the answer
    answer = chain.invoke(question)
    return answer["result"]
