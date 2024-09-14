# OpenAI.api_key = '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'

# def create_prompt(context,query):
#     header = "You are a helpful chatbot who is trying to answer the following query for an employee"
#     return header + context + "\n\n" + query + "\n"
import dotenv
import os
from openai import OpenAI 

dotenv.load_dotenv()
client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
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
