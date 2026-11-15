import requests
import streamlit as st

WLED_IP = "192.168.1.6"
WLED_URL = f"http://{WLED_IP}/json/state"


def enviar_comando_wled(payload):
    try:
        # El WLED está en la red local: enviar la petición directa, sin proxy.
        with requests.Session() as session:
            session.trust_env = False
            response = session.post(
                WLED_URL,
                json=payload,
                timeout=(3, 8)
            )

        if response.status_code != 200:
            st.error(
                f"Error al comunicar con WLED. Código: {response.status_code}. "
                f"Detalle: {response.text[:200]}"
            )
    except requests.exceptions.RequestException as exc:
        st.error(
            f"No se pudo conectar a WLED ({WLED_IP}). "
            f"Detalle: {type(exc).__name__}: {exc}"
        )