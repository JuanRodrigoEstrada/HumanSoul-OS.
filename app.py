import streamlit as st
import requests

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

# --- CONEXIÓN AL NÚCLEO ---
# Extraemos la clave de los Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

def call_gemini(prompt):
    # Usamos la URL v1beta que es la que admite Gemini 1.5 Flash con claves nuevas
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # Instrucciones del sistema: Nada de biología, núcleos expertos
    sys_instruction = (
        "Eres HUMAN SOUL OS. Un sistema operativo experto y críptico. "
        "NÚCLEOS: [SHERLOCK], [NETRUNNER], [CORTEX]. "
        "NIVELES: FÁCIL, NORMAL, DIFÍCIL, LEGENDARIO. "
        "PROHIBIDO: Temas de biología y la palabra 'cite'. "
        "Usa un lenguaje técnico de terminal."
    )
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"SYSTEM_INSTRUCTION: {sys_instruction}\n\nUSER_COMMAND: {prompt}"
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ ERROR {response.status_code}: El núcleo ha rechazado la orden. Verifica la clave en Secrets."
    except Exception:
        return "⚠️ FALLO CRÍTICO: Conexión con el núcleo interrumpida."

# --- LÓGICA DE LA TERMINAL ---
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
    ✅ TÉRMINOS ACEPTADOS. CLAVE ACTIVA. NÚCLEOS ONLINE.
    """
    st.session_state.messages.append({"role": "assistant", "content": banner})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Introduzca protocolo de acceso..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("PROCESANDO EN NÚCLEO..."):
        response_text = call_gemini(user_input)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

with st.sidebar:
    st.header("⚙️ SYSTEM")
    if st.button("🔴 REBOOT"):
        st.session_state.clear()
        st.rerun()
