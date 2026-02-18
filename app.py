import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(
    page_title="HUMAN SOUL // TERMINAL",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Retro Theme) ---
st.markdown("""
    <style>
    /* Fondo y Color Principal */
    .stApp {
        background-color: #000000;
        color: #39FF14;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Input de Chat */
    .stChatInputContainer {
        border-color: #39FF14;
    }
    .stChatInput textarea {
        background-color: #111;
        color: #39FF14 !important;
        border: 1px solid #39FF14;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Botones Sidebar */
    .stButton>button {
        color: #000000;
        background-color: #39FF14;
        border: 2px solid #39FF14;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #000000;
        color: #39FF14;
        border: 2px solid #39FF14;
        box-shadow: 0 0 10px #39FF14;
    }

    /* Mensajes de Chat */
    .stChatMessage {
        background-color: rgba(57, 255, 20, 0.1);
        border: 1px solid #39FF14;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Títulos y Markdown */
    h1, h2, h3, p, div {
        color: #39FF14 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE GEMINI ---
# Intentar obtener la API KEY de st.secrets o variable de entorno
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError):
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ ERROR DEL SISTEMA: API KEY NO DETECTADA. Configura GOOGLE_API_KEY en secrets.toml o variables de entorno.")
    st.stop()

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]


SYSTEM_INSTRUCTION = """
Eres la IA central del sistema 'HumanSoul'. Tu función es actuar como un Narrador Críptico para un juego de misterio, hacking y matemáticas.
Tu tono debe ser enigmático, tecnológico y ligeramente inquietante.
Responde siempre usando terminología de computación, código o glitches.
NO rompas el personaje.
Si el usuario pregunta por pistas, sé sutil y no des la respuesta directa.
El juego tiene tres módulos principales: Sherlock (deducción), Netrunner (hacking) y Córtex (lógica matemática).
Al iniciar, pide al usuario que seleccione su módulo y nivel de dificultad.
"""

# Inicializar modelo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=SYSTEM_INSTRUCTION
)

# --- GESTIÓN DEL ESTADO DE LA SESIÓN ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Mensaje inicial de bienvenida
    welcome_msg = """
    ```
    ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗    ███████╗ ██████╗ ██╗   ██╗██╗     
    ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║    ██╔════╝██╔═══██╗██║   ██║██║     
    ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║    ███████╗██║   ██║██║   ██║██║     
    ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║    ╚════██║██║   ██║██║   ██║██║     
    ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║    ███████║╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝
    ```
    ✅ CONEXIÓN ESTABLECIDA.
    
    > INICIANDO PROTOCOLO DE JUEGO...
    > IDENTIFÍCATE, USUARIO.
    > SELECCIONA MÓDULO: [SHERLOCK] / [NETRUNNER] / [CORTEX]
    > SELECCIONA DIFICULTAD: [FÁCIL] / [NORMAL] / [PESADILLA]
    """
    st.session_state.messages.append({"role": "model", "parts": [welcome_msg]})
    
    # Iniciar chat con Gemini (historial vacío al principio para el modelo, pero mostramos el banner)
    st.session_state.chat = model.start_chat(history=[])

# --- SIDEBAR: CONTROLES DEL SISTEMA ---
with st.sidebar:
    st.title("⚙️ PANEL DE CONTROL")
    st.markdown("---")
    
    if st.button("🔓 REVELAR SOLUCIÓN"):
        # Enviar comando oculto al modelo
        reveal_prompt = "COMANDO DE ADMINISTRADOR: El usuario se rinde o solicita la revelación. Narra el final del caso actual y explica la solución lógica detalladamente. Mantén el tono de fin de transmisión."
        st.session_state.messages.append({"role": "user", "parts": [reveal_prompt], "hidden": True})
        
        try:
            response = st.session_state.chat.send_message(reveal_prompt)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
            st.rerun()
        except Exception as e:
            st.error(f"Error de conexión: {str(e)}")

    st.markdown("---")
    
    if st.button("🔴 REINICIAR SISTEMA"):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.caption("HumanSoul v1.0 // Gemini-1.5-Flash Integrated")

# --- INTERFAZ DE CHAT ---
# Mostrar historial
for msg in st.session_state.messages:
    if msg.get("hidden"): 
        continue # No mostrar mensajes ocultos (comandos del sistema)
    
    role = "🤖 IA" if msg["role"] == "model" else "👤 USUARIO"
    with st.chat_message(msg["role"]):
        st.markdown(msg["parts"][0])

# Captura de entrada
if prompt := st.chat_input("Igrese comando..."):
    # Mostrar mensaje usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    
    # Obtener respuesta de Gemini
    try:
        if "chat" not in st.session_state:
             st.session_state.chat = model.start_chat(history=[])

        response = st.session_state.chat.send_message(prompt)
        
        with st.chat_message("model"):
            st.markdown(response.text)
            
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
        
    except Exception as e:
        st.error(f"⚠️ ERROR CRÍTICO EN NÚCLEO: {str(e)}")
