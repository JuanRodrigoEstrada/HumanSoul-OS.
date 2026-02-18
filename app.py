import streamlit as st
from google import genai
import os

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatInput textarea { background-color: #111; color: #39FF14 !important; border: 1px solid #39FF14; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; margin-bottom: 10px; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    .stButton>button { background-color: #39FF14; color: black; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN CON EL NUEVO SDK ---
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ ERROR: FALTA LA API KEY.")
    st.stop()

# Inicializamos el cliente moderno
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-1.5-flash"

# Instrucciones del sistema para ScanVital / HumanSoul
SYSTEM_PROMPT = """
Eres HUMAN SOUL OS. Un sistema experto y críptico.
NÚCLEOS: [SHERLOCK] (Deducción), [NETRUNNER] (Ciberseguridad), [CORTEX] (Matemáticas/Biología).
NIVELES: [FÁCIL], [NORMAL], [DIFÍCIL], [LEGENDARIO].
REGLA DE ORO: En niveles DIFÍCIL y LEGENDARIO, actúa como un sistema para PROFESIONALES.
No uses nunca la palabra 'cite'. Responde siempre en español.
"""

# --- LÓGICA DE SESIÓN ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    banner = "✅ SISTEMA V1.0.4 STABLE ONLINE. IDENTIFIQUE NÚCLEO Y NIVEL."
    st.session_state.messages.append({"role": "model", "content": banner})

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- ENTRADA DE COMANDOS ---
if prompt := st.chat_input("Escriba su comando de acceso..."):
    # Añadir mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Generación con el nuevo SDK (esto evita el error 404 de la beta)
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config={'system_instruction': SYSTEM_PROMPT}
        )
        
        answer = response.text
        with st.chat_message("model"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "model", "content": answer})
        
    except Exception as e:
        error_msg = f"⚠️ FALLO CRÍTICO DE HARDWARE: {str(e)}"
        st.error(error_msg)

with st.sidebar:
    st.title("⚙️ CONTROL")
    if st.button("🔴 REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()

