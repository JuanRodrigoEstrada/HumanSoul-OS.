import streamlit as st
from google import genai

# Leer la clave desde Secrets
api_key = st.secrets["GOOGLE_API_KEY"]

# Configurar el cliente
client = genai.Client(api_key=api_key)

# Test de respuesta rápida
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hola, sistema operativo online."
    )
    st.write(response.text)
except Exception as e:
    st.error(f"Error de conexión: {e}")

