import streamlit as st
from core.state_manager import init_session_state, avanzar_etapa, get_estado_actual
from core.mapa_3d import dibujar_mapa

# 1. Configuración de la página
st.set_page_config(page_title="Simulador", page_icon="🕹️", layout="wide")
init_session_state()

st.title("🕹️ Simulador Hídrico")

# 2. Parte superior: Estado general
col1, col2, col3, col4 = st.columns(4)
col1.metric("Caudal actual", f"{st.session_state.caudal_actual}")
col2.metric("Reserva Embalses", f"{st.session_state.reserva_embalses}")
col3.metric("Demanda Total", "0 %") 
col4.metric("Etapa actual", get_estado_actual())

st.divider()

# 3. Layout principal
main_col, control_col = st.columns([3, 1])

# --- COLUMNA IZQUIERDA: VISOR 3D ---
with main_col:
    st.subheader("Modelo Geográfico 3D")
    
    try:
        with st.spinner("Cargando modelo 3D de alta fidelidad..."):
            # Llamamos a la función segura que creamos en core
            dibujar_mapa()
    except Exception as e:
        st.error(f"Error al dibujar el mapa: {e}")

# --- COLUMNA DERECHA: CONTROLES ---
with control_col:
    st.subheader("Controles")
    st.write("Seleccione el escenario hidrológico inicial.")
    
    escenario = st.selectbox("Escenario", ["Normal", "Sequía", "Abundancia"])
    
    if st.button("▶ Iniciar"):
        avanzar_etapa()
        st.rerun()