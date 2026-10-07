import streamlit as st
from pathlib import Path
import base64
import mimetypes
import json

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

    encoded = base64.b64encode(
        file_path.read_bytes()
    ).decode()

    return f"data:{mime_type};base64,{encoded}"


def buscar_archivo(carpeta: Path, extensiones):

    if not carpeta.exists():
        return None

    encontrados = []

    for archivo in carpeta.rglob("*"):

        if (
            archivo.is_file()
            and archivo.suffix.lower() in extensiones
        ):
            encontrados.append(archivo)

    if not encontrados:
        return None

    return sorted(encontrados)[0]


def buscar_por_prefijo(carpeta: Path, prefijo: str):

    if not carpeta.exists():
        return None

    for archivo in sorted(carpeta.rglob("*")):

        if (
            archivo.is_file()
            and archivo.stem.lower().startswith(
                prefijo.lower()
            )
        ):
            return archivo

    return None


def crear_tarjeta_proceso(
    titulo,
    subtitulo,
    texto,
    imagen
):

    if imagen:

        bloque_imagen = f"""
        <img
            src="{imagen}"
            class="foto-proceso"
        >
        """

    else:

        bloque_imagen = """
        <div class="placeholder-foto">
            Imagen no disponible
        </div>
        """

    return f"""
    <div class="card-proceso">

        {bloque_imagen}

        <div class="card-proceso-body">

            <div class="card-subtitle">
                {subtitulo}
            </div>

            <div class="card-title">
                {titulo}
            </div>

            <div class="card-text">
                {texto}
            </div>

        </div>

    </div>
    """


def crear_tarjeta_dique(
    identificador,
    nombre,
    subtitulo,
    imagen
):

    if imagen:

        bloque_imagen = f"""
        <img
            src="{imagen}"
            class="foto-card-dique"
        >
        """

    else:

        bloque_imagen = """
        <div class="placeholder-card-dique">
            Imagen no disponible
        </div>
        """

    return f"""
    <div class="card-dique">

        {bloque_imagen}

        <div class="card-dique-body">

            <div class="card-dique-kicker">
                APROVECHAMIENTO HIDROELÉCTRICO
            </div>

            <div class="card-dique-title">
                {nombre}
            </div>

            <div class="card-dique-text">
                {subtitulo}
            </div>

            <button
                class="btn-explorar"
                onclick="explorarDique('{identificador}')"
            >
                Explorar dique →
            </button>

        </div>

    </div>
    """


def construir_componentes(
    carpeta_componentes: Path,
    definiciones,
    coordenadas
):

    componentes = {}

    for numero, nombre in definiciones.items():

        archivo = buscar_por_prefijo(
            carpeta_componentes,
            f"{numero}_"
        )

        componentes[numero] = {

            "nombre": nombre,

            "imagen": (
                file_to_data_uri(archivo)
                if archivo
                else ""
            ),

            "texto": "",

            "x": coordenadas[numero]["x"],

            "y": coordenadas[numero]["y"]
        }

    return componentes


# ============================================================
# ESCENARIO
# ============================================================

escenario = st.session_state.get(
    "escenario_seleccionado"
)


if not escenario:

    st.warning(
        "Primero debes seleccionar un escenario."
    )

    if st.button("← Volver al simulador"):

        st.switch_page(
            "pages/1_Simulador.py"
        )

    st.stop()


# ============================================================
# POR AHORA SOLO SUPERAVITARIO
# ============================================================

if escenario != "Superavitario":

    st.title("🌊 Simulación Hídrica")

    st.markdown(
        f"### Escenario inicial: **{escenario}**"
    )

    st.info(
        f"El escenario {escenario} todavía "
        "no tiene cargada la experiencia audiovisual."
    )

    if st.button("← Volver"):

        st.switch_page(
            "pages/1_Simulador.py"
        )

    st.stop()


# ============================================================
# VIDEO 1 · CORDILLERA → MINA
# ============================================================

video_1_path = (
    BASE_DIR
    / "assets"
    / "videos"
    / "01_Cordillera_Mina"
    / "Superavitario.mp4"
)


if not video_1_path.exists():

    st.error(
        "No se encontró el video Cordillera → Mina."
    )

    st.code(str(video_1_path))

    st.stop()


# ============================================================
# VIDEO 2 · MINA → DIQUES
# ============================================================

VIDEO_2_DIR = (
    BASE_DIR
    / "assets"
    / "videos"
    / "02_Mina_Diques"
)


video_2_path = (
    VIDEO_2_DIR
    / "Mina_Diques.mp4"
)


if not video_2_path.exists():

    video_2_path = buscar_archivo(
        VIDEO_2_DIR,
        {
            ".mp4",
            ".webm",
            ".mov",
            ".m4v"
        }
    )


if video_2_path is None:

    st.error(
        "No se encontró el video Mina → Diques."
    )

    st.stop()


# ============================================================
# VIDEO 3 · CARACOLES → ULLUM
# ============================================================

video_3_path = (
    BASE_DIR
    / "assets"
    / "videos"
    / "03_Caracoles_Ullum"
    / "Caracoles_Ullum.mp4"
)


if not video_3_path.exists():

    st.error(
        "No se encontró el video Caracoles → Ullum."
    )

    st.code(str(video_3_path))

    st.stop()


# ============================================================
# IMÁGENES MINA
# ============================================================

MINA_DIR = (
    BASE_DIR
    / "assets"
    / "images"
    / "mina"
)


img_moderno_path = (
    MINA_DIR
    / "metodo_moderno_recirculacion.jpg"
)


img_tradicional_path = (
    MINA_DIR
    / "metodo_tradicional_abierto.jpg"
)


fondo_mina_path = (
    MINA_DIR
    / "fondo_mina.jpg"
)


# ============================================================
# DIQUES
# ============================================================

DIQUES_DIR = (
    BASE_DIR
    / "assets"
    / "images"
    / "Diques"
)


CARACOLES_DIR = (
    DIQUES_DIR
    / "Caracoles"
)


PUNTA_NEGRA_DIR = (
    DIQUES_DIR
    / "Punta_Negra"
)


ULLUM_DIR = (
    DIQUES_DIR
    / "Ullum"
)


# ============================================================
# IMÁGENES MENÚ
# ============================================================

caracoles_menu_path = (
    CARACOLES_DIR
    / "caracoles_menu.jpg"
)


punta_negra_menu_path = (
    PUNTA_NEGRA_DIR
    / "punta_negra_menu.jpg"
)


ullum_menu_path = (
    ULLUM_DIR
    / "ullum_menu.jpg"
)


# ============================================================
# IMÁGENES DETALLE
# ============================================================

caracoles_detalle_path = (
    CARACOLES_DIR
    / "caracoles_detalle.jpg"
)


punta_negra_detalle_path = (
    PUNTA_NEGRA_DIR
    / "punta_negra_detalle.jpg"
)


ullum_detalle_path = (
    ULLUM_DIR
    / "ullum_detalle.jpg"
)


# ============================================================
# PUNTA NEGRA
# ============================================================

PUNTA_NEGRA_COMPONENTES = {

    "01": "Obra de toma",
    "02": "Aliviadero",
    "03": "Casa de máquinas",
    "04": "Subestación",
    "05": "Descargador de fondo",
    "06": "Presa",
    "07": "Embalse"
}


HOTSPOTS_PUNTA_NEGRA = {

    "01": {"x": 60.2, "y": 58.1},
    "02": {"x": 55.6, "y": 67.1},
    "03": {"x": 61.4, "y": 86.2},
    "04": {"x": 63.6, "y": 94.0},
    "05": {"x": 31.5, "y": 83.0},
    "06": {"x": 33.8, "y": 65.2},
    "07": {"x": 38.4, "y": 45.1}
}


# ============================================================
# CARACOLES
# ============================================================

CARACOLES_COMPONENTES = {

    "01": "Embalse",
    "02": "Pantalla de hormigón",
    "03": "Coronamiento",
    "04": "Aliviadero",
    "05": "Casa de máquinas y túneles",
    "06": "Camino de acceso",
    "07": "Río San Juan"
}


HOTSPOTS_CARACOLES = {

    "01": {"x": 56.5, "y": 85.0},
    "02": {"x": 50.6, "y": 64.2},
    "03": {"x": 50.6, "y": 49.2},
    "04": {"x": 18.2, "y": 57.4},
    "05": {"x": 21.2, "y": 76.1},
    "06": {"x": 8.2,  "y": 31.1},
    "07": {"x": 41.3, "y": 9.8}
}


# ============================================================
# ULLUM
# ============================================================

ULLUM_COMPONENTES = {

    "01": "Embalse (Lago de Ullum)",
    "02": "Presa de materiales sueltos",
    "03": "Coronamiento",
    "04": "Vertedero / Aliviadero",
    "05": "Central hidroeléctrica",
    "06": "Descargador de fondo",
    "07": "Río San Juan"
}


HOTSPOTS_ULLUM = {

    "01": {"x": 16.8, "y": 12.2},
    "02": {"x": 28.8, "y": 28.0},
    "03": {"x": 39.1, "y": 13.7},
    "04": {"x": 54.8, "y": 19.7},
    "05": {"x": 63.1, "y": 32.4},
    "06": {"x": 53.3, "y": 50.7},
    "07": {"x": 41.4, "y": 76.7}
}


# ============================================================
# CREAR COMPONENTES
# ============================================================

punta_negra_componentes = construir_componentes(
    PUNTA_NEGRA_DIR / "Componentes",
    PUNTA_NEGRA_COMPONENTES,
    HOTSPOTS_PUNTA_NEGRA
)


caracoles_componentes = construir_componentes(
    CARACOLES_DIR / "Componentes",
    CARACOLES_COMPONENTES,
    HOTSPOTS_CARACOLES
)


ullum_componentes = construir_componentes(
    ULLUM_DIR / "Componentes",
    ULLUM_COMPONENTES,
    HOTSPOTS_ULLUM
)


# ============================================================
# CONVERTIR ARCHIVOS
# ============================================================

video_1_data = file_to_data_uri(
    video_1_path
)

video_2_data = file_to_data_uri(
    video_2_path
)

video_3_data = file_to_data_uri(
    video_3_path
)


img_moderno_data = file_to_data_uri(
    img_moderno_path
)

img_tradicional_data = file_to_data_uri(
    img_tradicional_path
)

fondo_mina_data = file_to_data_uri(
    fondo_mina_path
)


caracoles_menu_data = file_to_data_uri(
    caracoles_menu_path
)

punta_negra_menu_data = file_to_data_uri(
    punta_negra_menu_path
)

ullum_menu_data = file_to_data_uri(
    ullum_menu_path
)


caracoles_detalle_data = (
    file_to_data_uri(
        caracoles_detalle_path
    ) or ""
)


punta_negra_detalle_data = (
    file_to_data_uri(
        punta_negra_detalle_path
    ) or ""
)


ullum_detalle_data = (
    file_to_data_uri(
        ullum_detalle_path
    ) or ""
)


# ============================================================
# BASE DE DATOS DIQUES
# ============================================================

DIQUES_INTERACTIVOS = {

    "caracoles": {

        "nombre":
            "Complejo Hidroeléctrico Los Caracoles",

        "etiqueta":
            "LOS CARACOLES",

        "detalle":
            caracoles_detalle_data,

        "componentes":
            caracoles_componentes
    },


    "punta_negra": {

        "nombre":
            "Complejo Hidroeléctrico Punta Negra",

        "etiqueta":
            "PUNTA NEGRA",

        "detalle":
            punta_negra_detalle_data,

        "componentes":
            punta_negra_componentes
    },


    "ullum": {

        "nombre":
            "Complejo Hidroeléctrico Dique de Ullum",

        "etiqueta":
            "ULLUM",

        "detalle":
            ullum_detalle_data,

        "componentes":
            ullum_componentes
    }

}


diques_interactivos_json = json.dumps(
    DIQUES_INTERACTIVOS,
    ensure_ascii=False
)


# ============================================================
# ESTADO STREAMLIT
# ============================================================

if "experiencia_iniciada" not in st.session_state:

    st.session_state.experiencia_iniciada = False


# ============================================================
# ENCABEZADO
# ============================================================

st.title(
    "🌊 Simulación Hídrica"
)


st.markdown(
    f"### Escenario inicial: **{escenario}**"
)


# ============================================================
# PANTALLA INICIAL
# ============================================================

if not st.session_state.experiencia_iniciada:

    st.markdown(
        """
        La cuenca inicia con una **alta disponibilidad hídrica**.

        El recorrido comienza en la **Cordillera de los Andes**
        y sigue el curso del **Río San Juan** hasta la primera
        parada del simulador: **la actividad minera**.
        """
    )

    st.write("")

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        if st.button(
            "▶ INICIAR EXPERIENCIA",
            type="primary",
            use_container_width=True
        ):

            st.session_state.experiencia_iniciada = True

            st.rerun()


# ============================================================
# EXPERIENCIA
# ============================================================

else:

    # ========================================================
    # TARJETAS MINA
    # ========================================================

    tradicional_html = crear_tarjeta_proceso(

        titulo="Método tradicional abierto",

        subtitulo="MAYOR USO DE AGUA FRESCA",

        texto="""
        En un esquema con menor recuperación interna,
        una mayor cantidad del agua utilizada debe
        reemplazarse mediante nuevos aportes desde la cuenca.

        Esto incrementa el consumo neto de agua fresca.
        """,

        imagen=img_tradicional_data
    )


    moderno_html = crear_tarjeta_proceso(

        titulo="Circuito cerrado y recirculación",

        subtitulo="GESTIÓN HÍDRICA MODERNA",

        texto="""
        Mediante sistemas de recuperación,
        parte del agua utilizada puede ser captada,
        tratada y reutilizada nuevamente dentro del proceso.

        Esto reduce la necesidad de incorporar agua fresca.
        """,

        imagen=img_moderno_data
    )


    # ========================================================
    # TARJETAS DIQUES
    # ========================================================

    caracoles_html = crear_tarjeta_dique(

        identificador="caracoles",

        nombre="Los Caracoles",

        subtitulo="""
        Explorá los principales componentes
        del aprovechamiento hidroeléctrico.
        """,

        imagen=caracoles_menu_data
    )


    punta_negra_html = crear_tarjeta_dique(

        identificador="punta_negra",

        nombre="Punta Negra",

        subtitulo="""
        Explorá sus principales componentes
        y cómo se distribuyen dentro del complejo.
        """,

        imagen=punta_negra_menu_data
    )


    ullum_html = crear_tarjeta_dique(

        identificador="ullum",

        nombre="Quebrada de Ullum",

        subtitulo="""
        Explorá la presa, el embalse
        y las principales obras hidráulicas.
        """,

        imagen=ullum_menu_data
    )


    # ========================================================
    # FONDO MINA
    # ========================================================

    if fondo_mina_data:

        fondo_css = f"""
        linear-gradient(
            90deg,
            rgba(0,0,0,0.48) 0%,
            rgba(0,0,0,0.34) 48%,
            rgba(0,0,0,0.20) 100%
        ),
        url("{fondo_mina_data}")
        """

    else:

        fondo_css = """
        linear-gradient(
            135deg,
            #28343b,
            #50616a
        )
        """


    # ========================================================
    # HTML
    # ========================================================

    html_template = """

<style>


/* =========================================================
   GENERAL
========================================================= */

body {

    margin: 0;

    background: #0d1820;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

}


.experiencia {

    width: 100%;

    height: 900px;

    position: relative;

    overflow: hidden;

    border-radius: 18px;

    background: #0d1820;

}


/* =========================================================
   PANTALLAS
========================================================= */

.pantalla-contenido {

    display: none;

    width: 100%;

    height: 900px;

    box-sizing: border-box;

    padding:
        35px 38px;

    color: white;

    overflow-y: auto;

}


.pantalla-mina {

    background:
        __FONDO_MINA__;

    background-size: cover;

    background-position: center;

}


/* =========================================================
   VIDEOS
========================================================= */

.pantalla-video {

    width: 100%;

    height: 900px;

    position: relative;

    overflow: hidden;

    background: black;

}


.video-recorrido {

    position: absolute;

    inset: 0;

    width: 100%;

    height: 100%;

    object-fit: cover;

    object-position: center;

}


.etiqueta-video {

    position: absolute;

    top: 28px;

    left: 30px;

    padding:
        12px 18px;

    border-radius: 12px;

    color: white;

    background:
        rgba(0,0,0,0.48);

    border:
        1px solid
        rgba(255,255,255,0.20);

    backdrop-filter:
        blur(8px);

    font-size: 17px;

    font-weight: 700;

}


/* =========================================================
   TÍTULOS
========================================================= */

.titulo-etapa {

    font-size: 13px;

    letter-spacing: 2.2px;

    color: #64d6df;

    font-weight: 800;

    margin-bottom: 9px;

}


.titulo-principal {

    font-size: 40px;

    line-height: 1.1;

    font-weight: 800;

    margin-bottom: 14px;

}


.descripcion {

    max-width: 1050px;

    font-size: 16px;

    line-height: 1.55;

    margin-bottom: 20px;

}


/* =========================================================
   BOTONES
========================================================= */

.botones-navegacion {

    display: flex;

    justify-content: center;

    gap: 13px;

    flex-wrap: wrap;

    margin-top: 22px;

}


.btn-principal,
.btn-secundario {

    border:
        1px solid
        rgba(255,255,255,0.25);

    border-radius: 12px;

    padding:
        14px 22px;

    color: white;

    font-size: 15px;

    font-weight: 700;

    cursor: pointer;

    transition: 0.2s;

}


.btn-principal {

    background:
        #169cad;

}


.btn-principal:hover {

    background:
        #22b6c8;

    transform:
        translateY(-2px);

}


.btn-secundario {

    background:
        rgba(7,20,28,0.62);

}


/* =========================================================
   TARJETAS MINA
========================================================= */

.grid-procesos {

    display: grid;

    grid-template-columns:
        repeat(2,1fr);

    gap: 18px;

}


.card-proceso {

    overflow: hidden;

    border-radius: 17px;

    background:
        rgba(10,22,28,0.60);

    border:
        1px solid
        rgba(255,255,255,0.18);

}


.foto-proceso {

    width: 100%;

    height: 195px;

    object-fit: cover;

}


.card-proceso-body {

    padding: 17px 19px;

}


.card-subtitle {

    color: #66d6df;

    font-size: 11px;

    letter-spacing: 1.5px;

    font-weight: 800;

}


.card-title {

    font-size: 22px;

    font-weight: 800;

    margin:
        5px 0 9px;

}


.card-text {

    font-size: 14px;

    line-height: 1.5;

}


.info-clave {

    margin-top: 17px;

    padding:
        15px 18px;

    border-radius: 13px;

    background:
        rgba(5,20,27,0.55);

    border:
        1px solid
        rgba(99,211,222,0.36);

}


/* =========================================================
   DECISIÓN MINA
========================================================= */

.pregunta {

    font-size: 24px;

    font-weight: 800;

    margin:
        27px 0 18px;

}


.opciones {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 15px;

}


.opcion {

    padding: 22px;

    color: white;

    text-align: left;

    cursor: pointer;

    border-radius: 16px;

    background:
        rgba(7,20,28,0.62);

    border:
        1px solid
        rgba(255,255,255,0.22);

}


.opcion strong {

    display: block;

    margin-bottom: 8px;

    font-size: 18px;

}


.opcion span {

    font-size: 14px;

    line-height: 1.45;

}


/* =========================================================
   RESULTADO MINA
========================================================= */

.resultado-grid {

    display: grid;

    grid-template-columns:
        0.85fr 1.15fr;

    gap: 35px;

    align-items: center;

}


.donut-wrapper {

    display: flex;

    justify-content: center;

}


.donut {

    width: 300px;

    height: 300px;

    border-radius: 50%;

    position: relative;

    display: flex;

    justify-content: center;

    align-items: center;

    background:
        conic-gradient(
            #e5a13a
            0%
            calc(var(--consumo) * 1%),

            #42bfd0
            calc(var(--consumo) * 1%)
            100%
        );

}


.donut::before {

    content: "";

    width: 195px;

    height: 195px;

    position: absolute;

    border-radius: 50%;

    background:
        #071921;

}


.donut-centro {

    position: relative;

    z-index: 2;

    text-align: center;

}


.donut-numero {

    font-size: 50px;

    font-weight: 800;

}


.donut-texto {

    max-width: 140px;

    font-size: 14px;

    color: #cce8ed;

}


.metricas {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 11px;

    margin-bottom: 15px;

}


.metrica {

    padding: 17px;

    border-radius: 13px;

    background:
        rgba(7,20,28,0.60);

    border:
        1px solid
        rgba(255,255,255,0.15);

}


.metrica-numero {

    font-size: 28px;

    font-weight: 800;

}


.metrica-label {

    margin-top: 4px;

    font-size: 12px;

    color: #c8dce1;

}


.resultado-explicacion,
.modelo-educativo {

    padding: 18px;

    border-radius: 14px;

    background:
        rgba(7,20,28,0.58);

    border:
        1px solid
        rgba(255,255,255,0.16);

    line-height: 1.55;

}


.modelo-educativo {

    margin-top: 14px;

    font-size: 12px;

}


/* =========================================================
   MENÚ DIQUES
========================================================= */

#menu-diques {

    background:
        linear-gradient(
            135deg,
            #071925,
            #0c3547,
            #10556b
        );

}


.recorrido-diques {

    display: flex;

    justify-content: center;

    align-items: center;

    gap: 10px;

    flex-wrap: wrap;

    padding: 12px;

    margin:
        7px 0 24px;

    border-radius: 13px;

    background:
        rgba(255,255,255,0.06);

}


.nodo-recorrido {

    font-size: 13px;

    font-weight: 700;

}


.flecha-recorrido {

    color: #64d6df;

}


.grid-diques {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 16px;

}


.card-dique {

    overflow: hidden;

    border-radius: 17px;

    background:
        rgba(4,18,27,0.67);

    border:
        1px solid
        rgba(255,255,255,0.16);

}


.foto-card-dique {

    width: 100%;

    height: 205px;

    object-fit: cover;

}


.card-dique-body {

    padding: 17px;

}


.card-dique-kicker {

    font-size: 10px;

    color: #65d7df;

    letter-spacing: 1.4px;

    font-weight: 800;

}


.card-dique-title {

    margin:
        5px 0 7px;

    font-size: 22px;

    font-weight: 800;

}


.card-dique-text {

    min-height: 43px;

    color: #dbe8eb;

    font-size: 13px;

    line-height: 1.45;

}


.btn-explorar {

    width: 100%;

    margin-top: 14px;

    padding: 12px;

    border: 0;

    border-radius: 10px;

    color: white;

    background: #169cad;

    font-weight: 700;

    cursor: pointer;

}


/* =========================================================
   EXPLORADOR
========================================================= */

#explorador-dique {

    background:
        linear-gradient(
            135deg,
            #071720,
            #0b303f
        );

}


.explorador-top {

    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    gap: 15px;

}


.guia-explorador {

    padding:
        10px 14px;

    margin-bottom: 16px;

    border-radius: 11px;

    background:
        rgba(255,255,255,0.06);

}


.explorador-grid {

    display: grid;

    grid-template-columns:
        minmax(0,1.55fr)
        minmax(275px,0.65fr);

    gap: 17px;

    align-items: start;

}


.mapa-hotspots {

    position: relative;

    overflow: hidden;

    width: 100%;

    border-radius: 16px;

    background: black;

}


.img-detalle {

    display: block;

    width: 100%;

    height: auto;

}


.hotspot {

    position: absolute;

    width: 44px;

    height: 44px;

    transform:
        translate(-50%,-50%);

    border-radius: 50%;

    border:
        2px solid white;

    color: white;

    background:
        rgba(3,20,28,0.78);

    font-weight: 800;

    cursor: pointer;

    z-index: 5;

}


.hotspot.activo {

    background:
        #2cc2d1;

    box-shadow:
        0 0 0 6px
        rgba(44,194,209,0.19);

}


.panel-componente {

    min-height: 515px;

    overflow: hidden;

    border-radius: 16px;

    background:
        rgba(255,255,255,0.07);

    border:
        1px solid
        rgba(255,255,255,0.14);

}


.panel-inicial {

    min-height: 515px;

    box-sizing: border-box;

    padding: 30px;

    display: flex;

    justify-content: center;

    align-items: center;

    flex-direction: column;

    text-align: center;

}


.panel-activo {

    display: none;

}


.imagen-componente {

    width: 100%;

    height: 235px;

    object-fit: cover;

}


.numero-componente {

    margin:
        19px 20px 4px;

    color: #64d6df;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.5px;

}


.titulo-componente {

    margin:
        0 20px;

    font-size: 23px;

    font-weight: 800;

}


.texto-componente {

    margin:
        15px 20px;

    padding-top: 15px;

    min-height: 90px;

    border-top:
        1px solid
        rgba(255,255,255,0.10);

}


/* =========================================================
   ULLUM · PANTALLA INFORMATIVA
========================================================= */

#info-ullum {

    background:
        radial-gradient(
            circle at 50% 45%,
            #17465a 0%,
            #0b2735 48%,
            #061720 100%
        );

}


.rueda-wrapper {

    display: grid;

    grid-template-columns:
        1fr 1.15fr;

    gap: 35px;

    align-items: center;

    margin-top: 25px;

}


.rueda {

    position: relative;

    width: 470px;

    height: 470px;

    max-width: 100%;

    margin: auto;

}


.rueda-centro {

    position: absolute;

    left: 50%;

    top: 50%;

    transform:
        translate(-50%,-50%);

    width: 155px;

    height: 155px;

    border-radius: 50%;

    display: flex;

    justify-content: center;

    align-items: center;

    text-align: center;

    box-sizing: border-box;

    padding: 20px;

    background:
        linear-gradient(
            135deg,
            #168fa2,
            #1eb6c8
        );

    border:
        5px solid
        rgba(255,255,255,0.18);

    box-shadow:
        0 0 0 12px
        rgba(35,193,207,0.08);

    font-size: 20px;

    font-weight: 800;

}


.rueda-btn {

    position: absolute;

    width: 150px;

    min-height: 82px;

    padding: 13px;

    border-radius: 15px;

    color: white;

    background:
        rgba(5,22,30,0.82);

    border:
        1px solid
        rgba(255,255,255,0.20);

    cursor: pointer;

    font-weight: 700;

    transition: 0.2s;

}


.rueda-btn:hover,
.rueda-btn.activo {

    background:
        #168fa2;

    transform:
        scale(1.04);

}


.rueda-top {

    top: 0;

    left: 50%;

    transform:
        translateX(-50%);

}


.rueda-bottom {

    bottom: 0;

    left: 50%;

    transform:
        translateX(-50%);

}


.rueda-left {

    left: 0;

    top: 50%;

    transform:
        translateY(-50%);

}


.rueda-right {

    right: 0;

    top: 50%;

    transform:
        translateY(-50%);

}


.panel-info-ullum {

    min-height: 360px;

    box-sizing: border-box;

    padding: 30px;

    border-radius: 18px;

    background:
        rgba(255,255,255,0.07);

    border:
        1px solid
        rgba(255,255,255,0.15);

}


.info-icono {

    font-size: 45px;

}


.info-titulo {

    margin:
        10px 0;

    font-size: 29px;

    font-weight: 800;

}


.info-texto {

    color: #d7e7ea;

    font-size: 16px;

    line-height: 1.6;

}


/* =========================================================
   DECISIÓN ULLUM
========================================================= */

#decision-ullum {

    background:
        linear-gradient(
            135deg,
            #08202b,
            #0e3e50
        );

}


.opciones-ullum {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 17px;

    margin-top: 28px;

}


.opcion-ullum {

    min-height: 230px;

    padding: 24px;

    box-sizing: border-box;

    text-align: left;

    border-radius: 18px;

    color: white;

    background:
        rgba(5,20,28,0.68);

    border:
        1px solid
        rgba(255,255,255,0.18);

    cursor: pointer;

    transition: 0.2s;

}


.opcion-ullum:hover {

    transform:
        translateY(-5px);

    border-color:
        #55d1dd;

}


.opcion-icono {

    font-size: 34px;

}


.opcion-titulo {

    margin:
        11px 0 8px;

    font-size: 21px;

    font-weight: 800;

}


.opcion-desc {

    font-size: 14px;

    line-height: 1.5;

    color: #d7e5e9;

}


.opcion-dato {

    margin-top: 18px;

    padding-top: 13px;

    border-top:
        1px solid
        rgba(255,255,255,0.12);

    color: #65d6df;

    font-weight: 700;

}


/* =========================================================
   RESULTADO ULLUM
========================================================= */

#resultado-ullum {

    background:
        linear-gradient(
            135deg,
            #061923,
            #0b3546
        );

}


.resultado-ullum-grid {

    display: grid;

    grid-template-columns:
        0.85fr 1.15fr;

    gap: 40px;

    align-items: center;

    margin-top: 30px;

}


.donut-ullum {

    width: 315px;

    height: 315px;

    margin: auto;

    position: relative;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        conic-gradient(
            #33bccb
            0%
            calc(var(--reserva) * 1%),

            #e5a13a
            calc(var(--reserva) * 1%)
            100%
        );

}


.donut-ullum::before {

    content: "";

    position: absolute;

    width: 205px;

    height: 205px;

    border-radius: 50%;

    background:
        #071b24;

}


.donut-ullum-centro {

    position: relative;

    z-index: 2;

    text-align: center;

}


.reserva-numero {

    font-size: 51px;

    font-weight: 800;

}


.reserva-label {

    width: 135px;

    font-size: 14px;

    color: #cbe6ea;

}


.leyenda-donut {

    display: flex;

    justify-content: center;

    gap: 18px;

    margin-top: 17px;

    font-size: 13px;

}


.punto-reserva,
.punto-liberado {

    display: inline-block;

    width: 10px;

    height: 10px;

    margin-right: 5px;

    border-radius: 50%;

}


.punto-reserva {

    background:
        #33bccb;

}


.punto-liberado {

    background:
        #e5a13a;

}


.metricas-ullum {

    display: grid;

    grid-template-columns:
        repeat(2,1fr);

    gap: 12px;

}


.metrica-ullum {

    padding: 19px;

    border-radius: 14px;

    background:
        rgba(5,20,28,0.65);

    border:
        1px solid
        rgba(255,255,255,0.15);

}


.metrica-ullum-numero {

    font-size: 27px;

    font-weight: 800;

}


.metrica-ullum-label {

    margin-top: 4px;

    font-size: 12px;

    color: #c8dce1;

}


.resultado-ullum-texto {

    margin-top: 15px;

    padding: 18px;

    border-radius: 14px;

    line-height: 1.55;

    background:
        rgba(5,20,28,0.62);

    border:
        1px solid
        rgba(255,255,255,0.15);

}


.aviso-modelo {

    margin-top: 13px;

    font-size: 12px;

    color: #c6dadd;

}


/* =========================================================
   SIGUIENTE ETAPA
========================================================= */

#aviso-distribuidor {

    display: none;

    margin-top: 16px;

    padding: 16px;

    border-radius: 13px;

    text-align: center;

    background:
        rgba(70,201,213,0.12);

    border:
        1px solid
        rgba(70,201,213,0.35);

}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {

    .grid-procesos,
    .opciones,
    .resultado-grid,
    .grid-diques,
    .explorador-grid,
    .rueda-wrapper,
    .opciones-ullum,
    .resultado-ullum-grid {

        grid-template-columns: 1fr;

    }


    .metricas,
    .metricas-ullum {

        grid-template-columns: 1fr;

    }


    .rueda {

        transform:
            scale(0.85);

    }

}

</style>



<div class="experiencia">


<!-- =====================================================
     VIDEO 1
===================================================== -->

<div
    id="video-1-screen"
    class="pantalla-video"
>

    <video
        id="video-1"
        class="video-recorrido"
        autoplay
        muted
        playsinline
        src="__VIDEO_1__"
    ></video>

    <div class="etiqueta-video">
        🏔️ Cordillera → Mina
    </div>

</div>



<!-- =====================================================
     INFO MINA
===================================================== -->

<div
    id="info-mina"
    class="pantalla-contenido pantalla-mina"
>

    <div class="titulo-etapa">
        PARADA 1 · CUENCA ALTA
    </div>

    <div class="titulo-principal">
        ⛏️ Gestión del agua en la actividad minera
    </div>

    <div class="descripcion">

        Antes de tomar una decisión,
        observá cómo distintas formas de gestión
        modifican el consumo neto de agua.

    </div>

    <div class="grid-procesos">

        __TRADICIONAL__

        __MODERNO__

    </div>

    <div class="info-clave">

        <strong>💡 Concepto clave:</strong>

        una mayor recuperación y recirculación
        reduce la necesidad de incorporar agua fresca.

    </div>

    <div class="botones-navegacion">

        <button
            class="btn-secundario"
            onclick="reproducirVideo1()"
        >
            ↻ Reproducir recorrido
        </button>

        <button
            class="btn-principal"
            onclick="mostrarDecisionMina()"
        >
            Continuar a la decisión →
        </button>

    </div>

</div>



<!-- =====================================================
     DECISIÓN MINA
===================================================== -->

<div
    id="decision-mina"
    class="pantalla-contenido pantalla-mina"
>

    <div class="titulo-etapa">
        PARADA 1 · DECISIÓN
    </div>

    <div class="titulo-principal">
        ♻️ ¿Cómo gestionarías el agua?
    </div>

    <div class="descripcion">

        Para este modelo educativo,
        el proceso requiere un volumen
        equivalente al 25 % del caudal inicial.

    </div>

    <div class="pregunta">
        Seleccioná una estrategia
    </div>

    <div class="opciones">

        <button
            class="opcion"
            onclick="seleccionarDecisionMina('alta')"
        >

            <strong>
                ♻️ Alta recirculación · 80 %
            </strong>

            <span>
                Consumo neto aproximado: 5 %.
            </span>

        </button>


        <button
            class="opcion"
            onclick="seleccionarDecisionMina('media')"
        >

            <strong>
                ⚖️ Recirculación intermedia · 60 %
            </strong>

            <span>
                Consumo neto aproximado: 10 %.
            </span>

        </button>


        <button
            class="opcion"
            onclick="seleccionarDecisionMina('nula')"
        >

            <strong>
                💧 Sin recirculación · 0 %
            </strong>

            <span>
                Consumo neto aproximado: 25 %.
            </span>

        </button>

    </div>

</div>



<!-- =====================================================
     RESULTADO MINA
===================================================== -->

<div
    id="resultado-mina"
    class="pantalla-contenido pantalla-mina"
>

    <div class="titulo-etapa">
        RESULTADO · PARADA 1
    </div>

    <div class="titulo-principal">
        📊 Impacto de tu decisión
    </div>

    <div class="descripcion">

        Elegiste:

        <strong id="resultado-titulo">
            -
        </strong>

    </div>


    <div class="resultado-grid">

        <div>

            <div class="donut-wrapper">

                <div
                    id="donut"
                    class="donut"
                    style="--consumo:5;"
                >

                    <div class="donut-centro">

                        <div
                            id="donut-restante"
                            class="donut-numero"
                        >
                            95%
                        </div>

                        <div class="donut-texto">
                            continúa disponible aguas abajo
                        </div>

                    </div>

                </div>

            </div>

        </div>


        <div>

            <div class="metricas">

                <div class="metrica">

                    <div
                        id="metrica-recirculacion"
                        class="metrica-numero"
                    >
                        80%
                    </div>

                    <div class="metrica-label">
                        Recirculación
                    </div>

                </div>


                <div class="metrica">

                    <div
                        id="metrica-consumo"
                        class="metrica-numero"
                    >
                        -5%
                    </div>

                    <div class="metrica-label">
                        Consumo neto
                    </div>

                </div>


                <div class="metrica">

                    <div
                        id="metrica-restante"
                        class="metrica-numero"
                    >
                        95%
                    </div>

                    <div class="metrica-label">
                        Caudal disponible
                    </div>

                </div>

            </div>


            <div class="resultado-explicacion">

                El consumo neto de esta etapa
                representa aproximadamente

                <strong id="texto-consumo">
                    5 %
                </strong>.

                <br><br>

                Continúa disponible aproximadamente

                <strong id="texto-restante">
                    95 %
                </strong>

                para seguir hacia el sistema de embalses.

            </div>


            <div class="modelo-educativo">

                ℹ️ Modelo educativo simplificado.

            </div>

        </div>

    </div>


    <div class="botones-navegacion">

        <button
            class="btn-secundario"
            onclick="mostrarDecisionMina()"
        >
            ← Cambiar decisión
        </button>

        <button
            class="btn-principal"
            onclick="reproducirVideo2()"
        >
            Continuar hacia los diques →
        </button>

    </div>

</div>



<!-- =====================================================
     VIDEO 2
===================================================== -->

<div
    id="video-2-screen"
    class="pantalla-video"
    style="display:none;"
>

    <video
        id="video-2"
        class="video-recorrido"
        muted
        playsinline
        src="__VIDEO_2__"
    ></video>

    <div class="etiqueta-video">
        🌊 Mina → Los Caracoles
    </div>

</div>



<!-- =====================================================
     MENÚ DIQUES
===================================================== -->

<div
    id="menu-diques"
    class="pantalla-contenido"
>

    <div class="titulo-etapa">
        SISTEMA DE EMBALSES
    </div>

    <div class="titulo-principal">
        🏞️ Regulación del Río San Juan
    </div>

    <div class="descripcion">

        Antes de continuar, podés explorar
        los tres principales aprovechamientos
        del sistema.

    </div>


    <div class="recorrido-diques">

        <span class="nodo-recorrido">
            🏔 Cordillera
        </span>

        <span class="flecha-recorrido">→</span>

        <span class="nodo-recorrido">
            Los Caracoles
        </span>

        <span class="flecha-recorrido">→</span>

        <span class="nodo-recorrido">
            Punta Negra
        </span>

        <span class="flecha-recorrido">→</span>

        <span class="nodo-recorrido">
            Ullum
        </span>

        <span class="flecha-recorrido">→</span>

        <span class="nodo-recorrido">
            🌾 Cuenca baja
        </span>

    </div>


    <div class="grid-diques">

        __CARACOLES__

        __PUNTA_NEGRA__

        __ULLUM__

    </div>


    <div class="botones-navegacion">

        <button
            class="btn-secundario"
            onclick="reproducirVideo2()"
        >
            ↻ Reproducir recorrido
        </button>

        <button
            class="btn-principal"
            onclick="reproducirVideo3()"
        >
            Continuar hacia Ullum →
        </button>

    </div>

</div>



<!-- =====================================================
     EXPLORADOR DIQUES
===================================================== -->

<div
    id="explorador-dique"
    class="pantalla-contenido"
>

    <div class="explorador-top">

        <div>

            <div
                id="explorador-etiqueta"
                class="titulo-etapa"
            >
                EXPLORADOR
            </div>

            <div
                id="explorador-titulo"
                class="titulo-principal"
            >
            </div>

        </div>

        <button
            class="btn-secundario"
            onclick="mostrarMenuDiques()"
        >
            ← Volver a los diques
        </button>

    </div>


    <div class="guia-explorador">

        Seleccioná uno de los puntos numerados
        para conocer cada componente.

    </div>


    <div class="explorador-grid">

        <div class="mapa-hotspots">

            <img
                id="imagen-detalle-dique"
                class="img-detalle"
                src=""
            >

            <div id="contenedor-hotspots">
            </div>

        </div>


        <div class="panel-componente">


            <div
                id="panel-inicial"
                class="panel-inicial"
            >

                <div style="font-size:48px;">
                    ◎
                </div>

                <strong>
                    Explorá el aprovechamiento
                </strong>

                <br>

                Tocá uno de los círculos numerados.

            </div>


            <div
                id="panel-activo"
                class="panel-activo"
            >

                <img
                    id="imagen-componente"
                    class="imagen-componente"
                    src=""
                >

                <div
                    id="numero-componente"
                    class="numero-componente"
                >
                </div>

                <div
                    id="titulo-componente"
                    class="titulo-componente"
                >
                </div>

                <div
                    id="texto-componente"
                    class="texto-componente"
                >
                </div>

            </div>

        </div>

    </div>

</div>



<!-- =====================================================
     VIDEO 3 · CARACOLES → ULLUM
===================================================== -->

<div
    id="video-3-screen"
    class="pantalla-video"
    style="display:none;"
>

    <video
        id="video-3"
        class="video-recorrido"
        muted
        playsinline
        src="__VIDEO_3__"
    ></video>

    <div class="etiqueta-video">
        🌊 Los Caracoles → Ullum
    </div>

</div>



<!-- =====================================================
     PARADA ULLUM · RUEDA INFORMATIVA
===================================================== -->

<div
    id="info-ullum"
    class="pantalla-contenido"
>

    <div class="titulo-etapa">
        PARADA 2 · DIQUE DE ULLUM
    </div>

    <div class="titulo-principal">
        💧 Gestión del último embalse
    </div>

    <div class="descripcion">

        Ullum representa el último gran punto
        de regulación antes de que el Río San Juan
        continúe hacia la cuenca baja.

        Explorá los factores que intervienen
        antes de tomar una decisión.

    </div>


    <div class="rueda-wrapper">


        <div class="rueda">


            <button
                class="rueda-btn rueda-top"
                data-info="reserva"
                onclick="mostrarInfoUllum('reserva')"
            >
                💧 Reserva
                <br>
                del embalse
            </button>


            <button
                class="rueda-btn rueda-left"
                data-info="energia"
                onclick="mostrarInfoUllum('energia')"
            >
                ⚡ Generación
                <br>
                hidroeléctrica
            </button>


            <div class="rueda-centro">

                DIQUE
                <br>
                DE ULLUM

            </div>


            <button
                class="rueda-btn rueda-right"
                data-info="caudal"
                onclick="mostrarInfoUllum('caudal')"
            >
                🌊 Caudal
                <br>
                aguas abajo
            </button>


            <button
                class="rueda-btn rueda-bottom"
                data-info="demanda"
                onclick="mostrarInfoUllum('demanda')"
            >
                🌾 Demanda
                <br>
                cuenca baja
            </button>


        </div>


        <div class="panel-info-ullum">

            <div
                id="info-ullum-icono"
                class="info-icono"
            >
                ◎
            </div>

            <div
                id="info-ullum-titulo"
                class="info-titulo"
            >
                ¿Qué debemos considerar?
            </div>

            <div
                id="info-ullum-texto"
                class="info-texto"
            >

                Seleccioná uno de los cuatro factores
                para conocer cómo interviene
                en la operación del embalse.

            </div>

        </div>


    </div>


    <div class="botones-navegacion">

        <button
            class="btn-secundario"
            onclick="reproducirVideo3()"
        >
            ↻ Reproducir Caracoles → Ullum
        </button>

        <button
            class="btn-principal"
            onclick="mostrarDecisionUllum()"
        >
            Tomar decisión →
        </button>

    </div>

</div>



<!-- =====================================================
     DECISIÓN ULLUM
===================================================== -->

<div
    id="decision-ullum"
    class="pantalla-contenido"
>

    <div class="titulo-etapa">
        PARADA 2 · DECISIÓN
    </div>

    <div class="titulo-principal">
        🏞️ ¿Cómo administrarías la liberación?
    </div>

    <div class="descripcion">

        La liberación modifica la reserva disponible,
        el caudal que continúa hacia la cuenca baja
        y la generación hidroeléctrica.

    </div>


    <div class="opciones-ullum">


        <button
            class="opcion-ullum"
            onclick="seleccionarDecisionUllum('reserva')"
        >

            <div class="opcion-icono">
                💧
            </div>

            <div class="opcion-titulo">
                Conservar reservas
            </div>

            <div class="opcion-desc">

                Reducir la liberación para conservar
                una mayor proporción del agua almacenada.

            </div>

            <div class="opcion-dato">
                Liberación relativa: 24
            </div>

        </button>



        <button
            class="opcion-ullum"
            onclick="seleccionarDecisionUllum('equilibrada')"
        >

            <div class="opcion-icono">
                ⚖️
            </div>

            <div class="opcion-titulo">
                Gestión equilibrada
            </div>

            <div class="opcion-desc">

                Mantener un equilibrio entre reserva,
                generación y entrega hacia aguas abajo.

            </div>

            <div class="opcion-dato">
                Liberación relativa: 30
            </div>

        </button>



        <button
            class="opcion-ullum"
            onclick="seleccionarDecisionUllum('liberacion')"
        >

            <div class="opcion-icono">
                ⚡
            </div>

            <div class="opcion-titulo">
                Mayor liberación
            </div>

            <div class="opcion-desc">

                Aumentar temporalmente el agua
                entregada hacia la cuenca baja.

            </div>

            <div class="opcion-dato">
                Liberación relativa: 36
            </div>

        </button>


    </div>


    <div class="botones-navegacion">

        <button
            class="btn-secundario"
            onclick="mostrarInfoUllumPantalla()"
        >
            ← Volver a la información
        </button>

    </div>

</div>



<!-- =====================================================
     RESULTADO ULLUM
===================================================== -->

<div
    id="resultado-ullum"
    class="pantalla-contenido"
>

    <div class="titulo-etapa">
        RESULTADO · PARADA 2
    </div>

    <div class="titulo-principal">
        📊 Gestión del embalse
    </div>

    <div class="descripcion">

        Estrategia seleccionada:

        <strong id="estrategia-ullum">
            -
        </strong>

    </div>


    <div class="resultado-ullum-grid">


        <div>


            <div
                id="donut-ullum"
                class="donut-ullum"
                style="--reserva:70;"
            >

                <div class="donut-ullum-centro">

                    <div
                        id="reserva-numero"
                        class="reserva-numero"
                    >
                        70%
                    </div>

                    <div class="reserva-label">
                        reserva relativa
                    </div>

                </div>

            </div>


            <div class="leyenda-donut">

                <span>
                    <span class="punto-reserva"></span>
                    Reserva
                </span>

                <span>
                    <span class="punto-liberado"></span>
                    Liberación
                </span>

            </div>


        </div>



        <div>


            <div class="metricas-ullum">


                <div class="metrica-ullum">

                    <div
                        id="caudal-ullum"
                        class="metrica-ullum-numero"
                    >
                        30
                    </div>

                    <div class="metrica-ullum-label">
                        Liberación relativa
                    </div>

                </div>


                <div class="metrica-ullum">

                    <div
                        id="energia-ullum"
                        class="metrica-ullum-numero"
                    >
                        Media
                    </div>

                    <div class="metrica-ullum-label">
                        Generación
                    </div>

                </div>


                <div class="metrica-ullum">

                    <div
                        id="estado-reserva-ullum"
                        class="metrica-ullum-numero"
                    >
                        Estable
                    </div>

                    <div class="metrica-ullum-label">
                        Reserva
                    </div>

                </div>


                <div class="metrica-ullum">

                    <div
                        class="metrica-ullum-numero"
                    >
                        Cuenca baja
                    </div>

                    <div class="metrica-ullum-label">
                        Próximo destino
                    </div>

                </div>


            </div>


            <div
                id="resultado-ullum-texto"
                class="resultado-ullum-texto"
            >
            </div>


            <div class="aviso-modelo">

                ℹ️ Los valores 24, 30 y 36 forman parte
                de un modelo educativo normalizado
                para visualizar diferentes estrategias
                de regulación. No representan una operación
                real específica del Dique de Ullum.

            </div>


        </div>


    </div>


    <div class="botones-navegacion">

        <button
            class="btn-secundario"
            onclick="mostrarDecisionUllum()"
        >
            ← Cambiar decisión
        </button>

        <button
            class="btn-principal"
            onclick="continuarDistribuidor()"
        >
            Continuar hacia el distribuidor →
        </button>

    </div>


    <div
        id="aviso-distribuidor"
    >

        ✅ Decisión guardada dentro de esta simulación.

        <br><br>

        El próximo paso será conectar esta elección
        con el video correspondiente:

        <strong id="video-siguiente">
        </strong>

    </div>

</div>


</div>



<script>


// ==========================================================
// DATOS DIQUES
// ==========================================================

const diquesInteractivos =
    __DIQUES_INTERACTIVOS__;


// ==========================================================
// ESTADO GENERAL
// ==========================================================

let diqueActual = null;

let decisionMina = null;

let decisionUllum = null;

let recirculacionActual = 0;

let consumoActual = 0;

let restanteActual = 100;


// ==========================================================
// PANTALLAS
// ==========================================================

const pantallas = [

    "video-1-screen",

    "info-mina",

    "decision-mina",

    "resultado-mina",

    "video-2-screen",

    "menu-diques",

    "explorador-dique",

    "video-3-screen",

    "info-ullum",

    "decision-ullum",

    "resultado-ullum"

];


function ocultarTodo() {

    pantallas.forEach(
        function(id) {

            const elemento =
                document.getElementById(id);

            if (elemento) {

                elemento.style.display =
                    "none";

            }

        }
    );

}


// ==========================================================
// VIDEOS
// ==========================================================

const video1 =
    document.getElementById("video-1");

const video2 =
    document.getElementById("video-2");

const video3 =
    document.getElementById("video-3");


// ==========================================================
// VIDEO 1
// ==========================================================

function reproducirVideo1() {

    ocultarTodo();

    document.getElementById(
        "video-1-screen"
    ).style.display =
        "block";

    video1.currentTime = 0;

    video1.play();

}


video1.addEventListener(
    "ended",
    mostrarInfoMina
);


// ==========================================================
// INFO MINA
// ==========================================================

function mostrarInfoMina() {

    ocultarTodo();

    document.getElementById(
        "info-mina"
    ).style.display =
        "block";

}


// ==========================================================
// DECISIÓN MINA
// ==========================================================

function mostrarDecisionMina() {

    ocultarTodo();

    document.getElementById(
        "decision-mina"
    ).style.display =
        "block";

}


function seleccionarDecisionMina(tipo) {


    if (tipo === "alta") {

        decisionMina =
            "Alta recirculación";

        recirculacionActual = 80;

        consumoActual = 5;

        restanteActual = 95;

    }


    else if (tipo === "media") {

        decisionMina =
            "Recirculación intermedia";

        recirculacionActual = 60;

        consumoActual = 10;

        restanteActual = 90;

    }


    else {

        decisionMina =
            "Sin recirculación";

        recirculacionActual = 0;

        consumoActual = 25;

        restanteActual = 75;

    }


    document.getElementById(
        "resultado-titulo"
    ).textContent =
        decisionMina;


    document.getElementById(
        "donut"
    ).style.setProperty(
        "--consumo",
        consumoActual
    );


    document.getElementById(
        "donut-restante"
    ).textContent =
        restanteActual + "%";


    document.getElementById(
        "metrica-recirculacion"
    ).textContent =
        recirculacionActual + "%";


    document.getElementById(
        "metrica-consumo"
    ).textContent =
        "-" + consumoActual + "%";


    document.getElementById(
        "metrica-restante"
    ).textContent =
        restanteActual + "%";


    document.getElementById(
        "texto-consumo"
    ).textContent =
        consumoActual + " %";


    document.getElementById(
        "texto-restante"
    ).textContent =
        restanteActual + " %";


    ocultarTodo();

    document.getElementById(
        "resultado-mina"
    ).style.display =
        "block";

}


// ==========================================================
// VIDEO 2
// ==========================================================

function reproducirVideo2() {

    ocultarTodo();

    document.getElementById(
        "video-2-screen"
    ).style.display =
        "block";

    video2.currentTime = 0;

    video2.play();

}


video2.addEventListener(
    "ended",
    mostrarMenuDiques
);


// ==========================================================
// MENÚ DIQUES
// ==========================================================

function mostrarMenuDiques() {

    ocultarTodo();

    document.getElementById(
        "menu-diques"
    ).style.display =
        "block";

}


// ==========================================================
// EXPLORADOR
// ==========================================================

function explorarDique(clave) {


    const dique =
        diquesInteractivos[clave];


    if (!dique) {
        return;
    }


    diqueActual = clave;


    ocultarTodo();


    document.getElementById(
        "explorador-dique"
    ).style.display =
        "block";


    document.getElementById(
        "explorador-etiqueta"
    ).textContent =
        "EXPLORADOR · " +
        dique.etiqueta;


    document.getElementById(
        "explorador-titulo"
    ).textContent =
        dique.nombre;


    document.getElementById(
        "imagen-detalle-dique"
    ).src =
        dique.detalle;


    document.getElementById(
        "panel-inicial"
    ).style.display =
        "flex";


    document.getElementById(
        "panel-activo"
    ).style.display =
        "none";


    const contenedor =
        document.getElementById(
            "contenedor-hotspots"
        );


    contenedor.innerHTML = "";


    Object.entries(
        dique.componentes
    ).forEach(
        function([numero, dato]) {


            const boton =
                document.createElement(
                    "button"
                );


            boton.className =
                "hotspot";


            boton.textContent =
                numero;


            boton.dataset.numero =
                numero;


            boton.style.left =
                dato.x + "%";


            boton.style.top =
                dato.y + "%";


            boton.onclick =
                function() {

                    seleccionarComponente(
                        numero
                    );

                };


            contenedor.appendChild(
                boton
            );

        }
    );

}


// ==========================================================
// COMPONENTE DEL DIQUE
// ==========================================================

function seleccionarComponente(numero) {


    const dato =
        diquesInteractivos[
            diqueActual
        ].componentes[
            numero
        ];


    document.querySelectorAll(
        ".hotspot"
    ).forEach(
        function(elemento) {

            elemento.classList.remove(
                "activo"
            );

        }
    );


    const activo =
        document.querySelector(
            '.hotspot[data-numero="' +
            numero +
            '"]'
        );


    if (activo) {

        activo.classList.add(
            "activo"
        );

    }


    document.getElementById(
        "panel-inicial"
    ).style.display =
        "none";


    document.getElementById(
        "panel-activo"
    ).style.display =
        "block";


    const imagen =
        document.getElementById(
            "imagen-componente"
        );


    if (dato.imagen) {

        imagen.src =
            dato.imagen;

        imagen.style.display =
            "block";

    }

    else {

        imagen.style.display =
            "none";

    }


    document.getElementById(
        "numero-componente"
    ).textContent =
        numero +
        " · COMPONENTE";


    document.getElementById(
        "titulo-componente"
    ).textContent =
        dato.nombre;


    document.getElementById(
        "texto-componente"
    ).textContent =
        dato.texto || "";

}


// ==========================================================
// VIDEO 3 · CARACOLES → ULLUM
// ==========================================================

function reproducirVideo3() {

    ocultarTodo();

    document.getElementById(
        "video-3-screen"
    ).style.display =
        "block";

    video3.currentTime = 0;

    video3.play();

}


video3.addEventListener(
    "ended",
    mostrarInfoUllumPantalla
);


// ==========================================================
// INFO ULLUM
// ==========================================================

function mostrarInfoUllumPantalla() {

    ocultarTodo();

    document.getElementById(
        "info-ullum"
    ).style.display =
        "block";

}


// ==========================================================
// RUEDA ULLUM
// ==========================================================

const infoUllum = {


    reserva: {

        icono: "💧",

        titulo:
            "Reserva del embalse",

        texto:
            "El embalse permite almacenar agua y regular su liberación en el tiempo. Mantener una mayor reserva puede aumentar la capacidad del sistema para responder a períodos posteriores de menor disponibilidad."

    },


    energia: {

        icono: "⚡",

        titulo:
            "Generación hidroeléctrica",

        texto:
            "Parte del agua liberada puede atravesar el sistema hidroeléctrico antes de continuar aguas abajo. Una mayor liberación permite una mayor generación relativa, pero también reduce más rápidamente el volumen almacenado."

    },


    caudal: {

        icono: "🌊",

        titulo:
            "Caudal aguas abajo",

        texto:
            "La cantidad de agua liberada desde Ullum condiciona la disponibilidad inmediata que continúa hacia la cuenca baja del Río San Juan."

    },


    demanda: {

        icono: "🌾",

        titulo:
            "Demanda de la cuenca baja",

        texto:
            "Aguas abajo, el recurso deberá abastecer distintos usos. En las siguientes etapas del simulador se incorporarán la agricultura, la ciudad, la industria y el abastecimiento de agua potable."

    }

};


function mostrarInfoUllum(clave) {


    const dato =
        infoUllum[clave];


    document.querySelectorAll(
        ".rueda-btn"
    ).forEach(
        function(elemento) {

            elemento.classList.remove(
                "activo"
            );

        }
    );


    const botonActivo =
        document.querySelector(
            '.rueda-btn[data-info="' +
            clave +
            '"]'
        );


    if (botonActivo) {

        botonActivo.classList.add(
            "activo"
        );

    }


    document.getElementById(
        "info-ullum-icono"
    ).textContent =
        dato.icono;


    document.getElementById(
        "info-ullum-titulo"
    ).textContent =
        dato.titulo;


    document.getElementById(
        "info-ullum-texto"
    ).textContent =
        dato.texto;

}


// ==========================================================
// DECISIÓN ULLUM
// ==========================================================

function mostrarDecisionUllum() {

    ocultarTodo();

    document.getElementById(
        "decision-ullum"
    ).style.display =
        "block";

}


// ==========================================================
// RESULTADO ULLUM
// ==========================================================

function seleccionarDecisionUllum(tipo) {


    let estrategia;

    let liberacion;

    let reserva;

    let energia;

    let estadoReserva;

    let texto;

    let videoSiguiente;


    if (tipo === "reserva") {


        estrategia =
            "Conservar reservas";

        liberacion =
            24;

        reserva =
            76;

        energia =
            "Baja";

        estadoReserva =
            "Alta";

        videoSiguiente =
            "Caudal_bajo";

        texto =
            "La estrategia conserva una mayor proporción del agua almacenada. La disponibilidad inmediata aguas abajo es menor, pero el sistema mantiene una reserva relativa más alta.";


    }


    else if (
        tipo === "equilibrada"
    ) {


        estrategia =
            "Gestión equilibrada";

        liberacion =
            30;

        reserva =
            70;

        energia =
            "Media";

        estadoReserva =
            "Estable";

        videoSiguiente =
            "Caudal_medio";

        texto =
            "La estrategia busca un equilibrio entre almacenamiento, generación hidroeléctrica y disponibilidad de agua para la cuenca baja.";


    }


    else {


        estrategia =
            "Mayor liberación";

        liberacion =
            36;

        reserva =
            64;

        energia =
            "Alta";

        estadoReserva =
            "Disminuye";

        videoSiguiente =
            "Caudal_alto";

        texto =
            "La liberación aumenta la disponibilidad inmediata aguas abajo y la generación relativa, pero reduce en mayor medida la reserva del embalse.";


    }


    decisionUllum = {

        estrategia:
            estrategia,

        liberacion:
            liberacion,

        reserva:
            reserva,

        energia:
            energia,

        estadoReserva:
            estadoReserva,

        videoSiguiente:
            videoSiguiente

    };


    document.getElementById(
        "estrategia-ullum"
    ).textContent =
        estrategia;


    document.getElementById(
        "donut-ullum"
    ).style.setProperty(
        "--reserva",
        reserva
    );


    document.getElementById(
        "reserva-numero"
    ).textContent =
        reserva + "%";


    document.getElementById(
        "caudal-ullum"
    ).textContent =
        liberacion;


    document.getElementById(
        "energia-ullum"
    ).textContent =
        energia;


    document.getElementById(
        "estado-reserva-ullum"
    ).textContent =
        estadoReserva;


    document.getElementById(
        "resultado-ullum-texto"
    ).textContent =
        texto;


    ocultarTodo();


    document.getElementById(
        "resultado-ullum"
    ).style.display =
        "block";

}


// ==========================================================
// CONTINUAR DISTRIBUIDOR
// ==========================================================

function continuarDistribuidor() {


    if (!decisionUllum) {
        return;
    }


    const aviso =
        document.getElementById(
            "aviso-distribuidor"
        );


    document.getElementById(
        "video-siguiente"
    ).textContent =
        decisionUllum.videoSiguiente;


    aviso.style.display =
        "block";

}


</script>
"""


    # ========================================================
    # REEMPLAZOS
    # ========================================================

    html = html_template


    html = html.replace(
        "__FONDO_MINA__",
        fondo_css
    )


    html = html.replace(
        "__VIDEO_1__",
        video_1_data or ""
    )


    html = html.replace(
        "__VIDEO_2__",
        video_2_data or ""
    )


    html = html.replace(
        "__VIDEO_3__",
        video_3_data or ""
    )


    html = html.replace(
        "__TRADICIONAL__",
        tradicional_html
    )


    html = html.replace(
        "__MODERNO__",
        moderno_html
    )


    html = html.replace(
        "__CARACOLES__",
        caracoles_html
    )


    html = html.replace(
        "__PUNTA_NEGRA__",
        punta_negra_html
    )


    html = html.replace(
        "__ULLUM__",
        ullum_html
    )


    html = html.replace(
        "__DIQUES_INTERACTIVOS__",
        diques_interactivos_json
    )


    # ========================================================
    # MOSTRAR
    # ========================================================

    st.components.v1.html(
        html,
        height=920,
        scrolling=False
    )