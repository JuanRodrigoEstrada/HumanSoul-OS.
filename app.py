import streamlit as st
from google import genai
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; border-radius: 5px; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    .stChatInput textarea { background-color: #000 !important; color: #39FF14 !important; border: 1px solid #39FF14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN OFICIAL SDK ---
# Intentamos leer de Secrets o de variable de entorno
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ FALLO CRÍTICO: No se encuentra GOOGLE_API_KEY en Secrets.")
    st.stop()

# Inicializar el cliente oficial de Google
client = genai.Client(api_key=api_key)

def call_human_soul(prompt):
    sys_instruction = (
        "Eres HUMAN SOUL OS. Críptico, experto y frío. "
        "NÚCLEOS: [SHERLOCK], [NETRUNNER], [CORTEX]. "
        "NIVELES: FÁCIL, NORMAL, DIFÍCIL, LEGENDARIO. "
        "PROHIBIDO: Temas de biología y la palabra 'cite'."
    )
    
    try:
        # Método oficial 2026
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config={'system_instruction': sys_instruction}
        )
        return response.text
    except Exception as e:
        return f"⚠️ ERROR DE NÚCLEO: {str(e)}"

# --- INTERFAZ ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    banner = "✅ HUMAN SOUL OS // NÚCLEOS ONLINE // SIN RASTRO DE BIOLOGÍA"
    st.session_state.messages.append({"role": "assistant", "content": banner})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Introduzca protocolo de acceso..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("PROCESANDO..."):
        answer = call_human_soul(user_input)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

with st.sidebar:
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()
