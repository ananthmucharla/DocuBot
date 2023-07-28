from chat_DocuBot import chat_module
from qna_DocuBot import qna_module
from summary_DocuBot import summary_module
import streamlit as st
from streamlit_option_menu import option_menu

if __name__ == '__main__':

    # loading the OpenAI api key from .env
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override=True)

    # st.write(OPENAI_API_KEY)
    # openai.api_key = os.environ['OPENAI_API_KEY']

    with st.sidebar:
        st.image('img_DocuBot.png')
        selected = option_menu(None, ["Home", "Chat", "Summarize", 'QnA'],
                            icons=['house', 'chat-dots', "file-text", 'question-diamond'],
                            menu_icon="cast", default_index=0, orientation="vertical")

    # Set a default model
    # if "openai_model" not in st.session_state:
    #     st.session_state["openai_model"] = "gpt-3.5-turbo"

    if selected == 'Home':
        st.title('Welcome to DocuBot!:robot_face:')
        st.subheader('I can chat, summarize and answer any questions you may have on uploaded documents.:hugging_face:')

        st.header('Features')
        st.write(':point_right: Chat with the bot')
        st.write(':point_right: Summarize uploaded documents')
        st.write(':point_right: Answer any questions users may have on uploaded documents')

    if selected == 'Chat':
        chat_module()

    if selected == 'Summarize':
        summary_module()

    if selected == 'QnA':
        qna_module()
