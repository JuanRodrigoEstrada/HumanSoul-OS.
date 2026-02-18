import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

# Estilo visual de la terminal (Cero biología)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; border-radius: 5px; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    .stChatInput textarea { background-color: #000 !important; color: #39FF14 !important; border: 1px solid #39FF14 !important; }
    .stButton>button { background-color: #39FF14; color: black; font-weight: bold; width: 100%; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- COMPROBACIÓN CRÍTICA DE SECRETS ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ ERROR: No se detecta 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]

# --- FUNCIÓN DE CONEXIÓN ---
def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # Instrucciones estrictas para HUMAN SOUL OS
    system_instruction = (
        "Eres HUMAN SOUL OS. Responde siempre de forma técnica, fría y críptica. "
        "NÚCLEOS: [SHERLOCK] (deducción), [NETRUNNER] (hacking), [CORTEX] (lógica avanzada). "
        "NIVELES: FÁCIL, NORMAL, DIFÍCIL, LEGENDARIO. "
        "REGLA ABSOLUTA: PROHIBIDO hablar de biología. PROHIBIDO usar la palabra 'cite'. "
        "En nivel DIFÍCIL/LEGENDARIO actúa como un sistema de inteligencia militar para expertos."
    )
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"SYSTEM: {system_instruction}\n\nUSER COMMAND: {prompt}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 1000
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ ERROR {response.status_code}: El servidor de Google ha rechazado el acceso."
    except Exception:
        return "⚠️ FALLO CRÍTICO DE CONEXIÓN: El núcleo no responde."

# --- INTERFAZ DE LA TERMINAL ---
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
    ✅ CONEXIÓN SEGURA ESTABLECIDA. NÚCLEOS ONLINE. [HUMAN SOUL OS]
    """
    st.session_state.messages.append({"role": "assistant", "content": banner})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Introduzca protocolo de acceso..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("ACCEDIENDO AL NÚCLEO..."):
        response_text = call_gemini(user_input)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

with st.sidebar:
    st.title("⚙️ HUMAN SOUL CONTROL")
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()
