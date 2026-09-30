import plotly.graph_objects as go
import rasterio
import geopandas as gpd
import numpy as np
import streamlit as st

@st.cache_data
def generar_modelo_3d(ruta_dem, ruta_rio):
    # 1. Procesar el DEM
    with rasterio.open(ruta_dem) as src:
        band1 = src.read(1)
        
        # Reemplazar valores NoData con NaN para que Plotly los ignore
        nodata = src.nodata
        if nodata is not None:
            band1 = np.where(band1 == nodata, np.nan, band1)
            
        # Simplificación dinámica extra para mantener el rendimiento
        factor = max(1, src.width // 150)
        z = band1[::factor, ::factor]
        
        cols, rows = np.meshgrid(np.arange(src.width)[::factor], np.arange(src.height)[::factor])
        xs, ys = rasterio.transform.xy(src.transform, rows, cols)
        x_dem = np.array(xs)
        y_dem = np.array(ys)

    fig = go.Figure(data=[go.Surface(
        z=z, x=x_dem, y=y_dem, 
        colorscale='Earth', 
        opacity=0.8,
        showscale=False,
        name='Terreno'
    )])

    # 2. Procesar el Río
    rio = gpd.read_file(ruta_rio)
    
    x_rio, y_rio, z_rio = [], [], []
    
    with rasterio.open(ruta_dem) as src_rio:
        for geom in rio.geometry:
            if geom.geom_type == 'LineString':
                coords = np.array(geom.coords)
                x_rio.extend(coords[:, 0])
                y_rio.extend(coords[:, 1])
                
                # Interpolar la altura Z del río basándose en el DEM para que se apoye en el terreno
                for coord in coords:
                    try:
                        val = next(src_rio.sample([(coord[0], coord[1])]))
                        z_rio.append(val[0] + 20) # +20 metros de exageración para asegurar visibilidad
                    except:
                        z_rio.append(None)
                        
                x_rio.append(None)
                y_rio.append(None)
                z_rio.append(None)

    fig.add_trace(go.Scatter3d(
        x=x_rio, y=y_rio, z=z_rio,
        mode='lines',
        line=dict(color='aqua', width=5),
        name='Río San Juan'
    ))

    # 3. Configuración de la cámara interactiva
    fig.update_layout(
        scene=dict(
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=0.2), # Exageración vertical del terreno
            xaxis_title='Longitud',
            yaxis_title='Latitud',
            zaxis_title='Elevación (m)'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=600
    )
    
    return fig