import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
from time import sleep


# loading PDF, DOCX and TXT files as LangChain Documents
def load_document(file):
    import os
    name, extension = os.path.splitext(file)

    if extension == '.pdf':
        from langchain.document_loaders import PyPDFLoader
        print(f'Loading {file}')
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        from langchain.document_loaders import Docx2txtLoader
        print(f'Loading {file}')
        loader = Docx2txtLoader(file)
    elif extension == '.txt':
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file, encoding='utf-8')
    else:
        print('Document format is not supported!')
        return None

    data_uploaded = loader.load()
    return data_uploaded


# splitting data in chunks
def chunk_data(data, chunk_size=256, chunk_overlap=50):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks


# create embeddings using OpenAIEmbeddings() and save them in a Chroma vector store
def create_embeddings(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(chunks, embeddings)
    return vector_store


def ask_and_get_answer(vector_store, q, k=3):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(model='gpt-3.5-turbo-16k', temperature=1)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    answer = chain.run(q)
    return answer


# calculate embedding cost using tiktoken
def calculate_embedding_cost(texts):
    import tiktoken
    enc = tiktoken.encoding_for_model('text-embedding-ada-002')
    total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
    # print(f'Total Tokens: {total_tokens}')
    # print(f'Embedding Cost in USD: {total_tokens / 1000 * 0.0004:.6f}')
    return total_tokens, total_tokens / 1000 * 0.0004


# clear the chat history from streamlit session state
def clear_history():
    if 'qna_history' in st.session_state:
        del st.session_state['qna_history']

    if 'vs' in st.session_state:
        del st.session_state['vs']


def qna_module():
    with st.sidebar:
        # file uploader widget
        uploaded_file = st.file_uploader('Upload a file:', type=['pdf', 'docx', 'txt'])

        # # chunk size number widget
        # chunk_size = st.number_input('Chunk size:', min_value=100, max_value=2048, value=512, on_change=clear_history)
        #
        # # k number input widget
        # k = st.number_input('k', min_value=1, max_value=20, value=3, on_change=clear_history)
        #

        chunk_size = 10000
        k = 5

        # add data button widget
        _, col2, _ = st.columns([1,1,1])

        with col2:
            add_data = st.button('Add Data', on_click=clear_history)

        if add_data and not uploaded_file:
            st.write('Please upload a document first!')

        if uploaded_file and add_data:  # if the user browsed a file
            with st.spinner('Reading, chunking and embedding file ...'):
                # writing the file from RAM to the current directory on disk
                bytes_data = uploaded_file.read()
                file_name = os.path.join('./', uploaded_file.name)
                with open(file_name, 'wb') as f:
                    f.write(bytes_data)

                data = load_document(file_name)
                chunks = chunk_data(data, chunk_size=chunk_size)
                st.write(f'Chunk size: {chunk_size}, Chunks: {len(chunks)}')

                tokens, embedding_cost = calculate_embedding_cost(chunks)
                st.write(f'Embedding cost: ${embedding_cost:.4f}')

                # creating the embeddings and returning the Chroma vector store
                vector_store = create_embeddings(chunks)

                # saving the vector store in the streamlit session state (to be persistent between reruns)
                st.session_state.vs = vector_store
                st.success('File uploaded, chunked and embedded successfully.')

    if 'qna_history' not in st.session_state:
        st.session_state.qna_history = []

    for message in st.session_state.qna_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if question := st.chat_input("Ask a question about the content of your file"):
        st.session_state.qna_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        if 'vs' in st.session_state:  # if there's the vector store (user uploaded, split and embedded a file)
            vector_store = st.session_state.vs
            answer = ask_and_get_answer(vector_store, question, k)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for char in answer:
                    full_response += char
                    message_placeholder.markdown(full_response + "▌")
                    sleep(0.03)
                message_placeholder.markdown(full_response)
            st.session_state.qna_history.append({"role": "assistant", "content": full_response})
