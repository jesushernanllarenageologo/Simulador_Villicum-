import ipaddress
import requests
import streamlit as st
from urllib.parse import urlparse

WLED_IP = "192.168.1.6"
WLED_URL = f"http://{WLED_IP}/json/state"


def _app_abierta_en_red_local():
    """Permite controlar WLED solo cuando la app se abre desde la red local."""
    try:
        host = urlparse(st.context.url).hostname
    except (AttributeError, RuntimeError, TypeError, ValueError):
        return False

    if not host:
        return False

    host = host.lower()
    if host == "localhost" or host.endswith(".local"):
        return True

    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False


# Se calcula durante la ejecución principal de Streamlit para que los hilos
# de animación usen el mismo modo sin consultar el contexto desde otro hilo.
WLED_LOCAL_ENABLED = _app_abierta_en_red_local()


def enviar_comando_wled(payload):
    # La app pública no puede llegar a la IP privada del WLED. Omitir esos
    # comandos evita mostrar un error de conexión a quienes solo visitan la web.
    if not WLED_LOCAL_ENABLED:
        return

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
