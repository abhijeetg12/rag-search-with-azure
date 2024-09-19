import os
import time
import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from gpt_return import *
from PIL import Image


# Persona definitions
PERSONAS = {
    "Well Engineer": st.secrets["well_engineer"],
    "PSD Manager": st.secrets["psd_manager"]
    }
# Initialize chat history storage in session state if not already present
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Streamlit App Header
st.set_page_config(page_title=" My AskAI Query Chatbot", layout="wide")
st.title("How may I help you today? ")


# Add logo at the top-left corner
logo_path = "logo.png"  # Local path to your logo

# Load and display the logo
logo_image = Image.open(logo_path)

# Streamlit will automatically resize the image when using st.image's width parameter
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        padding-top: 1px;
    }}
    [data-testid="stHeader"] {{
        display: none;
    }}
    .logo {{
        position: absolute;
        top: 10px;
        right: 0px;
        z-index: 100;
    }}
    </style>
    """, unsafe_allow_html=True
)

# Shrink the image by setting the width (adjust for 10x smaller based on original size)
st.image(logo_image, width=100)
# Persona selection dropdown
persona_selected = st.selectbox("Select a Persona:", options=list(PERSONAS.keys()))

# Sidebar for Chat History
with st.sidebar:
    st.markdown("## Chat History 🗂️")
    for i, (question, answer) in enumerate(st.session_state.conversation_history):
        st.markdown(f"**Q{i+1}:** {question}")
        st.markdown(f"**A{i+1}:** {answer}")
        st.markdown("---")

# User input field
st.markdown("### 🤖 Ask your Question:")
user_input = st.text_input('Enter your question here:', 'What are Sustainability initiatives take by SLB?')

if st.button('Submit') and user_input:

    # Azure Search Configuration
    service_name = st.secrets["searchservice"]
    # key = "YOUR-SEARCH-SERVICE-ADMIN-API-KEY"
    key = st.secrets["searchkey"]
    searchservice = st.secrets["searchservice"]
    endpoint = "https://{}.search.windows.net/".format(searchservice)
    index_name = st.secrets["index"]
    azure_credential = AzureKeyCredential(key)

   # Initialize Search Client
    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=azure_credential)

    KB_FIELDS_CONTENT = os.environ.get("KB_FIELDS_CONTENT") or "content"
    KB_FIELDS_CATEGORY = os.environ.get("KB_FIELDS_CATEGORY") or "SEARCH"
    KB_FIELDS_SOURCEPAGE = os.environ.get("KB_FIELDS_SOURCEPAGE") or "sourcepage"

    exclude_category = None
    filter = f"category ne '{exclude_category.replace("'", "''")}'" if exclude_category else None

    # Perform Search
    results = search_client.search(user_input,
                                   filter=filter,
                                   query_type=QueryType.SEMANTIC,
                                   query_language="en-us",
                                   query_speller="lexicon",
                                   semantic_configuration_name="content-search",
                                   top=3)

    # Extract and display references
    references = []
    content = ""
    for doc in results:
        content += doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") + "\n"
        references.append(doc[KB_FIELDS_SOURCEPAGE])

    st.markdown("### 📑 References:")
    st.write(" , ".join(set(references)))

    # Persona Context
    persona_description = PERSONAS[persona_selected]

    # Add persona context and past conversation to the conversation history
    conversation = [
        {"role": "system", "content": persona_description},
        {"role": "system", "content": "Answer to the user's queries"}
    ]

    # Append previous conversation history if available
    for question, answer in st.session_state.conversation_history:
        conversation.append({"role": "user", "content": question})
        conversation.append({"role": "assistant", "content": answer})

    # Add the current user input as part of the ongoing conversation
    prompt = create_prompt(content, user_input)
    conversation.append({"role": "user", "content": user_input})

    # Query the LLM with the extended conversation history
    reply = generate_answer(conversation)
    answer = reply.choices[0].message.content

    # Display the answer
    # st.markdown(f"### 💡 Answer from **{persona_selected}**:")
    st.write(answer)

    # Store the current question and answer in session history
    st.session_state.conversation_history.append((user_input, answer))

    # Add a time delay for better UI experience
    time.sleep(1)

# Footer with styling
st.markdown("""
    <style>
        .css-1aumxhk {background-color: #f5f5f5;}
        .stTextInput {border-radius: 10px;}
        .stButton > button {border-radius: 10px; background-color: #4CAF50; color: white;}
        .stMarkdown h2 {color: #4CAF50;}
        .stMarkdown {font-size: 1.1rem;}
    </style>
""", unsafe_allow_html=True)
