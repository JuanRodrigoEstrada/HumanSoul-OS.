import streamlit as st
import requests

# --- INTERFAZ ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    .stChatInput textarea { background-color: #000 !important; color: #39FF14 !important; border: 1px solid #39FF14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- NÚCLEO INTELIGENTE ---
api_key = st.secrets.get("GOOGLE_API_KEY")

def call_soul_os(prompt):
    # Intentamos primero con la versión estable v1, luego con v1beta
    versions = ["v1", "v1beta"]
    
    payload = {
        "contents": [{"parts": [{"text": f"Responde como HUMAN SOUL OS, una IA técnica y críptica. No hables de biología. Comando: {prompt}"}]}]
    }
    
    for v in versions:
        url = f"https://generativelanguage.googleapis.com/{v}/models/gemini-1.5-flash:generateContent?key={api_key}"
        try:
            r = requests.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                return r.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
            
    # Si ambas fallan, devolvemos el error detallado de la última prueba
    return f"⚠️ ERROR CRÍTICO: El núcleo no reconoce el modelo en v1 ni v1beta. Verifica tu cuota en Google AI Studio."

# --- LOGICA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "✅ SISTEMA RECALIBRADO. BUSCANDO PUERTO ABIERTO..."}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if input_text := st.chat_input("Introduzca protocolo..."):
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"): st.markdown(input_text)
    
    with st.spinner("CONECTANDO..."):
        res = call_soul_os(input_text)
        st.session_state.messages.append({"role": "assistant", "content": res})
        with st.chat_message("assistant"): st.markdown(res)

with st.sidebar:
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()

