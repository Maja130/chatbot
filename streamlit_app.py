import streamlit as st
from openai import OpenAI

st.title("💬 Custom Assistant Chatbot")
st.write(
    "Dieser Chatbot nutzt deinen eigenen OpenAI Assistant (über die Assistants API). "
    "Gib unten deinen OpenAI API Key ein, um loszulegen."
)

# API-Key abfragen
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Bitte trage deinen OpenAI API Key ein.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Assistant-ID (dein Custom Assistant)
    ASSISTANT_ID = "asst_rzepEpQa4pUpJpqImzRPdcE9"

    # Session State für Nachrichten
    if "thread_id" not in st.session_state:
        # Jeder Nutzer bekommt seinen eigenen Thread
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Alte Nachrichten anzeigen
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Was möchtest du wissen?"):
        # User-Message speichern
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Nachricht an Thread anhängen
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # Run starten – nutzt deinen Assistant!
        run = client.beta.threads.runs.create_and_poll(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Antwort abholen
        messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
        last_message = messages.data[0].content[0].text.value

        # Anzeige + Speicherung
        with st.chat_message("assistant"):
            st.markdown(last_message)
        st.session_state.messages.append({"role": "assistant", "content": last_message})
