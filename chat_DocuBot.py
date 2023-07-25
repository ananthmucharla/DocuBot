import streamlit as st
from time import sleep
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
import os


def chat_module():
    llm = ChatOpenAI(temperature=0)
    tools = load_tools(["google-search", "llm-math", "wikipedia"], llm=llm)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                   verbose=False, memory=memory)

    # if there's no chat history in the session state, create it
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Send a message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # for response in openai.ChatCompletion.create(
            #         model=st.session_state["openai_model"],
            #         messages=[
            #             {"role": m["role"], "content": m["content"]}
            #             for m in st.session_state.messages
            #         ],
            #         stream=True,
            # ):
            for response in agent_chain.run(input=prompt):
                # st.write(response)
                # full_response += response.choices[0].delta.get("content", "")
                full_response += response
                message_placeholder.markdown(full_response + "▌")
                sleep(0.03)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})