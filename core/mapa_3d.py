import os
import streamlit.components.v1 as components

# Armamos la ruta desde la carpeta 'core' hacia 'pages/visor_3d'
ruta_visor = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pages", "visor_3d"))

# Declaramos el componente aquí, fuera del alcance del bug de Streamlit
visor_qgis = components.declare_component("visor_qgis", path=ruta_visor)

def dibujar_mapa():
    visor_qgis(height=600)