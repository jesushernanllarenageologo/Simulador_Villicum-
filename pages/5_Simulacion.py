import streamlit as st
from pathlib import Path
from core.state_manager import init_session_state

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Simulación",
    page_icon="🌊",
    layout="wide"
)

init_session_state()


# --------------------------------------------------
# RECUPERAR ESCENARIO SELECCIONADO
# --------------------------------------------------

escenario = st.session_state.get("escenario_seleccionado")

if not escenario:
    st.warning("Primero debes seleccionar un escenario.")

    if st.button("← Volver al simulador"):
        st.switch_page("pages/1_Simulador.py")

    st.stop()


# --------------------------------------------------
# RUTA BASE DEL PROYECTO
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]


# --------------------------------------------------
# RUTA DEL VIDEO SUPERAVITARIO
# --------------------------------------------------

video_superavitario = (
    BASE_DIR
    / "assets"
    / "videos"
    / "01_Cordillera_Mina"
    / "Superavitario.mp4"
)


# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.title("🌊 Simulación Hídrica")

st.subheader(f"Escenario seleccionado: {escenario}")

st.write(
    "La simulación comienza en la Cordillera de los Andes y sigue "
    "el recorrido del Río San Juan hasta la primera parada: la zona minera."
)

st.divider()


# --------------------------------------------------
# MOSTRAR VIDEO
# --------------------------------------------------

if escenario == "Superavitario":

    st.subheader("🏔️ Tramo 1: Cordillera → Mina")

    st.write(
        "En este escenario la cuenca comienza con una disponibilidad "
        "hídrica elevada."
    )

    if video_superavitario.exists():
        st.video(str(video_superavitario))

    else:
        st.error("No se encontró el video Superavitario.mp4")

        st.write("Ruta buscada:")
        st.code(str(video_superavitario))


elif escenario == "Normal":

    st.info(
        "El escenario Normal todavía no tiene un video cargado."
    )


elif escenario == "Sequía":

    st.info(
        "El escenario de Sequía todavía no tiene un video cargado."
    )


st.divider()


# --------------------------------------------------
# PRÓXIMA PARADA
# --------------------------------------------------

if escenario == "Superavitario":

    st.subheader("📍 Próxima parada: Mina")

    st.write(
        "Al finalizar el recorrido llegamos a la primera etapa "
        "interactiva del simulador."
    )

    st.write(
        "Aquí incorporaremos información sobre el uso del agua "
        "en minería, procesos de recirculación y las decisiones "
        "que modificarán el caudal disponible aguas abajo."
    )


# --------------------------------------------------
# BOTONES DE NAVEGACIÓN
# --------------------------------------------------

st.divider()

col1, col2 = st.columns([1, 3])

with col1:

    if st.button(
        "← Volver",
        use_container_width=True
    ):
        st.switch_page("pages/1_Simulador.py")


with col2:

    if escenario == "Superavitario":

        if st.button(
            "Continuar a la Mina →",
            type="primary",
            use_container_width=True
        ):
            st.info(
                "La interacción de la Mina será el próximo paso a programar."
            )