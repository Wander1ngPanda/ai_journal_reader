import time
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

st.title("Translation Bot")

llm = ChatOllama(model="llama3");

chat_template = """
    You are an assistant that translates messages from {language}) to {target_language}. 
    Output messages should only be in the format:
    {output_format}
    Example:
    {example}
    Note:
    If the user input is a question, the output should be a question. Do not answer it!
    """
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
        ("system", chat_template),
        ("user", human_template)
    ])

chat_prompt = chat_prompt.partial(language="English", output_format="""
                                      target_language_here : translated_text_here
                                      """,
                                      example="Japanese: こんにちは")

output_parser = StrOutputParser()

def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "processing" not in st.session_state:
    st.session_state.processing = True

def disable_chat():
    st.session_state.disabled = True
    st.session_state.processing = False

def enable_chat():
    st.session_state.disabled = False

with st.sidebar:
    language = st.selectbox("Select the target language", ("Japanese", "Filipino","Spanish", "French", "German", "Italian", "Korean", "Chinese", "Russian", "Arabic", "Portuguese", "Dutch", "Turkish", "Polish", "Swedish", "Czech", "Danish", "Finnish", "Greek", "Hebrew", "Hindi", "Hungarian", "Indonesian", "Norwegian", "Romanian", "Slovak", "Thai", "Ukrainian", "Vietnamese"), index=None, placeholder="Select Language") or "English"


if prompt := st.chat_input("Enter a message to translate:", disabled=st.session_state.disabled):
    disable_chat()
    with st.spinner("Translating..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            chain = chat_prompt | llm | output_parser
            stream = chain.invoke({"target_language": language, "text": prompt})
            response = st.write_stream(response_generator(stream))     
        st.session_state.messages.append({"role": "assistant", "content": response})
    enable_chat()