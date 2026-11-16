import streamlit as st
from PIL import Image
from pathlib import Path

# Configuración inicial
st.set_page_config(page_title="Simulador Hídrico San Juan", page_icon="💧", layout="wide")

# Rutas de imágenes (Ajustá los nombres a los archivos que tengas en tu carpeta assets/images)
BASE_DIR = Path(__file__).resolve().parent
img_hero = BASE_DIR / "assets" / "images" / "mapa_cuenca.png" # La imagen del mapa que subiste
img_modelo = BASE_DIR / "assets" / "images" / "modelo_3d.png"    # Nueva imagen de la maqueta topográfica

# Encabezado principal
st.title("💧 Simulador Hídrico Interactivo del Río San Juan")
st.markdown("---")

# Layout de dos columnas (Agrandamos la columna derecha pasándola de 1 a 1.3)
col1, col2 = st.columns([1, 1.3])

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
    
    st.markdown("### Modelo Topográfico 3D")
    st.write(
        "Para sumar a la didáctica y facilitar la comprensión espacial del problema, la simulación "
        "se encuentra sincronizada en tiempo real con una maqueta topográfica interactiva de la cuenca. "
        "Esto permite observar el relieve, las pendientes hídricas y la ubicación exacta de las infraestructuras."
    )
    
    # Imagen del modelo 3D debajo del texto
    if img_modelo.exists():
        st.image(str(img_modelo), use_container_width=True)
    else:
        st.info("💡 Colocá acá la imagen de tu modelo 3D (guardala como 'modelo_3d.png' en assets/images/)")

with col2:
    # La imagen del mapa ahora se verá más grande porque su columna es más ancha
    if img_hero.exists():
        st.image(str(img_hero), use_container_width=True)
    else:
        st.info("💡 Colocá acá la imagen del mapa (guardala como 'mapa_cuenca.png' en assets/images/)")

st.markdown("---")

# ==========================================
# SECCIÓN: EL RECORRIDO DEL AGUA (TARJETAS)
# ==========================================
st.markdown("### El Recorrido del Agua")

# CSS personalizado para agrandar los recuadros y sacarles los íconos
estilo_tarjetas = """
<style>
.tarjeta-recorrido {
    background-color: #152b39;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #1e3d52;
    height: 160px; /* Ajustá este valor si querés los recuadros más o menos altos */
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.tarjeta-titulo {
    color: #169cad;
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 12px;
}
.tarjeta-texto {
    color: #ffffff;
    font-size: 0.95rem;
    line-height: 1.4;
}
</style>
"""
st.markdown(estilo_tarjetas, unsafe_allow_html=True)

cols = st.columns(3)

with cols[0]:
    st.markdown("""
    <div class="tarjeta-recorrido">
        <div class="tarjeta-titulo">Alta Cordillera</div>
        <div class="tarjeta-texto">Nacimiento del recurso hídrico y paso por la zona de exploración y explotación minera.</div>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div class="tarjeta-recorrido">
        <div class="tarjeta-titulo">Cuenca Media</div>
        <div class="tarjeta-texto">Sistema integral de embalses (Caracoles, Punta Negra, Ullum) para la regulación del caudal.</div>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown("""
    <div class="tarjeta-recorrido">
        <div class="tarjeta-titulo">Valles y Ciudad</div>
        <div class="tarjeta-texto">Distribución final destinada al uso agrícola, desarrollo industrial y consumo humano.</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Botón central grande
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("▶ INICIAR SIMULACIÓN", type="primary", use_container_width=True):
        st.switch_page("pages/1_Simulador.py")