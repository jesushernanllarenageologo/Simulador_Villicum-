import streamlit as st
from config import settings

def init_session_state():
    """Inicializa las variables de estado de la simulación."""
    if "simulacion_activa" not in st.session_state:
        st.session_state.simulacion_activa = False
        
    if "etapa_actual" not in st.session_state:
        st.session_state.etapa_actual = 0
        
    if "escenario" not in st.session_state:
        st.session_state.escenario = "Normal"
        
    if "caudal_actual" not in st.session_state:
        st.session_state.caudal_actual = settings.ESCENARIOS["Normal"]["aporte_inicial"]
        
    if "progreso_rio" not in st.session_state:
        st.session_state.progreso_rio = 0
        
    if "mina_demanda" not in st.session_state:
        st.session_state.mina_demanda = settings.DEFAULT_MINA_DEMANDA
        
    if "mina_recirculacion" not in st.session_state:
        st.session_state.mina_recirculacion = settings.DEFAULT_MINA_RECIRCULACION
        
    if "reserva_embalses" not in st.session_state:
        st.session_state.reserva_embalses = 100 # %

def reiniciar_simulacion():
    """Reinicia el estado de la simulación al paso 0."""
    st.session_state.simulacion_activa = False
    st.session_state.etapa_actual = 0
    st.session_state.progreso_rio = 0
    escenario_actual = st.session_state.get("escenario", "Normal")
    st.session_state.caudal_actual = settings.ESCENARIOS[escenario_actual]["aporte_inicial"]

def avanzar_etapa():
    """Avanza la simulación a la siguiente etapa."""
    if st.session_state.etapa_actual < max(settings.ESTADOS_SIMULACION.keys()):
        st.session_state.etapa_actual += 1
        st.session_state.simulacion_activa = True

def get_estado_actual():
    """Retorna el nombre de la etapa actual."""
    return settings.ESTADOS_SIMULACION.get(st.session_state.etapa_actual, "Desconocido")
