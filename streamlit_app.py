import streamlit as st
from PIL import Image
from pathlib import Path

# Configuración inicial
st.set_page_config(page_title="Simulador Hídrico San Juan", page_icon="💧", layout="wide")

# Rutas de imágenes (Ajustá estas rutas a las imágenes reales que tengas en tu carpeta assets)
BASE_DIR = Path(__file__).resolve().parent
img_hero = BASE_DIR / "assets" / "images" / "mapa_cuenca.png" # O usá una foto linda del Río San Juan

# Encabezado principal
st.title("💧 Simulador Hídrico Interactivo del Río San Juan")
st.markdown("---")

# Layout de dos columnas
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### El Problema")
    st.write(
        "La cuenca del Río San Juan es un ecosistema árido donde el agua es un recurso vital y escaso. "
        "Diversos actores (minería, agricultura, consumo urbano e industrial) dependen de la misma fuente."
    )
    
    st.markdown("### Objetivo")
    st.write(
        "Esta aplicación web interactiva permite visualizar y comprender de manera dinámica la gestión del agua, "
        "desde la alta cordillera hasta los valles agrícolas, tomando decisiones en tiempo real."
    )

with col2:
    # Si tenés la imagen, la mostramos acá para romper tanto texto
    if img_hero.exists():
        st.image(str(img_hero), use_container_width=True, caption="Cuenca del Río San Juan")
    else:
        st.info("Agregá una imagen hero en assets/images/")

st.markdown("---")

# Sección de Etapas con íconos
st.markdown("### 🗺️ El Recorrido del Agua")
cols = st.columns(3)
with cols[0]:
    st.info("🏔️ **Alta Cordillera**\n\nNacimiento del recurso y paso por la zona de explotación minera.")
with cols[1]:
    st.info("🌊 **Cuenca Media**\n\nSistema de embalses (Caracoles, Punta Negra, Ullum) para regulación.")
with cols[2]:
    st.info("🏙️ **Valles y Ciudad**\n\nDistribución para uso agrícola, industrial y consumo humano.")

st.write("")

# Botón central grande
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶ INICIAR SIMULACIÓN", type="primary", use_container_width=True):
        st.switch_page("pages/1_Simulador.py") # Asegurate que la ruta al simulador sea la correcta