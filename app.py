import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

# Estilos retro
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatInput textarea { background-color: #111; color: #39FF14 !important; border: 1px solid #39FF14; }
    .stButton>button { color: #000000; background-color: #39FF14; border: 2px solid #39FF14; font-weight: bold; width: 100%; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; font-family: 'Courier New', Courier, monospace !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN IA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ ERROR: FALTA API KEY.")
    st.stop()

# Configuración básica (sin v1beta forzado)
genai.configure(api_key=api_key)

# Instrucciones para Sherlock, Netrunner y Cortex
SYSTEM_PROMPT = """
ERES HUMAN SOUL OS. NUNCA USES LA PALABRA 'CITE'.
NÚCLEOS: 
- SHERLOCK (Detectives/Deducción)
- NETRUNNER (Hacking/Ciberseguridad)
- CORTEX (Matemáticas/Lógica)

NIVELES: FÁCIL, NORMAL, DIFÍCIL, LEGENDARIO.
NOTA: Los niveles DIFÍCIL y LEGENDARIO son para PROFESIONALES. Plantea retos técnicos reales.
Tono: Terminal críptica y directa.
"""

# Inicialización limpia
@st.cache_resource
def load_game_core():
    # Usamos el nombre del modelo a secas, que es el más estable
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM_PROMPT
    )

model = load_game_core()

# --- SESIÓN ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    banner = """
    ```
    ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗
    ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║
    ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║
    ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
    ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
    ```
    ✅ SISTEMA ONLINE // VERSIÓN FINAL.
    > NÚCLEOS: [SHERLOCK] / [NETRUNNER] / [CORTEX]
    > DIFICULTAD: [FÁCIL] / [NORMAL] / [DIFÍCIL] / [LEGENDARIO]
    """
    st.session_state.messages.append({"role": "model", "parts": [banner]})
    st.session_state.chat = model.start_chat(history=[])

# Mostrar chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["parts"][0])

# Entrada de usuario
if prompt := st.chat_input("Comando..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    
    try:
        # Intento de respuesta estándar
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("model"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
    except Exception as e:
        # Si la API se pone tonta con el chat, usamos generación directa
        try:
            res_direct = model.generate_content(prompt)
            with st.chat_message("model"):
                st.markdown(res_direct.text)
            st.session_state.messages.append({"role": "model", "parts": [res_direct.text]})
        except Exception as e2:
            st.error(f"⚠️ FALLO TOTAL: {str(e2)}")

with st.sidebar:
    if st.button("🔴 RESET"):
        st.session_state.clear()
        st.rerun()
