import streamlit as st

st.set_page_config(page_title="Escenarios", page_icon="📊", layout="wide")

st.title("📊 Comparar Escenarios")

st.markdown("""
En esta sección se podrán comparar los resultados de diferentes simulaciones.
Por ejemplo: **Sequía vs Normal**.

*Esta funcionalidad se desarrollará en futuras iteraciones del MVP.*
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Escenario: Sequía")
    st.info("Gráficos y métricas del escenario de sequía")

with col2:
    st.subheader("Escenario: Normal")
    st.info("Gráficos y métricas del escenario normal")
