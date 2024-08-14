from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=api_key)

loader = PyPDFDirectoryLoader("Journals")
docs = loader.load()

embeddings = OpenAIEmbeddings(api_key=api_key)

text_splitter = RecursiveCharacterTextSplitter()

documents = text_splitter.split_documents(docs)

vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)


response = retrieval_chain.invoke({"input": "Summarise malaria?"})

print(response["answer"])


