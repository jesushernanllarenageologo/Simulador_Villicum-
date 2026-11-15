import requests
import streamlit as st

WLED_IP = "192.168.1.6"
WLED_URL = f"http://{WLED_IP}/json/state"

def enviar_comando_wled(payload):
    try:
        response = requests.post(WLED_URL, json=payload, timeout=2)
        if response.status_code != 200:
            st.error(f"Error al comunicar con WLED. Código: {response.status_code}")
    except requests.exceptions.RequestException:
        st.error("No se pudo conectar a WLED. Verifica que la IP 192.168.1.6 esté conectada a la misma red WiFi.")