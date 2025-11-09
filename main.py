import streamlit as st
from groq import Groq

modelos = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile',
'openai/gpt-oss-120b']

st.set_page_config(page_title="lucaGPT", page_icon="💎", layout="wide")

def configurar_pagina():
    st.title("hola!!! :3")
    st.sidebar.title("que modelo querés usar?")
    nombre = st.text_input("como te llamás???")
    return nombre

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400,border=True)
    # Abrimos el contenedor del chat y mostramos el historial.
    with contenedorDelChat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    nombre = configurar_pagina()
    if st.button("hola!!!"):
       st.write(f"hola {nombre}, bienvenido!! ˶ᵔ ᵕ ᵔ˶")
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    st.title("hablamos?? (˶˃ᆺ˂˶)")
    area_chat()
    elegirModelo = st.sidebar.selectbox("modelo ( ⸝⸝´꒳`⸝⸝)", options=modelos, index=0)
    mensaje = st.chat_input("Escribí tu mensaje:")
    if mensaje:
        actualizar_historial("user", mensaje, "🧑")
        chat_completo = configurar_modelo(clienteUsuario, elegirModelo, mensaje)
        # actualizar_historial("assistant", chat_completo,"🐱")
        # st.rerun()
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🐱")
                st.rerun() 

if __name__ == "__main__":
    main()