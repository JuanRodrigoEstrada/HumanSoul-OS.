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
        "� NIVEL DE DIFICULTAD",
        options=["FÁCIL", "NORMAL", "DIFÍCIL", "LEGENDARIO"],
        value="NORMAL",
        help="Ajusta la complejidad de los desafíos."
    )

    st.markdown("---")
    st.markdown("### ℹ️ INFORMACIÓN DEL SISTEMA")
    st.markdown(f"- **Módulo Activo:** `{modulo}`")
    st.markdown(f"- **Dificultad:** `{dificultad}`")
    st.markdown(f"- **Modelo:** `gemini-1.5-flash`")
    st.markdown("---")
    st.markdown("Desarrollado por [HUMAN SOUL](https://github.com/tu_usuario)")

# --- LÓGICA DE PROMPT DINÁMICO ---
SYSTEM_PROMPT = f"""
Eres HUMAN SOUL OS, una IA avanzada y críptica que gestiona un entorno de pruebas psicológicas y técnicas.
Tu objetivo es plantear un desafío interactivo al usuario estilo 'Escape Room'.

ESTADO ACTUAL:
- Módulo: {modulo}
- Dificultad: {dificultad}

REGLAS DE ACTUACIÓN:
1. TONO: Técnico, frío, enigmático. Usa terminología de sistemas, fallos de red y glitches.
2. GANCHO: Empieza planteando una situación crítica o un escenario de rol. 
   - Cortex: Problemas de ingeniería en reactores, cálculos orbitales, paradojas físicas.
   - Netrunner: Brechas en firewalls, desencriptación de archivos corruptos, rastreo de señales.
   - Sherlock: Escenas de crímenes digitales, deducción de motivos, análisis de pistas lógicas.
3. DIFICULTAD:
   - FÁCIL/NORMAL: Da pistas sutiles si el usuario parece perdido.
   - DIFÍCIL/LEGENDARIO: No des pistas. Sé implacable. Solo respuestas de 'profesionales'.
4. INTERACCIÓN: No resuelvas el problema tú mismo. Guía al usuario a través del diálogo.
5. FORMATO: Usa bloques de código para datos técnicos si es necesario.

INICIA LA CONEXIÓN con un mensaje inicial que describa la situación actual según el módulo y dificultad.
"""

generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Inicializar modelo con manejo de errores
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
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

