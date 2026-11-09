import time
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

# 3. Layout principal (Proporción 1:1 para que el mapa y el panel de video tengan el mismo tamaño inmenso)
main_col, control_col = st.columns([4, 1])

# --- COLUMNA IZQUIERDA: VISOR 3D ---
with main_col:
    st.subheader("Modelo Geográfico 3D")
    
    try:
        with st.spinner("Cargando modelo 3D de alta fidelidad..."):
            # Truco anti-caché: le sumamos el tiempo actual a la URL para forzar al navegador a descargar la nueva versión de GitHub Pages
            enlace_mapa = f"https://jesushernanllarenageologo.github.io/Simulador_Villicum-/static/visor_3d/index.html?refresh={time.time()}"
            
            # Usamos el componente iframe de Streamlit
            components.iframe(enlace_mapa, height=600, scrolling=False)
            
    except Exception as e:
        st.error(f"Error al dibujar el mapa: {e}")

# --- COLUMNA DERECHA: CONTROLES ---
with control_col:
    st.subheader("Controles")
    
    # --- SISTEMA DE MONITOREO DE VIDEO NATIVO ---
    st.write("Cámaras de Infraestructura")
    nodo_seleccionado = st.selectbox(
        "Punto de Inspección:", 
        ["--- Seleccionar ---", "Dique 1 (Punta Negra)", "Dique 2 (Los Caracoles)", "Dique 3 (Ullum)"]
    )
    
    if nodo_seleccionado == "Dique 3 (Ullum)":
        st.success("Transmisión en Vivo: Dique 3")
        
        # Contenedor con borde para darle aspecto de pantalla de control SCADA
        with st.container(border=True):
            st.video("static/visor_3d/videos/ullum_superavitario.mp4", autoplay=True)
            
    elif nodo_seleccionado != "--- Seleccionar ---":
        st.info(f"Cámara en {nodo_seleccionado} temporalmente fuera de línea.")
        
    st.divider()
    
    # --- CONTROLES ORIGINALES ---
    st.write("Seleccione el escenario hidrológico inicial.")
    
    escenario = st.selectbox(
        "Escenario",
        ["Normal", "Sequía", "Superavitario"]
    )
    
    if st.button("▶ Iniciar", use_container_width=True):
        
        # Guardamos el escenario elegido
        st.session_state.escenario_seleccionado = escenario
        
        # Avanzamos la etapa del simulador
        avanzar_etapa()
        
        # Vamos a la pantalla de simulación
        st.switch_page("pages/5_Simulacion.py")