# LangChain RAG Integration

This demonstrates how to set up and use Retrieval-Augmented Generation (RAG) with LangChain in a uAgent. Follow the instructions below to get started.

---

## Requirements

- **Python** (v3.10+ recommended)
- **Poetry** (Python dependency management tool)

---

## Setup

1. **Obtain API Keys**:  
   - Visit [Cohere](https://dashboard.cohere.com/) and [OpenAI](https://openai.com/).  
   - Sign up or log in.  
   - Copy your API keys from their respective dashboards.

2. **Create a `.env` File**:  
   In the `langchain-rag/src` directory, create a `.env` file and add the following:

   ```bash
   export COHERE_API_KEY="your-cohere-api-key"
   export OPENAI_API_KEY="your-openai-api-key"
   export LANGCHAIN_RAG_SEED="your-random-seed"

3. In the `langchain-rag-agent` directory install all dependencies

    ```bash
    poetry install
    ```

3. To load the environment variables from `.env:

    ```bash
    cd src
    source .env
    ```

## Running The Main Script

To run the project, use the command:

```
poetry run python main.py

```