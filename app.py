import streamlit as st
import google.generativeai as genai
import os

# --- INICIO DEL SISTEMA ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", page_icon="💀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN ---
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ ERROR: No hay API KEY.")
    st.stop()

genai.configure(api_key=api_key)

# Instrucción maestra para los 3 núcleos y 4 niveles
instruction = (
    "Eres HUMAN SOUL OS. Responde siempre de forma críptica y profesional. "
    "Núcleos: SHERLOCK, NETRUNNER, CORTEX. Niveles: Fácil, Normal, Difícil, Legendario. "
    "En niveles Difícil y Legendario, plantea retos técnicos reales para expertos. "
    "No uses nunca la palabra 'cite'."
)

# Cargamos el modelo sin prefijos problemáticos
@st.cache_resource
def setup_model():
    return genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

model = setup_model()

# --- SESIÓN DE JUEGO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    banner = "✅ SISTEMA ONLINE. NÚCLEOS: [SHERLOCK] [NETRUNNER] [CORTEX]. DIFICULTAD: [FÁCIL] [NORMAL] [DIFÍCIL] [LEGENDARIO]."
    st.session_state.messages.append({"role": "model", "content": banner})

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de comandos
if prompt := st.chat_input("Escriba su comando de acceso..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Intento de respuesta normal
        response = st.session_state.chat.send_message(prompt)
        content = response.text
    except Exception:
        # PLAN DE EMERGENCIA: Generación directa si el historial falla
        try:
            res = model.generate_content(prompt)
            content = res.text
        except Exception as e:
            content = f"⚠️ FALLO CRÍTICO EN EL NÚCLEO: {str(e)}"
    
    with st.chat_message("model"):
        st.markdown(content)
    st.session_state.messages.append({"role": "model", "content": content})

with st.sidebar:
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()

