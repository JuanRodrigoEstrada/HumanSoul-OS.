import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="HUMAN SOUL // TERMINAL",
    page_icon="💀",
    layout="wide"
)

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

# --- CONFIGURACIÓN IA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ ERROR: FALTA API KEY.")
    st.stop()

# Configuración de la librería
genai.configure(api_key=api_key)

# INSTRUCCIÓN MAESTRA
SYSTEM_PROMPT = """
ERES EL SISTEMA HUMAN SOUL OS.
NÚCLEOS: [SHERLOCK], [NETRUNNER], [CORTEX].
NIVELES: [FÁCIL], [NORMAL], [DIFÍCIL], [LEGENDARIO].
En DIFÍCIL y LEGENDARIO actúa como un sistema para PROFESIONALES.
Tono críptico. No uses la palabra 'cite'.
"""

# --- INICIALIZACIÓN DEL MODELO ---
# Usamos un bloque try/except específico para capturar el modelo de forma estable
@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM_PROMPT
    )

model = load_model()

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
    ✅ SISTEMA V1.0.2 STABLE ONLINE.
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
        # Forzamos la respuesta del chat
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("model"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
    except Exception as e:
        # Si falla, intentamos una llamada directa sin historial para desbloquear
        try:
            direct_response = model.generate_content(prompt)
            with st.chat_message("model"):
                st.markdown(direct_response.text)
            st.session_state.messages.append({"role": "model", "parts": [direct_response.text]})
        except Exception as e2:
            st.error(f"⚠️ FALLO CRÍTICO: {str(e2)}")

with st.sidebar:
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()
