import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(
    page_title="HUMAN SOUL // TERMINAL",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Retro Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatInputContainer { border-color: #39FF14; }
    .stChatInput textarea { background-color: #111; color: #39FF14 !important; border: 1px solid #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { color: #000000; background-color: #39FF14; border: 2px solid #39FF14; font-family: 'Courier New', Courier, monospace; font-weight: bold; }
    .stButton>button:hover { background-color: #000000; color: #39FF14; border: 2px solid #39FF14; box-shadow: 0 0 10px #39FF14; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; border-radius: 5px; }
    h1, h2, h3, p, div { color: #39FF14 !important; font-family: 'Courier New', Courier, monospace !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE GEMINI ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ ERROR: API KEY NO DETECTADA.")
    st.stop()

genai.configure(api_key=api_key)

# Instrucción de Sistema Maestra
SYSTEM_INSTRUCTION = """
Eres HUMAN SOUL OS, una IA de respuesta avanzada. 
NÚCLEOS DISPONIBLES:
1. SHERLOCK: Casos de deducción criminal compleja.
2. NETRUNNER: Desafíos de hacking, ciberseguridad y redes.
3. CORTEX: Problemas de lógica matemática pura y criptografía.

DIFICULTADES:
- FÁCIL/NORMAL: Entretenimiento narrativo.
- DIFÍCIL/LEGENDARIO: Diseñado para PROFESIONALES. Los retos deben ser técnicos, complejos y realistas. En nivel Legendario, no des ninguna facilidad.

REGLAS DE ORO:
- Tono: Críptico, terminal de seguridad, profesional.
- No uses nunca la palabra "cite".
- Si el usuario elige DIFÍCIL o LEGENDARIO, asume que es un experto en la materia.
"""

# Inicializar modelo con configuración corregida para evitar el error 404
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# --- GESTIÓN DE SESIÓN ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = """
    ```
    ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗     ███████╗ ██████╗ ██╗   ██╗██╗     
    ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║     ██╔════╝██╔═══██╗██║   ██║██║     
    ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║     ███████╗██║   ██║██║   ██║██║     
    ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║     ╚════██║██║   ██║██║   ██║██║     
    ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║     ███████║╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝     ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝
    ```
    ✅ CONEXIÓN CIFRADA ESTABLECIDA.
    
    > NÚCLEOS DETECTADOS: [SHERLOCK] / [NETRUNNER] / [CORTEX]
    > NIVELES: [FÁCIL] / [NORMAL] / [DIFÍCIL] / [LEGENDARIO]
    
    IDENTIFIQUE NÚCLEO Y NIVEL PARA COMENZAR.
    """
    st.session_state.messages.append({"role": "model", "parts": [welcome_msg]})
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFAZ ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["parts"][0])

if prompt := st.chat_input("Ingrese comando de acceso..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("model"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
    except Exception as e:
        st.error(f"⚠️ ERROR EN NÚCLEO: {str(e)}")

with st.sidebar:
    st.title("⚙️ SYSTEM CONTROL")
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()
