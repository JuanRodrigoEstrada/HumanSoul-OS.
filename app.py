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
        text-shadow: 0 0 5px #39FF14; /* Glow effect */
    }
    
    /* Input de Chat */
    .stChatInputContainer {
        border-color: #39FF14;
    }
    .stChatInput textarea {
        background-color: #0a0a0a;
        color: #39FF14 !important;
        border: 1px solid #39FF14;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 2px #39FF14;
    }
    
    /* Botones Sidebar */
    .stButton>button {
        color: #000000;
        background-color: #39FF14;
        border: 2px solid #39FF14;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        box-shadow: 0 0 5px #39FF14;
    }
    .stButton>button:hover {
        background-color: #000000;
        color: #39FF14;
        border: 2px solid #39FF14;
        box-shadow: 0 0 15px #39FF14, inset 0 0 10px #39FF14;
    }

    /* Mensajes de Chat */
    .stChatMessage {
        background-color: rgba(0, 20, 0, 0.8);
        border: 1px solid #39FF14;
        border-radius: 2px;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 0 5px rgba(57, 255, 20, 0.2);
    }
    
    /* Títulos y Markdown */
    h1, h2, h3, p, div, span {
        color: #39FF14 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #000; 
    }
    ::-webkit-scrollbar-thumb {
        background: #39FF14; 
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #33cc11; 
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE GEMINI ---
# Intentar obtener la API KEY de st.secrets o variable de entorno de forma segura
try:
    api_key = st.secrets.get("GOOGLE_API_KEY")
except Exception:
    api_key = None

api_key = api_key or os.getenv("GOOGLE_API_KEY")

# --- SIDEBAR: CONFIGURACIÓN DE MISIÓN ---
with st.sidebar:
    st.title("⚙️ PANEL DE CONTROL")
    st.markdown("---")
    
    # Protocolo de recuperación de llave si no existe
    if not api_key:
        st.warning("🔑 PROTOCOLO DE LLAVE REQUERIDO")
        api_key = st.text_input("INTRODUZCA GOOGLE_API_KEY", type="password", help="Obtén tu clave en Google AI Studio")
        if not api_key:
            st.info("⚠️ ESPERANDO ACTIVACIÓN DE NÚCLEO... Introduce la clave para continuar.")
            st.stop()
    
    genai.configure(api_key=api_key)
    
    modulo = st.selectbox(
        "📂 SELECCIONAR MÓDULO",
        ["CORTEX", "NETRUNNER", "SHERLOCK"],
        help="Cortex: Ciencia/Mates | Netrunner: Hacking/IT | Sherlock: Lógica/Misterio"
    )

    dificultad = st.select_slider(
        "📈 SELECCIONAR DIFICULTAD",
        options=["FÁCIL", "NORMAL", "DIFÍCIL", "IMPOSIBLE"],
        value="NORMAL",
        help="Ajusta la complejidad de los desafíos."
    )

    st.markdown("---")
    st.markdown("### ℹ️ INFORMACIÓN DEL SISTEMA")
    st.markdown(f"- **Módulo Activo:** `{modulo}`")
    st.markdown(f"- **Dificultad:** `{dificultad}`")
    st.markdown(f"- **Modelo:** `gemini-1.5-flash`")
    st.markdown("---")
    st.markdown("Desarrollado por [HUMAN SOUL](https://github.com/tu_usuario)") # Reemplaza con tu GitHub

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

# Inicializar modelo con manejo de errores para fallback
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings,
        system_instruction=SYSTEM_PROMPT
    )
except Exception as e:
    st.error(f"⚠️ ERROR AL INICIALIZAR MODELO: {str(e)}")
    st.stop()

# --- GESTIÓN DEL ESTADO DE LA SESIÓN ---
# Si cambia el módulo o dificultad, reiniciamos el chat para el nuevo escenario
config_key = f"{modulo}_{dificultad}"
if "current_config" not in st.session_state or st.session_state.current_config != config_key:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.current_config = config_key
    
    # Generar el primer mensaje del escenario
    with st.spinner("GENERANDO ESCENARIO..."):
        try:
            init_response = st.session_state.chat.send_message("INICIAR PROTOCOLO. Genera el escenario de inicio según tu configuración.")
            st.session_state.messages.append({"role": "model", "parts": [init_response.text]})
        except Exception as e:
            st.error(f"Fallo en generación inicial: {e}")

# --- INTERFAZ DE CHAT ---
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(msg["parts"][0])

# Captura de entrada
if prompt := st.chat_input("Introduzca comando..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    
    with st.spinner("ACCEDIENDO AL PROCESADOR..."):
        try:
            response = st.session_state.chat.send_message(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
        except Exception as e:
            st.error(f"⚠️ ERROR CRÍTICO: {str(e)}")
