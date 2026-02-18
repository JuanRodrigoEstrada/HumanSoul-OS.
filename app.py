import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="HUMAN SOUL // OS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.05); border: 1px solid #39FF14; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DEL MOTOR ---
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Forzamos Gemini 1.5 Flash que es el más compatible con cuentas gratuitas nuevas
    model = genai.GenerativeModel('gemini-1.5-flash') 
else:
    st.error("🔑 ERROR: CLAVE NO DETECTADA")
    st.stop()

def call_soul(prompt):
    try:
        # Instrucciones de sistema integradas
        response = model.generate_content(
            f"SYSTEM: Eres HUMAN SOUL OS. Responde técnico y críptico. Sin biología ni 'cite'.\nUSER: {prompt}"
        )
        return response.text
    except Exception as e:
        # Si el Pro falla, el sistema intentará decirte por qué
        return f"⚠️ FALLO DE NÚCLEO: {str(e)}"

# --- INTERFAZ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "✅ NÚCLEO RECALIBRADO. ESPERANDO PROTOCOLO."}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if user_input := st.chat_input("Introduzca comando..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    
    with st.spinner("ACCEDIENDO..."):
        res = call_soul(user_input)
        st.session_state.messages.append({"role": "assistant", "content": res})
        with st.chat_message("assistant"): st.markdown(res)
