import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def main():
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Error: google api key not found ")
        st.info("Please create env file in the same file")
        st.stop()

    st.set_page_config(page_title="Chatbot",page_icon="🤖")
    st.title("Simple Langchain Chatbot")
    st.caption("A simple web based chatbot")

    if 'conversation' not in st.session_state:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.7)
        memory = ConversationBufferMemory()
        st.session_state.conversation = ConversationChain( llm = llm , memory = memory, verbose = False)

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to ask?"):
        st.session_state.messages.append({"role": "user","content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("Thinking...."):
            response = st.session_state.conversation.predict(input=prompt)
        st.session_state.messages.append({"role":"assistant", "content":response})
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main() 