import streamlit as st
import os


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
def chunk_data(data, chunk_size=256, chunk_overlap=20):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks


def synopsis_of_document(chunks):
    from langchain.chains.summarize import load_summarize_chain
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')
    chain = load_summarize_chain(llm=llm, chain_type='map_reduce', verbose=True)

    output_synopsis = chain.run(chunks)
    return output_synopsis


def summarize_document(chunks):
    from langchain.chains.summarize import load_summarize_chain
    from langchain.chat_models import ChatOpenAI
    from langchain import PromptTemplate

    map_prompt = '''
    Write a short and concise summary of the following:
    Text: `{text}`
    CONCISE SUMMARY:
    '''
    map_prompt_template = PromptTemplate(input_variables=['text'], template=map_prompt)

    combine_prompt = '''
    Write a concise summary of the following text that covers the key points.
    Add a title to the summary.
    Start your summary with an INTRODUCTION PARAGRAPH that gives an overview of the topic FOLLOWED
    by BULLET POINTS if possible AND end the summary with a CONCLUSION PHRASE.
    Text: `{text}`
    '''
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=['text'])

    llm = ChatOpenAI(model='gpt-3.5-turbo-16k', temperature=0.3)
    summary_chain = load_summarize_chain(llm, chain_type='map_reduce',
                                         map_prompt=map_prompt_template,
                                         combine_prompt=combine_prompt_template,
                                         verbose=False)

    answer = summary_chain.run(chunks)
    return answer


# calculate embedding cost using tiktoken
def calculate_embedding_cost(texts):
    import tiktoken
    enc = tiktoken.encoding_for_model('gpt-3.5-turbo-16k')
    total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
    # print(f'Total Tokens: {total_tokens}')
    # print(f'Embedding Cost in USD: {total_tokens / 1000 * 0.0004:.6f}')
    return total_tokens, total_tokens / 1000 * 0.002


def summary_module():

    chunk_size = 10000
    chunks = ""
    col1, _, col3 = st.columns([7, 1, 2])

    with col1:
        uploaded_file = st.file_uploader('Upload a file:', type=['pdf', 'docx', 'txt'])
    with col3:
        st.text("")
        st.text("")
        st.text("")
        add_data = st.button('Add Data')

    col1, col2, col3 = st.columns([1, 2, 4])

    with col2:
        synopsis = st.button('Synopsis')
    with col3:
        summary = st.button('Summary')

    if 'chunks' not in st.session_state:
        st.session_state.chunks = []

    if add_data and not uploaded_file:
        st.write('Please upload a document first!')

    if (synopsis or summary) and len(st.session_state.chunks) == 0:
        st.write('Please upload a document first!')

    if uploaded_file and add_data:  # if the user browsed a file
        with st.spinner('Reading and chunking file ...'):
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

            st.session_state.chunks = chunks
            st.success('File uploaded and chunked successfully.')

    if synopsis and len(st.session_state.chunks) > 0:
        st.write(synopsis_of_document(st.session_state.chunks))

    if summary and len(st.session_state.chunks) > 0:
        st.write(summarize_document(st.session_state.chunks))
