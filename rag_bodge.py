from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import dotenv
import os
import requests
import bs4

dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=api_key)

url = input("Enter the URL of the article you want to summarize: ")

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text, 'html.parser')

article = soup.get_text()


prompt_template = f"""You are an expert on the following article. Answer the following question based on only the context provided and in unser 3 sentences:
                    <context>
                    {article}
                    </context>
                    """

prompt = ChatPromptTemplate.from_template(prompt_template + "Question: {input} ")

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

while True:
    question = input("Enter the question you want to ask: ")
    if question == "exit":
        break
    print(chain.invoke({"input": question}))