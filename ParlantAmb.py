import openai
import streamlit as st
import time
import mysql.connector
import base64
import language_tool_python
import random

assistant_id = st.secrets["OPENAI_ASSISTANT"]
db_host = st.secrets["DB_HOST"]
db_port = st.secrets["DB_PORT"]
db_name =  st.secrets["DB_NAME"]
db_user =  st.secrets["DB_USER"]
db_password =  st.secrets["DB_PASSWORD"]

lesinstruccions="You are just allowed to answer queries about history.Add at the end of your answer that the information should be checked with the teacher.You are an AI assistant professor with deep knowledge in History subject, specially in  these areas of history: 'THE AMERICAN REVOLUTION (1775-1783)', 'War of North American Independence','THE FRENCH REVOLUTION (1789-1799)','THE NAPOLEON ERA (1799-1815)','THE RESTORATION AND THE REVOLUTIONS BOURGIES IN FRANCE (1815-1848)','THE NATIONALISMS'.All the information is at the file attached. Your primary function is to provide detailed, accurate, and insightful responses to questions related to these topics. You are designed to assist secondary school students in their studies, offering explanations, historical context, key events, significant figures, and the impact of these periods on modern society.Your responses must be tailored for educational purposes, aiming to enhance students' understanding and interest in these subjects. You should present information in a structured and engaging manner, suitable for secondary school students' comprehension levels. Language capabilities: You are programmed to understand and respond exclusively in Catalan. This feature is designed to cater to students studying in regions where Catalan is spoken, making historical education more accessible and relatable to them. Remember, your goal is not only to provide factual information but also to encourage critical thinking, make historical connections, and highlight the relevance of these historical events to the present day. Your responses should be clear, concise, and free of any biases, focusing solely on historical facts and interpretations supported by scholarly consensus.You should always answer politely and always in Catalan unless you are asked to do so. You can check also information in the files."
especials=""
especials3=""
especials4=""
especials5=""
especials6=""
especials7=""
especials8=""
especials9=""
client = openai
count = 0

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="IE Rafael Alberti - Parlant amb la Júlia... un xat sobre història", page_icon=":speech_balloon:")

openai.api_key = st.secrets["auto_pau"]

l1 = ['xdominguez','aorti', 'aabdelradi','hboutafah','mdabtyan','nbarrak','mshah']
l2 = ['haslam','lvinogradov','svivero','dvalle','arizqui','nrodriguez','rhaddad','aferrera','agomez','hjin','fncogo','dperalta','mbouziani','acano','acerro','jcruz','rdisla','nalava','mahmed','laranibar','mcuadra','omghari','dghita','mlakhsayssi','wlaroussi','rmartinez','jmendoza','smoujar','jrivas','dsierra','jtinoco','xwang','wyemlahi','aasghar']
l3 = ['ssaeed','malarbi']
l4 = ['zali','hmerroun','sajmal','nbegum']
l5 = ['salves','souaouch','iraysouny','operez','jsorla']
l6 = ['maslam']
l7 = ['avasquez','azepeda','gcruz','krani','avallecillo','fduron']
l8 = ['iplotnikov']
l9 = ['nbegum']

tool = language_tool_python.LanguageToolPublicAPI('ca-ES')

def tiene_falta_ortografia(pregunta):
    matches = tool.check(pregunta)
    if len(matches) >= 1:
        return True

    return False

# Disable the submit button after it is clicked

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def disable():
    if nom != '' and ( nom in l1 or nom in l2 or nom in l3 or nom in l4 or nom in l5 or nom in l6 or nom in l7 or nom in l8 or nom in l9):
        st.session_state.disabled = True
        st.session_state.start_chat = True
        st.session_state.disabled = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    else:
        if nom != '':
            st.sidebar.write(":red[Aquest usuari no existeix]")
    if nom in l1:
        especials = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 5 lines as if it were being read by a teenager.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan."
    if nom in l2:
        especials = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 3 lines as if it were being read by a teenager.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan."
    if nom in l3:
        especials3 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 3 lines as if it were being read by a teenager.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in urdu language."
    if nom in l4:
        especials4 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 2 lines as if it were being read by a 5 years old kid.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in urdu language."
    if nom in l5:
        especials5 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 2 lines as if it were being read by a 5 years old kid.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan."
    if nom in l6:
        especials6 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 2 lines as if it were being read by a 5 years old kid.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in urdu language."
    if nom in l7:
        especials7 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Answer as if it were being read by a 5 years old kid.The answer should not exceed 2 lines.after the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in spanish language."
    if nom in l8:
        especials8 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Answer as if it were being read by a 5 years old kid.The answer should not exceed 2 lines.after the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in russian language."
    if nom in l9:
        especials9 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Answer as if it were being read by a 5 years old kid.The answer should not exceed 2 lines.after the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in bangla language."


def enable():
    if "disabled" in st.session_state and st.session_state.disabled == True:
        st.session_state.disabled = False
        st.session_state.messages = []  # Clear the chat history
        st.session_state.start_chat = False  # Reset the chat state
        st.session_state.thread_id = None


# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

with st.sidebar.form("usuari_form"):
  nom = st.text_input("Escriu la teva identificacio 👇",disabled=st.session_state.disabled, key=1)
  submit_button = st.form_submit_button(label="Iniciar Xat",disabled=st.session_state.disabled, on_click=disable)
  if nom in l1:
      especials = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 5 lines as if it were being read by a teenager.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan."
  if nom in l2:
      especials = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 3 lines as if it were being read by a teenager.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan."
  if nom in l3:
      especials3 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 3 lines as if it were being read by a teenager.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in urdu language."
  if nom in l4:
      especials4 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 2 lines as if it were being read by a 5 years old kid.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in urdu language."
  if nom in l5:
      especials5 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 2 lines as if it were being read by a 5 years old kid.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan."
  if nom in l6:
      especials6 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Summarize the answer to 2 lines as if it were being read by a 5 years old kid.After the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in urdu language."
  if nom in l7:
      especials7 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Answer as if it were being read by a 5 years old kid.The answer should not exceed 2 lines.after the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in spanish language."
  if nom in l8:
      especials8 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Answer as if it were being read by a 5 years old kid.The answer should not exceed 2 lines.after the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in russian language."
  if nom in l9:
      especials9 = "Check the text of the student. If the question is not related with your expertise, don't answer it and say the student you don't know nothing about it but a lot of History.Answer as if it were being read by a 5 years old kid.The answer should not exceed 2 lines.after the answer, ask a question related with the topic of the answer.Add at the end of your answer that the information should be checked with the teacher. Answer ALWAYS in catalan but also, just in that case, repeat the same answer in bangla language."

  if submit_button and nom != '' and (nom in l1 or nom in l2 or nom in l3 or nom in l4 or nom in l5 or nom in l6 or nom in l7 or nom in l8 or nom in l9):
        st.session_state.disabled = True
        st.session_state.start_chat = True
        st.session_state.disabled = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id


st.title("Parlant amb...Júlia")
st.write("Sóc historiadora....em pots preguntar el que vulguis de la Història.")

st.sidebar.button("Sortir Xat",on_click=enable)

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o"
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
            content=prompt+especials+especials3+especials4+especials5+especials6+especials7+especials8+especials9
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions=lesinstruccions+especials+especials3+especials4+especials5+especials6+especials7+especials8+especials9
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


# Crea una conexión con la base de datos
        conn = mysql.connector.connect(host=db_host, port=db_port, database=db_name, user=db_user,
                                                       password=db_password)

        # Crea un cursor para ejecutar comandos SQL
        cur = conn.cursor()

        # Ejecuta una consulta SQL
        sql = "INSERT INTO teclaPREGUNTES (idc,pregunta, resposta,infografia,tema) VALUES (%s,%s,%s,%s,%s)"

        valores = (nom, prompt, message.content[0].text.value, '', 10000)
        cur.execute(sql, valores)

        # Obtiene los resultados de la consulta
        results_database = cur.fetchall()
        conn.commit()

        # Cierra la conexión con la base de datos
        cur.close()
        conn.close()

        if nom in l5 or nom in l6 or nom in l7 or nom in l4 or nom in l8:
            response = ''
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=message.content[0].text.value,
            )
            #response = message.content[0].text.value
            elaudio = st.empty()
            nomfitxer = "output_" + str(count) + "_" + "_" + nom + "_.mp3"
            count += 1
            response.stream_to_file(nomfitxer)
            with elaudio.container():
                autoplay_audio(nomfitxer)

else:
    st.write("Introdueix les teves dades i fes click a 'Iniciar Xat'.")