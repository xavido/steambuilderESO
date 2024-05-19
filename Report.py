import openai

import time
import mysql.connector
import base64
import csv
import requests
import ftplib

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import os

assistant_id = st.secrets["OPENAI_ASSISTANT"]
db_host = st.secrets["DB_HOST"]
db_port = st.secrets["DB_PORT"]
db_name =  st.secrets["DB_NAME"]
db_user =  st.secrets["DB_USER"]
db_password =  st.secrets["DB_PASSWORD"]

client = openai
count = 0

csv_file_path = 'egipto_informe_5.csv'

if os.path.exists(csv_file_path):
  os.remove(csv_file_path)
else:
  print("The file does not exist")

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="Informe sobre - Parlant amb...Júlia (Història)",page_icon="✅",layout="wide")

openai.api_key = st.secrets["auto_pau"]

l1 = ['xdominguez', 'aorti']
lc = ['dajil','fali','wboutafah','acano','scolmenarez','ocontreras','efreitas','cdiaz','rdisla','rhaiek','aessalhi',
'ifatima','nfernandez','jgaleano','ngonzalez','omartinez','mmuhammad','tmuhammad','lnaharro','npresciutti','hrabani','jroldan',
'oruiz','asenon','gsingh','vtrinidad','svilla','jzalkaliani','azepeda','azeaaj','mabdul','sasghar','mabrioul','maslam','mcabanillas','wcardenas',
'acerro','ecolmenarez','jcruz','adiaz','fduron','dfernandez','m_fernandez','ifigueroa','sghanem','maguisao','limran','clara','jmendoza',
'hmir','hnoor','napresciutti','krani','kromero','hsingh','asoriano','bvalencia','kzaman']

#list(set(listA) & set(listB))
listcaptions =[]
listimages = []
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
    if nom != '' and nom in l1:
        st.session_state.disabled = True
        st.session_state.start_chat = True
        st.session_state.disabled = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    else:
        if nom != '':
            st.sidebar.write(":red[Este usuario no existe]")

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
  nom = st.text_input("Escriu la teva identificació 👇",disabled=st.session_state.disabled, key=1)
  submit_button = st.form_submit_button(label="Veure Informe",disabled=st.session_state.disabled, on_click=disable)

  if submit_button and nom != '' and nom in l1:
        st.session_state.disabled = True
        st.session_state.start_chat = True
        st.session_state.disabled = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id


st.title("Informe - Parlant amb...Júlia")

st.sidebar.button("Sortir de l'Informe",on_click=enable)

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Crea una conexión con la base de datos
        conn = mysql.connector.connect(host=db_host, port=db_port, database=db_name, user=db_user,
                                                       password=db_password)

        # Crea un cursor para ejecutar comandos SQL
        cur = conn.cursor()

        # Ejecuta una consulta SQL
        sql = "SELECT * FROM teclaPREGUNTES WHERE tema = '10000'"
        cur.execute(sql)

        # Obtiene los resultados de la consulta
        results_database = cur.fetchall()
        if results_database:
            # New empty list called 'result'. This will be written to a file.
            result = list()

            # The row name is the first entry for each entity in the description tuple.
            column_names = list()
            for i in cur.description:
                column_names.append(i[0])

            result.append(column_names)
            for row in results_database:
                result.append(row)

            # Write result to file.
            with open(csv_file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in result:
                    csvwriter.writerow(row)

        else:
            sys.exit("No rows found for query: {}".format(sql))

        conn.commit()

        # Cierra la conexión con la base de datos
        cur.close()
        conn.close()

        # read csv from a URL
        @st.experimental_memo
        def get_data() -> pd.DataFrame:
            return pd.read_csv(csv_file_path)


        df = get_data()
        # top-level filters
        #user_filter = st.selectbox("Escull un usuari", pd.unique(df["idc"]))
        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("### Distribució de Preguntes")
            conteo = df['idc'].value_counts().reset_index()
            conteo.columns = ['Usuario', 'Número de Preguntas']
            # Crea el gráfico de columnas
            #fig = px.bar(conteo, x='Usuario', y='Número de Preguntas', title='Número de preguntas por usuarix')
            #fig = px.pie(df, values='pregunta', names='idc')
            #st.write(fig)
            fig2 = px.pie(conteo, values='Número de Preguntas', names='Usuario',title='Número de preguntes per usuarix')
            st.write(fig2)

        with fig_col2:
            st.markdown("### Preguntes per data")
            df['data'] = pd.to_datetime(df['data']).dt.date
            # Agrupa por fecha y cuenta las preguntas únicas por fecha
            conteo_preguntas = df.groupby('data')['pregunta'].nunique().reset_index()
            conteo_preguntas.columns = ['Data', 'Número de Preguntes']

            # Crea el gráfico de columnas
            fig = px.bar(conteo_preguntas, x='Data', y='Número de Preguntes',
                         title='Número de Preguntes per Data')

            st.write(fig)

        st.markdown ('### Llistat usuaris sense participar')
        noparticipating = list(set(lc) - set(df['idc']))
        us_noparticipating = ",".join(str(element) for element in noparticipating)
        st.markdown(us_noparticipating)
        st.markdown("### Dades Completes")
        st.dataframe(df,width=1800,column_order=("idc","pregunta","resposta"),column_config={"idc": "Usuari","pregunta":"Pregunta","resposta": "Resposta","id":None,"tema":None,"curso":None,})
        #for i in range(len(df['infografia'])):
        #    if df['infografia'][i]:
        #        df['infografia'][i] = "https://www.xavidominguez.com/tecla/"+str(df['infografia'][i])
        #        #st.write(df['infografia'][i])
        #        listimages.append(str(df['infografia'][i]))
        #        listcaptions.append(df['pregunta'][i])

        #st.image(listimages,caption=listcaptions,width=200,output_format="JPEG")
        # Realiza una petición a la API de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # O el modelo que estés utilizando
            messages=[
                {"role": "system", "content": "Eres un analista de datos y linguista catalan."},
                {"role": "user", "content": "Puedes analizar esta información:"+df[idc]+". Devuelve un string con cada usuario idc."}
            ]
        )

        # Imprime la respuesta
        st.markdown(response.choices[0].message['content'])
else:
    st.write("Afegeix les teves dades i fes click a Veure Informe.")