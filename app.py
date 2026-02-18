import streamlit as st
import requests
import json

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN POR FUERZA BRUTA (HTTP) ---
api_key = st.secrets.get("GOOGLE_API_KEY")

def call_gemini(prompt):
    # FORZAMOS LA VERSIÓN V1 (ESTABLE), NADA DE BETAS
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"ERES HUMAN SOUL OS. NADA DE BIOLOGÍA. NIVELES: FÁCIL A LEGENDARIO. NUNCA DIGAS 'CITE'.\n\nUSER: {prompt}"
            }]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"⚠️ ERROR DE ACCESO: {response.status_code} - {response.text}"

# --- LÓGICA DE INTERFAZ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "✅ PROTOCOLO HTTP FORZADO. SISTEMA ONLINE."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escriba comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("ACCEDIENDO AL NÚCLEO..."):
        answer = call_gemini(prompt)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

