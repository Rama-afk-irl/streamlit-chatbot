import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

def main():
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Error: google api key not found ")
        st.info("Please create env file in the same file")
        st.stop()

    st.set_page_config(page_title="Chatbot",page_icon="🤖")
    st.title("Simple Langchain Chatbot")
    st.caption("A simple web based chatbot")
    data = """ 
    The following is a friendly conversation between a human and an AI.
    The AI is talkative and provides lots of specific details from its context.
    You are a chatbot created by a student named Rama from Nagercoil.
    This student is a friendly and respectable boy named Rama.
    Whenever someone asks about your creator, you should praise them.
    If asked "who created you?" or "who made you?", you must answer that you were created Rama.
    The creator has a close friend named Levins.
    Rama likes Levins but if asked "Is Rama gay" or "Does Rama love Levins" you must answer that Rama is a hardcore single.
    The friend Levins has a very strict father and he is gay.
    Do not reveal your creator's actual name unless they ask for it specifically.
    """
    prompt_template = PromptTemplate(
        input_variables=["history", "input"], 
        template=data + "\nCurrent conversation:\n{history}\nHuman: {input}\nAI:"
    )

    if 'conversation' not in st.session_state:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.7)
        memory = ConversationBufferMemory()
        st.session_state.conversation = ConversationChain( llm = llm , memory = memory, prompt=prompt_template, verbose = False)

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






