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

# --- ESTILOS CSS (Interfaz Retro Terminal) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatInputContainer { border-color: #39FF14; }
    .stChatInput textarea { background-color: #111; color: #39FF14 !important; border: 1px solid #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { color: #000000; background-color: #39FF14; border: 2px solid #39FF14; font-family: 'Courier New', Courier, monospace; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #000000; color: #39FF14; border: 2px solid #39FF14; box-shadow: 0 0 10px #39FF14; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; border-radius: 5px; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; font-family: 'Courier New', Courier, monospace !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE LA IA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ ERROR CRÍTICO: FALTA LA CLAVE DE ACCESO (API KEY).")
    st.stop()

genai.configure(api_key=api_key)

# Instrucciones del Sistema: Núcleos y Niveles Profesionales
SYSTEM_INSTRUCTION = """
Eres el Sistema Operativo HUMAN SOUL. Un narrador críptico y avanzado.
NÚCLEOS DE OPERACIÓN:
1. SHERLOCK: Deducción forense y criminalística avanzada.
2. NETRUNNER: Hacking técnico, ciberseguridad y protocolos de red.
3. CORTEX: Lógica matemática compleja, criptografía y algoritmos.

NIVELES DE DIFICULTAD:
- FÁCIL/NORMAL: Narrativo y accesible.
- DIFÍCIL/LEGENDARIO: Nivel PROFESIONAL. Plantea retos técnicos reales que requieran conocimientos expertos en la materia seleccionada.

REGLAS ESTRICTAS:
- No uses NUNCA la palabra "cite".
- Responde siempre como una terminal de seguridad.
- Si el usuario falla en nivel Legendario, sé implacable.
"""

# Inicialización del modelo (Sin v1beta para evitar el error 404)
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
    
    > ACCESO CONCEDIDO A HUMAN SOUL OS.
    > NÚCLEOS DISPONIBLES: [SHERLOCK] / [NETRUNNER] / [CORTEX]
    > DIFICULTAD: [FÁCIL] / [NORMAL] / [DIFÍCIL] / [LEGENDARIO]
    
    INTRODUZCA SELECCIÓN DE PROTOCOLO:
    """
    st.session_state.messages.append({"role": "model", "parts": [welcome_msg]})
    st.session_state.chat = model.start_chat(history=[])

# --- INTERFAZ DE CHAT ---
for msg in st.session_state.messages:
    role_label = "🤖 SYSTEM" if msg["role"] == "model" else "👤 USER"
    with st.chat_message(msg["role"]):
        st.markdown(msg["parts"][0])

if prompt := st.chat_input("Escriba su comando..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("model"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
    except Exception as e:
        st.error(f"⚠️ FALLO EN EL NÚCLEO: {str(e)}")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ CONTROL DE SISTEMA")
    st.markdown("---")
    if st.button("🔓 REVELAR SOLUCIÓN (LOGOUT)"):
        res = st.session_state.chat.send_message("El usuario solicita terminar la sesión. Revela la solución del caso actual con detalle técnico y cierra la conexión.")
        st.session_state.messages.append({"role": "model", "parts": [res.text]})
        st.rerun()
    
    if st.button("🔴 REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption("v1.0.2 - STABLE VERSION")

