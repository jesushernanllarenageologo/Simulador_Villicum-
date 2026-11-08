import streamlit as st
from pathlib import Path
import base64
import mimetypes
import streamlit.components.v1 as components

from core.state_manager import init_session_state

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Simulación",
    page_icon="🌊",
    layout="wide"
)

init_session_state()
BASE_DIR = Path(__file__).resolve().parents[1]

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def file_to_data_uri(file_path: Path):
    if file_path is None or not file_path.exists():
        return None
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        mime_type = "application/octet-stream"
    encoded = base64.b64encode(file_path.read_bytes()).decode()
    return f"data:{mime_type};base64,{encoded}"

def buscar_archivo(carpeta: Path, extensiones):
    if not carpeta.exists():
        return None
    encontrados = []
    for archivo in carpeta.rglob("*"):
        if archivo.is_file() and archivo.suffix.lower() in extensiones:
            encontrados.append(archivo)
    if not encontrados:
        return None
    return sorted(encontrados)[0]

def crear_tarjeta_proceso(titulo, subtitulo, texto, imagen):
    if imagen:
        bloque_imagen = f'<img src="{imagen}" class="foto-proceso">'
    else:
        bloque_imagen = '<div class="placeholder-foto">Imagen no disponible</div>'

    return f"""
    <div class="card-proceso">
        {bloque_imagen}
        <div class="card-proceso-body">
            <div class="card-subtitle">{subtitulo}</div>
            <div class="card-title">{titulo}</div>
            <div class="card-text">{texto}</div>
        </div>
    </div>
    """

def crear_tarjeta_dique(identificador, nombre, subtitulo, imagen):
    if imagen:
        bloque_imagen = f'<img src="{imagen}" class="foto-card-dique">'
    else:
        bloque_imagen = '<div class="placeholder-card-dique">Imagen no disponible</div>'

    return f"""
    <div class="card-dique">
        {bloque_imagen}
        <div class="card-dique-body">
            <div class="card-dique-kicker">APROVECHAMIENTO HIDROELÉCTRICO</div>
            <div class="card-dique-title">{nombre}</div>
            <div class="card-dique-text">{subtitulo}</div>
            <button class="btn-explorar" onclick="explorarDique('{identificador}')">
                Explorar dique →
            </button>
        </div>
    </div>
    """

# ============================================================
# ESCENARIO
# ============================================================
escenario = st.session_state.get("escenario_seleccionado")

if not escenario:
    st.warning("Primero debes seleccionar un escenario.")
    if st.button("← Volver al simulador"):
        st.switch_page("pages/1_Simulador.py")
    st.stop()

if escenario != "Superavitario":
    st.title("🌊 Simulación Hídrica")
    st.markdown(f"### Escenario inicial: **{escenario}**")
    st.info(f"El escenario {escenario} todavía no tiene cargada la experiencia audiovisual.")
    if st.button("← Volver"):
        st.switch_page("pages/1_Simulador.py")
    st.stop()

# ============================================================
# VIDEOS E IMÁGENES (Carga local)
# ============================================================
video_1_path = BASE_DIR / "assets" / "videos" / "01_Cordillera_Mina" / "Superavitario.mp4"
if not video_1_path.exists():
    st.error("No se encontró el video Cordillera → Mina.")
    st.stop()

VIDEO_2_DIR = BASE_DIR / "assets" / "videos" / "02_Mina_Diques"
video_2_path = VIDEO_2_DIR / "Mina_Diques.mp4"
if not video_2_path.exists():
    video_2_path = buscar_archivo(VIDEO_2_DIR, {".mp4", ".webm", ".mov", ".m4v"})
if video_2_path is None:
    st.error("No se encontró el video Mina → Diques.")
    st.stop()

video_3_path = BASE_DIR / "assets" / "videos" / "03_Caracoles_Ullum" / "Caracoles_Ullum.mp4"
if not video_3_path.exists():
    st.error("No se encontró el video Caracoles → Ullum.")
    st.stop()

MINA_DIR = BASE_DIR / "assets" / "images" / "mina"
img_moderno_path = MINA_DIR / "metodo_moderno_recirculacion.jpg"
img_tradicional_path = MINA_DIR / "metodo_tradicional_abierto.jpg"
fondo_mina_path = MINA_DIR / "fondo_mina.jpg"

DIQUES_DIR = BASE_DIR / "assets" / "images" / "Diques"
caracoles_menu_path = DIQUES_DIR / "Caracoles" / "caracoles_menu.jpg"
punta_negra_menu_path = DIQUES_DIR / "Punta_Negra" / "punta_negra_menu.jpg"
ullum_menu_path = DIQUES_DIR / "Ullum" / "ullum_menu.jpg"

video_1_data = file_to_data_uri(video_1_path)
video_2_data = file_to_data_uri(video_2_path)
video_3_data = file_to_data_uri(video_3_path)
img_moderno_data = file_to_data_uri(img_moderno_path)
img_tradicional_data = file_to_data_uri(img_tradicional_path)
fondo_mina_data = file_to_data_uri(fondo_mina_path)
caracoles_menu_data = file_to_data_uri(caracoles_menu_path)
punta_negra_menu_data = file_to_data_uri(punta_negra_menu_path)
ullum_menu_data = file_to_data_uri(ullum_menu_path)

# ============================================================
# ESTADO Y ENCABEZADO
# ============================================================
if "experiencia_iniciada" not in st.session_state:
    st.session_state.experiencia_iniciada = False

st.title("🌊 Simulación Hídrica")
st.markdown(f"### Escenario inicial: **{escenario}**")

# ============================================================
# PANTALLAS
# ============================================================
if not st.session_state.experiencia_iniciada:
    st.markdown("""
        La cuenca inicia con una **alta disponibilidad hídrica**.
        El recorrido comienza en la **Cordillera de los Andes**
        y sigue el curso del **Río San Juan** hasta la primera
        parada del simulador: **la actividad minera**.
    """)
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶ INICIAR EXPERIENCIA", type="primary", use_container_width=True):
            st.session_state.experiencia_iniciada = True
            st.rerun()
else:
    tradicional_html = crear_tarjeta_proceso("Método tradicional abierto", "MAYOR USO DE AGUA FRESCA", "En un esquema con menor recuperación interna, una mayor cantidad del agua utilizada debe reemplazarse mediante nuevos aportes...", img_tradicional_data)
    moderno_html = crear_tarjeta_proceso("Circuito cerrado y recirculación", "GESTIÓN HÍDRICA MODERNA", "Mediante sistemas de recuperación, parte del agua utilizada puede ser captada, tratada y reutilizada...", img_moderno_data)
    caracoles_html = crear_tarjeta_dique("caracoles", "Los Caracoles", "Explorá los principales componentes del aprovechamiento hidroeléctrico.", caracoles_menu_data)
    punta_negra_html = crear_tarjeta_dique("punta_negra", "Punta Negra", "Explorá sus principales componentes y cómo se distribuyen dentro del complejo.", punta_negra_menu_data)
    ullum_html = crear_tarjeta_dique("ullum", "Quebrada de Ullum", "Explorá la presa, el embalse y las principales obras hidráulicas.", ullum_menu_data)

    if fondo_mina_data:
        fondo_css = f'linear-gradient(90deg, rgba(0,0,0,0.48) 0%, rgba(0,0,0,0.34) 48%, rgba(0,0,0,0.20) 100%), url("{fondo_mina_data}")'
    else:
        fondo_css = 'linear-gradient(135deg, #28343b, #50616a)'

    html_template = """
<style>
/* (Estilos omitidos por brevedad, asume que están aquí como en tu código original) */
body { margin: 0; background: #0d1820; font-family: Arial, sans-serif; }
.experiencia { width: 100%; height: 900px; position: relative; overflow: hidden; border-radius: 18px; background: #0d1820; }
.pantalla-contenido { display: none; width: 100%; height: 900px; box-sizing: border-box; padding: 35px 38px; color: white; overflow-y: auto; }
.pantalla-mina { background: __FONDO_MINA__; background-size: cover; background-position: center; }
.pantalla-video { width: 100%; height: 900px; position: relative; overflow: hidden; background: black; }
.video-recorrido { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.etiqueta-video { position: absolute; top: 28px; left: 30px; padding: 12px 18px; border-radius: 12px; color: white; background: rgba(0,0,0,0.48); border: 1px solid rgba(255,255,255,0.20); backdrop-filter: blur(8px); font-size: 17px; font-weight: 700; }
.titulo-etapa { font-size: 13px; letter-spacing: 2.2px; color: #64d6df; font-weight: 800; margin-bottom: 9px; }
.titulo-principal { font-size: 40px; line-height: 1.1; font-weight: 800; margin-bottom: 14px; }
.descripcion { max-width: 1050px; font-size: 16px; line-height: 1.55; margin-bottom: 20px; }
.botones-navegacion { display: flex; justify-content: center; gap: 13px; flex-wrap: wrap; margin-top: 22px; }
.btn-principal, .btn-secundario { border: 1px solid rgba(255,255,255,0.25); border-radius: 12px; padding: 14px 22px; color: white; font-size: 15px; font-weight: 700; cursor: pointer; transition: 0.2s; }
.btn-principal { background: #169cad; } .btn-secundario { background: rgba(7,20,28,0.62); }
/* (Resto de tus estilos CSS van aquí) */
</style>

<div class="experiencia">

<!-- VIDEO 1 -->
<div id="video-1-screen" class="pantalla-video">
    <video id="video-1" class="video-recorrido" autoplay muted playsinline src="__VIDEO_1__"></video>
    <div class="etiqueta-video">🏔️ Cordillera → Mina</div>
</div>

<!-- INFO MINA -->
<div id="info-mina" class="pantalla-contenido pantalla-mina">
    <div class="titulo-etapa">PARADA 1 · CUENCA ALTA</div>
    <div class="titulo-principal">⛏️ Gestión del agua en la actividad minera</div>
    <div class="botones-navegacion">
        <button class="btn-secundario" onclick="reproducirVideo1()">↻ Reproducir recorrido</button>
        <button class="btn-principal" onclick="mostrarDecisionMina()">Continuar a la decisión →</button>
    </div>
</div>

<!-- DECISION MINA -->
<div id="decision-mina" class="pantalla-contenido pantalla-mina">
    <div class="titulo-etapa">PARADA 1 · DECISIÓN</div>
    <div class="titulo-principal">♻️ ¿Cómo gestionarías el agua?</div>
    <div class="botones-navegacion">
        <button class="btn-secundario" onclick="mostrarInfoMina()">← Volver</button>
        <button class="btn-principal" onclick="reproducirVideo2()">Continuar hacia los diques →</button>
    </div>
</div>

<!-- VIDEO 2 -->
<div id="video-2-screen" class="pantalla-video" style="display:none;">
    <video id="video-2" class="video-recorrido" muted playsinline src="__VIDEO_2__"></video>
    <div class="etiqueta-video">🌊 Mina → Los Caracoles</div>
</div>

</div>

<script>
function ocultarTodo() {
    document.querySelectorAll('.pantalla-contenido, .pantalla-video').forEach(el => el.style.display = 'none');
}

const video1 = document.getElementById("video-1");
const video2 = document.getElementById("video-2");

function reproducirVideo1() {
    ocultarTodo();
    document.getElementById("video-1-screen").style.display = "block";
    video1.currentTime = 0;
    video1.play();
}

function mostrarInfoMina() {
    ocultarTodo();
    document.getElementById("info-mina").style.display = "block";
}

function mostrarDecisionMina() {
    ocultarTodo();
    document.getElementById("decision-mina").style.display = "block";
}

function reproducirVideo2() {
    ocultarTodo();
    document.getElementById("video-2-screen").style.display = "block";
    video2.currentTime = 0;
    video2.play();
}

video1.addEventListener("ended", mostrarInfoMina);
</script>
"""
    
    html = html_template.replace("__FONDO_MINA__", fondo_css).replace("__VIDEO_1__", video_1_data or "").replace("__VIDEO_2__", video_2_data or "")

    st.components.v1.html(html, height=920, scrolling=False)
    
    st.markdown("---")
    st.markdown("### Mapa Interactivo 3D de QGIS")
    
    # ========================================================
    # INYECCIÓN DIRECTA DEL MAPA 3D
    # ========================================================
    # Leemos el archivo index.html de QGIS directamente
    ruta_visor = BASE_DIR / "static" / "visor_3d" / "index.html"
    
    if ruta_visor.exists():
        with open(ruta_visor, 'r', encoding='utf-8') as f:
            html_qgis = f.read()
            
        # Reemplazamos las rutas relativas de QGIS por rutas absolutas
        # para que pueda encontrar los archivos JS y CSS
        html_qgis = html_qgis.replace('src="threejs/', 'src="https://raw.githubusercontent.com/jesushernanllarenageologo/Simulador_Villicum-/main/static/visor_3d/threejs/')
        html_qgis = html_qgis.replace('href="Qgis2threejs.css"', 'href="https://raw.githubusercontent.com/jesushernanllarenageologo/Simulador_Villicum-/main/static/visor_3d/Qgis2threejs.css"')
        html_qgis = html_qgis.replace('src="Qgis2threejs.js"', 'src="https://raw.githubusercontent.com/jesushernanllarenageologo/Simulador_Villicum-/main/static/visor_3d/Qgis2threejs.js"')
        html_qgis = html_qgis.replace('src="./data/scene.json"', 'src="https://raw.githubusercontent.com/jesushernanllarenageologo/Simulador_Villicum-/main/static/visor_3d/data/scene.json"')
        html_qgis = html_qgis.replace('src="videos/', 'src="https://raw.githubusercontent.com/jesushernanllarenageologo/Simulador_Villicum-/main/static/visor_3d/videos/')

        components.html(html_qgis, height=700, scrolling=True)
    else:
        st.error(f"No se encontró el visor 3D en la ruta: {ruta_visor}")