import streamlit as st
from core.state_manager import init_session_state

st.set_page_config(
    page_title="Simulación",
    page_icon="🌊",
    layout="wide"
)

init_session_state()

# Comprobar que se eligió un escenario
if "escenario_seleccionado" not in st.session_state:
    st.warning("Primero debes seleccionar un escenario.")

    if st.button("← Volver"):
        st.switch_page("pages/1_Simulador.py")

    st.stop()

escenario = st.session_state.escenario_seleccionado

st.title("🌊 Simulación Hídrica")

st.subheader(f"Escenario seleccionado: {escenario}")

st.write(
    "La simulación ha comenzado. Aquí se mostrará el recorrido "
    "correspondiente al escenario seleccionado."
)

if st.button("← Volver al simulador"):
    st.switch_page("pages/1_Simulador.py")