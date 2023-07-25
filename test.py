import streamlit as st
from time import sleep
from streamlit_option_menu import option_menu
import base64

my_resp = "The Sun is the star at the center of the Solar System. It is a nearly perfect ball of hot plasma," \
          " heated to incandescence by nuclear fusion reactions in its core. The Sun radiates this energy mainly " \
          "as light, ultraviolet, and infrared radiation, and is the most important source of energy for life on Earth."

message_placeholder = st.empty()
full_response = ""

for char in my_resp:
    full_response += char
    message_placeholder.markdown(full_response + "▌")
    sleep(.01)
message_placeholder.markdown(full_response)
    # sleep(.1)

#
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
#         background-size: 100% 100%;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )
#
# st.set_page_config(page_title="Chatbot Home Page", page_icon=":guardsman:", layout="wide")
#
# add_bg_from_local('docubot_background.png')
#
# with st.sidebar:
#     st.image('DocuBot.png')
#     selected2 = option_menu(None, ["Home", "Chat", "Summarize", 'QnA'],
#                             icons=['house', 'chat-dots', "file-text", 'question-diamond'],
#                             menu_icon="cast", default_index=0, orientation="vertical")
#
# st.title('Welcome to DocuBot!')
# st.subheader('I can chat, summarize and answer any questions users may have on uploaded documents.')
#
# st.header('Features')
# st.write('1. Chat with the bot')
# st.write('2. Summarize uploaded documents')
# st.write('3. Answer any questions users may have on uploaded documents')