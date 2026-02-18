import streamlit as st
import requests

# --- INTERFAZ ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    .stChatInput textarea { background-color: #000 !important; color: #39FF14 !important; border: 1px solid #39FF14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN ---
api_key = st.secrets.get("GOOGLE_API_KEY")

def call_gemini(prompt):
    # URL para Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # Formato de carga ultra-simple para evitar ERROR 400
    payload = {
        "contents": [{
            "parts": [{
                "text": (
                    "Actúa como HUMAN SOUL OS. Responde de forma técnica y críptica. "
                    "Reglas: Prohibido hablar de biología. Prohibido usar la palabra 'cite'. "
                    f"Comando del usuario: {prompt}"
                )
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # Si hay error, mostramos el mensaje de Google para saber qué pasa
            return f"⚠️ ERROR {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ FALLO DE CONEXIÓN: {str(e)}"

# --- TERMINAL ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "✅ SISTEMA OPERATIVO HUMAN SOUL ONLINE. ESPERANDO PROTOCOLO..."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Introduzca protocolo de acceso..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("ACCEDIENDO AL NÚCLEO..."):
        res = call_gemini(user_input)
        
    st.session_state.messages.append({"role": "assistant", "content": res})
    with st.chat_message("assistant"):
        st.markdown(res)

with st.sidebar:
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()
