import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; border-radius: 5px; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    .stChatInput textarea { background-color: #000 !important; color: #39FF14 !important; border: 1px solid #39FF14 !important; }
    .stButton>button { background-color: #39FF14; color: black; font-weight: bold; width: 100%; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIÓN DE CONEXIÓN SIN FALLOS ---
def call_gemini(prompt):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        return "⚠️ ERROR: No se encontró la API KEY en Secrets."

    # PROBAMOS LA URL ESTABLE DE GEMINI 1.5 FLASH
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Instrucciones del sistema (Sin biología, núcleos expertos)
    sys_msg = "Eres HUMAN SOUL OS. Críptico y experto. Núcleos: Sherlock, Netrunner, Cortex. Sin biología."
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{sys_msg}\n\nUSER COMMAND: {prompt}"
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # Si la v1beta falla (404), intentamos automáticamente con la v1
        if response.status_code == 404:
            url_v1 = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            response = requests.post(url_v1, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ ERROR {response.status_code}: El servidor de Google rechaza la conexión."
            
    except Exception as e:
        return f"⚠️ FALLO DE RED: {str(e)}"

# --- TERMINAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    banner = "✅ CONEXIÓN SEGURA REESTABLECIDA. NÚCLEOS LISTOS. SIN RASTRO DE BIOLOGÍA."
    st.session_state.messages.append({"role": "assistant", "content": banner})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Introduzca protocolo..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("ACCEDIENDO AL NÚCLEO..."):
        response_text = call_gemini(user_input)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

with st.sidebar:
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()
