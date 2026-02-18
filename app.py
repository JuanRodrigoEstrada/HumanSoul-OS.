import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", page_icon="💀", layout="wide")

# --- ESTILOS RETRO TERMINAL ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatInput textarea { background-color: #111; color: #39FF14 !important; border: 1px solid #39FF14; }
    .stButton>button { color: #000000; background-color: #39FF14; border: 2px solid #39FF14; font-weight: bold; width: 100%; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; font-family: 'Courier New', Courier, monospace !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE IA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ ERROR: FALTA API KEY.")
    st.stop()

# Configuración forzando la versión estable de la API
genai.configure(api_key=api_key)

SYSTEM_PROMPT = """
ERES EL SISTEMA HUMAN SOUL OS.
NÚCLEOS: [SHERLOCK], [NETRUNNER], [CORTEX].
NIVELES: [FÁCIL], [NORMAL], [DIFÍCIL], [LEGENDARIO].
En DIFÍCIL y LEGENDARIO actúa para PROFESIONALES.
Tono críptico. No uses la palabra 'cite'.
"""

# Inicialización robusta
@st.cache_resource
def get_model():
    # Usamos la cadena de nombre completa para evitar ambigüedades con la v1beta
    return genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
        system_instruction=SYSTEM_PROMPT
    )

model = get_model()

# --- LÓGICA DE SESIÓN ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    banner = """
    ```
    ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗     ███████╗ ██████╗ ██╗   ██╗██╗     
    ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║     ██╔════╝██╔═══██╗██║   ██║██║     
    ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║     ███████╗██║   ██║██║   ██║██║     
    ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║     ╚════██║██║   ██║██║   ██║██║     
    ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║     ███████║╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝     ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝
    ```
    ✅ SISTEMA V1.0.3 STABLE ONLINE.
    > NÚCLEOS: SHERLOCK / NETRUNNER / CORTEX
    > DIFICULTAD: FÁCIL / NORMAL / DIFÍCIL / LEGENDARIO
    """
    st.session_state.messages.append({"role": "model", "parts": [banner]})
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFAZ ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["parts"][0])

if prompt := st.chat_input("Escriba su comando..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    
    try:
        # Intento de respuesta vía chat
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("model"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
    except Exception as e:
        # Plan B: Generación directa si el objeto chat falla
        try:
            direct_res = model.generate_content(prompt)
            with st.chat_message("model"):
                st.markdown(direct_res.text)
            st.session_state.messages.append({"role": "model", "parts": [direct_res.text]})
        except Exception as e2:
            st.error(f"⚠️ FALLO CRÍTICO DE CONEXIÓN: {str(e2)}")

with st.sidebar:
    if st.button("🔴 REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()
