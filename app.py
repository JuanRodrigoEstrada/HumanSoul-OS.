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
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN DIRECTA (ELIMINA EL ERROR 404) ---
api_key = st.secrets["GOOGLE_API_KEY"]

def call_gemini(prompt):
    # Usamos la URL v1 estable para evitar el problema de la v1beta
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # Instrucciones estrictas: Nada de biología, núcleos expertos.
    system_instruction = (
        "Eres HUMAN SOUL OS. Responde de forma críptica, breve y técnica. "
        "Núcleos: [SHERLOCK] (investigación), [NETRUNNER] (hacking), [CORTEX] (lógica pura). "
        "Niveles: FÁCIL, NORMAL, DIFÍCIL, LEGENDARIO. "
        "PROHIBIDO: Temas de biología y la palabra 'cite'. "
        "Si el nivel es DIFÍCIL o LEGENDARIO, sé extremadamente técnico."
    )
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"SYSTEM_INSTRUCTION: {system_instruction}\n\nUSER_COMMAND: {prompt}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "maxOutputTokens": 800
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"⚠️ FALLO EN EL NÚCLEO: {str(e)}"

# --- LÓGICA DE LA TERMINAL ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "✅ PROTOCOLO HTTP ESTABLECIDO. NÚCLEOS ONLINE. ESPERANDO COMANDO..."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Escriba su comando de acceso..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("PROCESANDO EN NÚCLEO..."):
        response_text = call_gemini(user_input)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

with st.sidebar:
    st.title("⚙️ SYSTEM")
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()
