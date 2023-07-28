# DocuBot

## Overview


This project is a web application built using Streamlit, Langchain, and Chroma to provide three key features:

1. **Chat:** Users can interact with the application and get information using Langchain's capabilities, such as serpapi, llm-math, and Wikipedia integration.

2. **Summarize Uploaded Documents:** Users can upload documents and choose between a synopsis or a detailed summary, generated using the map_reduce functionality.

3. **Answer Questions on Uploaded Documents:** Users can ask questions related to the uploaded documents, and the application will provide answers based on the embedded content stored in Chroma.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ananthmucharla/DocuBot.git
cd DocuBot
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app.py
```

## Features and Usage

### Chat

- Users can interact with the chatbot by typing in queries.
- Langchain's serpapi integration allows users to get real-time search results.
- The llm-math tool can assist with mathematical queries.
- Wikipedia integration provides access to a vast amount of knowledge.

### Summarize Uploaded Documents

- Users can upload documents in various formats like text, PDF, or Word documents.
- Choose between a "Synopsis" or a "Detailed Summary" option.
- Map_reduce functionality is employed to generate summaries based on document content.

### Answer Questions on Uploaded Documents

- Users can ask questions related to the uploaded documents.
- The application uses the embeddings of the uploaded documents, stored in Chroma, to find relevant answers.

## Technologies Used

- Streamlit
- Langchain
- Chroma

## Contributors

None

## Acknowledgments

N/A

## License


## Contact

