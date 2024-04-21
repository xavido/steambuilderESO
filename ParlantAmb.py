import openai
import streamlit as st
import time

assistant_id = st.secrets["OPENAI_ASSISTANT"]

client = openai

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="IE Rafael Alberti - Parlant amb la Júlia... un xat sobre història", page_icon=":speech_balloon:")

openai.api_key = st.secrets["auto_pau"]

l1 = ['xdominguez', 'aorti', 'C', 'D', 'A', 'A', 'C']
# Disable the submit button after it is clicked
def disable():
    st.session_state.disabled = True

def enable():
    if "disabled" in st.session_state and st.session_state.disabled == True:
        st.session_state.disabled = False

# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

with st.sidebar.form("usuari_form"):
  nom = st.text_input("Escriu la teva identificacio ")
  submit_button = st.form_submit_button(label="Iniciar Xat")


  if submit_button and nom != '' and nom in l1:
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
  else:
    st.write("Aquest usuari no existeix[red]")

#if st.sidebar.button("Iniciar Xat"):
#    st.session_state.start_chat = True
#    thread = client.beta.threads.create()
#    st.session_state.thread_id = thread.id

st.title("Parlant amb...Júlia")
st.write("Soc historiadora....em pots preguntar el que vulguis de la Història.")

if st.sidebar.button("Sortir Xat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escriu aquí la teva pregunta"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="You are the best history researcher. You are only allowed to answer queries in arab and with information from your docs."
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Introdueix les teves dades i fes click a 'Iniciar Xat'.")