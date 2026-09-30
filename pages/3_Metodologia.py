import streamlit as st

st.set_page_config(page_title="Metodología", page_icon="📚", layout="wide")

st.title("📚 Metodología y Datos")

st.markdown("""
### Datos Utilizados
- **DEM (Modelo de Elevación Digital):** Representación 3D del terreno de la cuenca.
- **Río San Juan:** Shapefile segmentado del cauce principal.

### Supuestos del Modelo
El simulador inicial utiliza un **modelo conceptual de balance hídrico**:
- El agua disponible = Aportes - Consumos - Extracciones + Retornos ± Almacenamiento
- Los valores iniciales en el MVP son aproximaciones para fines educativos e interpretativos.

### Limitaciones
- Esta versión no es un modelo hidrodinámico riguroso (ej. HEC-RAS).
- El foco está en la **comprensión de las dinámicas y compromisos** de la gestión del agua.
""")
