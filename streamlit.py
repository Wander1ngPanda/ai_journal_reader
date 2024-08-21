import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
import tempfile
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if 'llm' not in st.session_state:
    st.session_state['llm'] = ChatOpenAI(api_key=api_key)
if 'embeddings' not in st.session_state:
    st.session_state['embeddings'] = OpenAIEmbeddings(api_key=api_key)
if 'vector' not in st.session_state:
    st.session_state['vector'] = None



def generate_response(user_input):
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

    document_chain = create_stuff_documents_chain(st.session_state.llm, prompt)
    retriever = st.session_state.vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": user_input})
    st.info(response["answer"])


files = st.file_uploader(label='Upload a PDF', type='pdf', accept_multiple_files=True)

if files:
        temp_dir = tempfile.mkdtemp()
        for data in files:
            path = os.path.join(temp_dir, data.name)
            with open(path, "wb") as f:
                    f.write(data.getvalue())
        loader = PyPDFDirectoryLoader(temp_dir)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        st.session_state.vector = FAISS.from_documents(documents, st.session_state.embeddings)

        with st.form("my_form"):
            text = st.text_area("Enter text:")
            submitted = st.form_submit_button("Submit")
            if submitted:
                generate_response(text)




