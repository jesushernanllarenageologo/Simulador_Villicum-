import os
import streamlit as st
import streamlit.components.v1 as components
from core.state_manager import init_session_state, avanzar_etapa, get_estado_actual

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

# 3. Layout principal: 3/4 para visualización, 1/4 para controles
main_col, control_col = st.columns([3, 1])

# --- COLUMNA IZQUIERDA: VISOR 3D ---
with main_col:
    st.subheader("Modelo Geográfico 3D")
    
    try:
        with st.spinner("Cargando modelo 3D de alta fidelidad..."):
            # Ruta absoluta para que Streamlit nunca se pierda
            ruta_visor = os.path.abspath(os.path.join(os.path.dirname(__file__), "visor_3d"))
            
            # DIAGNÓSTICO: Verificamos qué está pasando en la nube
            if not os.path.exists(ruta_visor):
                st.error(f"🚨 LA CARPETA NO SUBIÓ A INTERNET. Streamlit buscó en: {ruta_visor} y no la encontró.")
                st.info("Solución: El archivo .gitignore de GitHub está bloqueando la subida de tu carpeta.")
            elif not os.path.exists(os.path.join(ruta_visor, "index.html")):
                st.error("🚨 LA CARPETA ESTÁ, PERO ESTÁ VACÍA. Falta el archivo 'index.html'.")
            else:
                # Si todo está perfecto, cargamos el mapa
                visor_qgis = components.declare_component("visor_qgis", path=ruta_visor)
                visor_qgis(height=600)
                
    except Exception as e:
        st.error(f"Error técnico al cargar el visor 3D: {e}")

# --- COLUMNA DERECHA: CONTROLES ---
with control_col:
    st.subheader("Controles")
    st.write("Seleccione el escenario hidrológico inicial.")
    
    escenario = st.selectbox("Escenario", ["Normal", "Sequía", "Abundancia"])
    
    if st.button("▶ Iniciar"):
        avanzar_etapa()
        st.rerun()