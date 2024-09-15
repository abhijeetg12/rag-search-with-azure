# def create_prompt(context,query):
#     header = "You are a helpful chatbot who is trying to answer the following query for an employee"
#     return header + context + "\n\n" + query + "\n"
from openai import OpenAI 
import streamlit as st

client = OpenAI(
    api_key = st.secrets["OPENAI_API_KEY"]
)
def create_prompt(context,query):
    header = "Be a helpful company internal chatbot"
    return header + context + "\n\n" + query + "\n"


def generate_answer(conversation):
    print (conversation)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation
        )
        return completion #['choices'][0]['message']['content']
    except Exception as e:
        return f"Error occurred: {str(e)}"
