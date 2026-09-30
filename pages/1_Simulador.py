import streamlit as st
import streamlit.components.v1 as components
from core.state_manager import init_session_state, avanzar_etapa, get_estado_actual, reiniciar_simulacion


st.set_page_config(page_title="Simulador", page_icon="🕹️", layout="wide")
init_session_state()

st.title("🕹️ Simulador Hídrico")

# --- Parte superior: Estado general ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Caudal actual", f"{st.session_state.caudal_actual} %")
col2.metric("Reserva Embalses", f"{st.session_state.reserva_embalses} %")
col3.metric("Demanda Total", "0 %") # Placeholder
col4.metric("Etapa actual", get_estado_actual())

st.divider()

# Layout principal: 3/4 para visualización, 1/4 para controles
main_col, control_col = st.columns([3, 1])

with main_col:
    st.subheader("Modelo Geográfico 3D")
    
    try:
        with st.spinner("Cargando modelo 3D de alta fidelidad..."):
            
            # Como la carpeta ahora está al lado del archivo, la encuentra directo
            visor_qgis = components.declare_component("visor_qgis", path="visor_3d")
            visor_qgis(height=600)
            
    except Exception as e:
        st.error(f"Error al cargar el visor 3D: {e}")

with control_col:
    st.subheader("Controles")
    # ... DE AQUÍ PARA ABAJO NO TOQUES NADA, DEJA TODOS TUS BOTONES COMO ESTÁN ...
    
    # Controles según la etapa
    if st.session_state.etapa_actual == 0:
        st.write("Seleccione el escenario hidrológico inicial.")
        escenario = st.selectbox("Escenario", ["Sequía", "Normal", "Húmedo"], 
                                 index=["Sequía", "Normal", "Húmedo"].index(st.session_state.escenario))
        st.session_state.escenario = escenario
        
        if st.button("▶ Iniciar", use_container_width=True, type="primary"):
            avanzar_etapa()
            st.rerun()
            
    elif st.session_state.etapa_actual == 1:
        st.write("El agua fluye desde la Alta Cordillera.")
        st.info("El caudal avanza por el río...")
        
        if st.button("▶ Continuar a Mina", use_container_width=True, type="primary"):
            avanzar_etapa()
            st.rerun()
            
    elif st.session_state.etapa_actual == 2:
        st.write("**El agua ha llegado al sector minero.**")
        st.write("Defina la estrategia de utilización y recirculación.")
        
        st.session_state.mina_demanda = st.slider("Demanda Minera (%)", 0, 100, st.session_state.mina_demanda)
        st.session_state.mina_recirculacion = st.slider("Recirculación (%)", 0, 100, st.session_state.mina_recirculacion)
        
        if st.button("▶ Continuar recorrido", use_container_width=True, type="primary"):
            avanzar_etapa()
            st.rerun()
            
    elif st.session_state.etapa_actual == 3:
        st.write("El agua continúa hacia la Cuenca Media...")
        
        if st.button("▶ Continuar a Embalses", use_container_width=True, type="primary"):
            avanzar_etapa()
            st.rerun()
            
    elif st.session_state.etapa_actual == 4:
        st.write("**Embalses**")
        st.write("Decida cómo administrar el almacenamiento.")
        
        liberacion = st.slider("Apertura de compuertas / Liberación (%)", 0, 100, 50)
        
        if st.button("▶ Continuar recorrido", use_container_width=True, type="primary"):
            avanzar_etapa()
            st.rerun()
            
    elif st.session_state.etapa_actual == 5:
        st.write("El agua se dirige hacia Ullum y el Valle...")
        
        if st.button("▶ Continuar a Distribución", use_container_width=True, type="primary"):
            avanzar_etapa()
            st.rerun()
            
    elif st.session_state.etapa_actual == 6:
        st.write("**Distribución del agua en el Valle**")
        st.write("Asigne el agua disponible a los diferentes sectores.")
        
        st.slider("Agricultura (%)", 0, 100, 60)
        st.slider("Urbano (%)", 0, 100, 20)
        st.slider("Industrial (%)", 0, 100, 10)
        
        if st.button("▶ Ver Resultados", use_container_width=True, type="primary"):
            avanzar_etapa()
            st.rerun()
            
    elif st.session_state.etapa_actual == 7:
        st.success("Simulación completada.")
        st.write("Vea el resumen de resultados.")
        
        if st.button("↻ Reiniciar", use_container_width=True):
            reiniciar_simulacion()
            st.rerun()

st.divider()
if st.button("↻ Reiniciar simulación en cualquier momento", type="secondary"):
    reiniciar_simulacion()
    st.rerun()