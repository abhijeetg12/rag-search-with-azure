
# RAG Search with Azure AI

This project implements a Retrieval-Augmented Generation (RAG) search system using Azure AI services and Streamlit. It creates a chatbot interface that allows users to ask questions and receive answers based on a knowledge base stored in Azure Cognitive Search.

## Features

- Persona-based responses
- Azure Cognitive Search integration
- Conversation history
- Streamlit-based user interface

## Prerequisites

- Python 3.7+
- Azure account with access to Azure Cognitive Search
- OpenAI API key (for GPT model access)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/rag-search-azure-ai.git
   cd rag-search-azure-ai
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Azure Cognitive Search service and index.

4. Create a `secrets.toml` file in the `.streamlit` directory with the following content:
   ```toml
   [default]
   searchservice = "your-search-service-name"
   searchkey = "your-search-service-admin-api-key"
   index = "your-index-name"
   tlm_manager = "TLM Manager persona description"
   psd_manager = "PSD Manager persona description"
   ```

## Usage

Run the Streamlit app:

```
streamlit run app.py
```

Navigate to the provided URL in your web browser to interact with the chatbot.

## Project Structure

- `app.py`: Main Streamlit application
- `gpt_return_st.py`: Contains functions for creating prompts and generating answers (not provided in the given code snippet)
- `.streamlit/secrets.toml`: Configuration file for API keys and other secrets

## How it Works

1. The user selects a persona from the dropdown menu.
2. The user enters a question in the text input field.
3. The system queries Azure Cognitive Search to retrieve relevant documents.
4. The retrieved content is used to create a prompt for the GPT model.
5. The GPT model generates an answer based on the prompt and selected persona.
6. The answer is displayed to the user, along with references to the source documents.
7. The conversation history is updated and displayed in the sidebar.

## Customization

- To add new personas, update the `PERSONAS` dictionary in `app.py`.
- To modify the search behavior, adjust the parameters in the `search_client.search()` call.
- To change the UI layout or styling, modify the Streamlit components and custom CSS in `app.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.