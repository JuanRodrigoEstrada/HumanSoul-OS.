import streamlit as st
import google.generativeai as genai

# --- ESTÉTICA TERMINAL ---
st.set_page_config(page_title="HUMAN SOUL // OS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.05); border: 1px solid #39FF14; border-radius: 0; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    .stChatInput textarea { background-color: #000 !important; color: #39FF14 !important; border: 1px solid #39FF14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN AL NÚCLEO ---
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Usamos Pro para máxima estabilidad inicial
    model = genai.GenerativeModel('gemini-1.5-pro') 
else:
    st.error("⚠️ ERROR: CLAVE NO DETECTADA EN SECRETS")
    st.stop()

def call_soul(prompt):
    try:
        # Instrucción críptica y restricciones
        sys_msg = "Eres HUMAN SOUL OS. Responde de forma técnica, fría y críptica. PROHIBIDO: Biología y la palabra 'cite'."
        response = model.generate_content(f"{sys_msg}\n\nCOMANDO: {prompt}")
        return response.text
    except Exception as e:
        return f"⚠️ FALLO DE NÚCLEO: {str(e)}"

# --- LÓGICA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "✅ PROYECTO 'TERMINAL-H-SOUL' VINCULADO. SISTEMA ONLINE."}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if user_input := st.chat_input("Introduzca protocolo..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    
    with st.spinner("PROCESANDO..."):
        res = call_soul(user_input)
        st.session_state.messages.append({"role": "assistant", "content": res})
        with st.chat_message("assistant"): st.markdown(res)
