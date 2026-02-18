import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="HUMAN SOUL // TERMINAL", layout="wide")

# Estilo visual de la terminal
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #39FF14; font-family: 'Courier New', Courier, monospace; }
    .stChatMessage { background-color: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; border-radius: 5px; }
    h1, h2, h3, p, div, span { color: #39FF14 !important; }
    .stChatInput textarea { background-color: #000 !important; color: #39FF14 !important; border: 1px solid #39FF14 !important; }
    .stButton>button { background-color: #39FF14; color: black; font-weight: bold; width: 100%; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN SEGURA CON GOOGLE AI ---
def call_gemini(prompt):
    # Obtenemos la clave de Secrets
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        return "⚠️ ERROR: No se encontró GOOGLE_API_KEY en los Secrets."

    # URL usando v1beta para máxima compatibilidad con Gemini 1.5 Flash
    url_base = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    # Parámetros y Headers (La clave va aquí para que no salga en errores de URL)
    params = {'key': api_key}
    headers = {'Content-Type': 'application/json'}
    
    # Instrucción de sistema integrada en el mensaje
    system_instruction = (
        "Eres HUMAN SOUL OS. Responde siempre de forma críptica y técnica. "
        "Núcleos disponibles: [SHERLOCK] (deducción), [NETRUNNER] (hacking), [CORTEX] (lógica avanzada). "
        "Niveles: FÁCIL, NORMAL, DIFÍCIL, LEGENDARIO. "
        "Reglas estrictas: PROHIBIDO hablar de biología. PROHIBIDO usar la palabra 'cite'. "
        "Si el nivel es DIFÍCIL o LEGENDARIO, actúa como un sistema para PROFESIONALES."
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
        # Petición HTTP
        response = requests.post(url_base, headers=headers, json=payload, params=params)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            # Error controlado sin mostrar la API KEY
            return f"⚠️ ERROR DEL NÚCLEO (Código {response.status_code}): No se pudo procesar el comando."
            
    except Exception:
        return "⚠️ FALLO CRÍTICO: Conexión interrumpida por seguridad del sistema."

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
    ✅ CONEXIÓN SEGURA ESTABLECIDA. 
    > NÚCLEOS: [SHERLOCK] / [NETRUNNER] / [CORTEX]
    > DIFICULTAD: FÁCIL / NORMAL / DIFÍCIL / LEGENDARIO
    """
    st.session_state.messages.append({"role": "assistant", "content": banner})

# Dibujar mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input de comandos
if user_input := st.chat_input("Introduzca protocolo de acceso..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Procesar con spinner
    with st.spinner("ACCEDIENDO AL NÚCLEO..."):
        response_text = call_gemini(user_input)
        
    # Guardar y mostrar respuesta de la IA
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

# Menú lateral
with st.sidebar:
    st.header("⚙️ SYSTEM CONTROL")
    if st.button("🔴 REBOOT (LIMPIAR TERMINAL)"):
        st.session_state.clear()
        st.rerun()
