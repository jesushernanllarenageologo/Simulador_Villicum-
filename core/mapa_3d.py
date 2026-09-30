import os
import streamlit.components.v1 as components

# Ahora buscamos la carpeta directamente en la raíz (".."), sin pasar por "pages"
ruta_visor = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "visor_3d"))

visor_qgis = components.declare_component("visor_qgis", path=ruta_visor)

def dibujar_mapa():
    visor_qgis(height=600)