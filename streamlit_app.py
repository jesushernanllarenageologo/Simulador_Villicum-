import streamlit as st
from core.state_manager import init_session_state, reiniciar_simulacion

st.set_page_config(
    page_title="Simulador Hídrico - Río San Juan",
    page_icon="💧",
    layout="wide"
)

# Inicializar estado de la sesión
init_session_state()

st.title('💧 Simulador Hídrico Interactivo del Río San Juan')

st.markdown("""
### El Problema
La cuenca del Río San Juan es un ecosistema árido donde el agua es un recurso vital y escaso. 
Diversos actores (minería, agricultura, consumo urbano e industrial) dependen de la misma fuente de agua,
lo que requiere una gestión cuidadosa y estratégica, especialmente en escenarios de sequía.

### Objetivo
Esta aplicación web interactiva permite visualizar y comprender de manera dinámica la gestión del agua 
a lo largo de la cuenca del Río San Juan, desde la alta cordillera hasta los valles agrícolas.

### La Cuenca
El recorrido del agua comienza en la **alta cordillera y los glaciares**, pasa por zonas de **explotación minera**, 
llega a los **embalses de la cuenca media** y finalmente se distribuye en la **zona urbana y agrícola**.

### Funcionamiento
El simulador funciona por etapas. A medida que el agua avanza por el territorio, se te pedirá tomar 
decisiones sobre el uso y distribución del agua. Cada decisión afectará la disponibilidad aguas abajo.
""")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("▶ Iniciar simulación", use_container_width=True, type="primary"):
        reiniciar_simulacion()
        st.switch_page("pages/1_Simulador.py")
