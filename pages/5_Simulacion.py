import streamlit as st
from pathlib import Path
import base64
import mimetypes
import json

from core.state_manager import init_session_state


# ============================================================
# CONFIGURACIÓN
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

            # Por ahora lo dejamos vacío.
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
        "No se encontró ningún video dentro de "
        "assets/videos/02_Mina_Diques/"
    )

    st.stop()


# ============================================================
# MINA
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
# MENÚ DE DIQUES
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
# IMÁGENES DE DETALLE
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
# COMPONENTES · PUNTA NEGRA
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

    "01": {
        "x": 60.2,
        "y": 58.1
    },

    "02": {
        "x": 55.6,
        "y": 67.1
    },

    "03": {
        "x": 61.4,
        "y": 86.2
    },

    "04": {
        "x": 63.6,
        "y": 94.0
    },

    "05": {
        "x": 31.5,
        "y": 83.0
    },

    "06": {
        "x": 33.8,
        "y": 65.2
    },

    "07": {
        "x": 38.4,
        "y": 45.1
    }
}


# ============================================================
# COMPONENTES · CARACOLES
# ============================================================

CARACOLES_COMPONENTES = {

    "01": "Embalse",

    "02": "Pantalla de hormigón",

    "03": "Coronamiento",

    "04": "Aliviadero",

    "05": "Casa de máquinas",

    "06": "Camino de acceso",

    "07": "Río San Juan"
}


HOTSPOTS_CARACOLES = {

    "01": {
        "x": 77.8,
        "y": 85.4
    },

    "02": {
        "x": 70.1,
        "y": 64.3
    },

    "03": {
        "x": 69.8,
        "y": 49.4
    },

    "04": {
        "x": 25.3,
        "y": 57.6
    },

    "05": {
        "x": 29.6,
        "y": 76.8
    },

    "06": {
        "x": 11.7,
        "y": 31.4
    },

    "07": {
        "x": 57.4,
        "y": 9.8
    }
}


# ============================================================
# COMPONENTES · ULLUM
# ============================================================
#
# El hotspot 08 (Quebrada de Ullum)
# NO se incluye.
#
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

    "01": {
        "x": 22.5,
        "y": 12.5
    },

    "02": {
        "x": 38.5,
        "y": 27.8
    },

    "03": {
        "x": 52.6,
        "y": 13.8
    },

    "04": {
        "x": 73.4,
        "y": 20.0
    },

    "05": {
        "x": 84.2,
        "y": 32.8
    },

    "06": {
        "x": 70.8,
        "y": 50.0
    },

    "07": {
        "x": 55.0,
        "y": 75.9
    }
}


# ============================================================
# CREAR DATOS DE COMPONENTES
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


caracoles_detalle_data = file_to_data_uri(
    caracoles_detalle_path
) or ""


punta_negra_detalle_data = file_to_data_uri(
    punta_negra_detalle_path
) or ""


ullum_detalle_data = file_to_data_uri(
    ullum_detalle_path
) or ""


# ============================================================
# BASE DE DATOS DE LOS 3 DIQUES
# ============================================================

DIQUES_INTERACTIVOS = {

    "caracoles": {

        "nombre": "Complejo Hidroeléctrico Los Caracoles",

        "etiqueta": "LOS CARACOLES",

        "detalle": caracoles_detalle_data,

        "componentes": caracoles_componentes
    },


    "punta_negra": {

        "nombre": "Complejo Hidroeléctrico Punta Negra",

        "etiqueta": "PUNTA NEGRA",

        "detalle": punta_negra_detalle_data,

        "componentes": punta_negra_componentes
    },


    "ullum": {

        "nombre": "Complejo Hidroeléctrico Dique de Ullum",

        "etiqueta": "ULLUM",

        "detalle": ullum_detalle_data,

        "componentes": ullum_componentes
    }

}


diques_interactivos_json = json.dumps(
    DIQUES_INTERACTIVOS,
    ensure_ascii=False
)


# ============================================================
# ESTADO STREAMLIT
# ============================================================

if (
    "experiencia_iniciada"
    not in st.session_state
):

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

    box-shadow:
        0 18px 45px
        rgba(0,0,0,0.22);

}



/* =========================================================
   VIDEO
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

    top: 30px;

    left: 35px;

    padding:
        12px 20px;

    color: white;

    background:
        rgba(0,0,0,0.48);

    border:
        1px solid
        rgba(255,255,255,0.18);

    border-radius: 12px;

    backdrop-filter: blur(7px);

    font-size: 18px;

    font-weight: 700;

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

    animation:
        aparecer 0.5s ease;

}


.pantalla-mina {

    background:
        __FONDO_MINA__;

    background-size: cover;

    background-position: center;

}


@keyframes aparecer {

    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }

}



/* =========================================================
   TÍTULOS
========================================================= */

.titulo-etapa {

    font-size: 14px;

    letter-spacing: 2.4px;

    color: #69d6dd;

    font-weight: 700;

    margin-bottom: 10px;

}


.titulo-principal {

    font-size: 42px;

    font-weight: 800;

    margin-bottom: 12px;

    color: white;

}


.descripcion {

    font-size: 17px;

    line-height: 1.6;

    max-width: 1050px;

    margin-bottom: 24px;

}



/* =========================================================
   TARJETAS MINA
========================================================= */

.grid-procesos {

    display: grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap: 18px;

    margin-top: 18px;

    margin-bottom: 20px;

}


.card-proceso {

    background:
        rgba(12,22,27,0.52);

    border:
        1px solid
        rgba(255,255,255,0.24);

    border-radius: 17px;

    overflow: hidden;

}


.foto-proceso {

    width: 100%;

    height: 200px;

    object-fit: cover;

}


.placeholder-foto {

    height: 200px;

    display: flex;

    align-items: center;

    justify-content: center;

}


.card-proceso-body {

    padding:
        17px 20px 19px;

}


.card-subtitle {

    font-size: 12px;

    letter-spacing: 1.5px;

    color: #75dce2;

    font-weight: 700;

    margin-bottom: 7px;

}


.card-title {

    font-size: 23px;

    font-weight: 750;

    margin-bottom: 10px;

}


.card-text {

    font-size: 15px;

    line-height: 1.5;

    color: #f3f3f3;

}


.info-clave {

    margin-top: 10px;

    padding:
        16px 20px;

    border-radius: 15px;

    background:
        rgba(10,20,25,0.52);

    border:
        1px solid
        rgba(112,214,222,0.42);

    line-height: 1.55;

}



/* =========================================================
   BOTONES
========================================================= */

.botones-navegacion {

    display: flex;

    justify-content: center;

    gap: 14px;

    margin-top: 22px;

    flex-wrap: wrap;

}


.btn-principal,
.btn-secundario {

    border:
        1px solid
        rgba(255,255,255,0.28);

    border-radius: 13px;

    padding:
        15px 25px;

    color: white;

    font-size: 16px;

    font-weight: 700;

    cursor: pointer;

}


.btn-principal {

    background:
        rgba(22,156,171,0.95);

}


.btn-secundario {

    background:
        rgba(10,20,25,0.62);

}



/* =========================================================
   DECISIÓN MINA
========================================================= */

.pregunta {

    font-size: 25px;

    font-weight: 700;

    margin-top: 32px;

    margin-bottom: 20px;

}


.opciones {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 17px;

}


.opcion {

    width: 100%;

    box-sizing: border-box;

    text-align: left;

    color: white;

    background:
        rgba(10,20,25,0.58);

    border:
        1px solid
        rgba(255,255,255,0.24);

    border-radius: 17px;

    padding: 23px;

    cursor: pointer;

}


.opcion strong {

    display: block;

    font-size: 20px;

    margin-bottom: 9px;

}


.opcion span {

    display: block;

    font-size: 15px;

    line-height: 1.5;

}



/* =========================================================
   RESULTADO MINA
========================================================= */

.resultado-grid {

    display: grid;

    grid-template-columns:
        0.85fr 1.15fr;

    gap: 38px;

    align-items: center;

    margin-top: 25px;

}


.donut-wrapper {

    display: flex;

    justify-content: center;

}


.donut {

    width: 315px;

    height: 315px;

    border-radius: 50%;

    background:

        conic-gradient(

            #e9a23b
            0%
            calc(var(--consumo) * 1%),

            #4dc1d1
            calc(var(--consumo) * 1%)
            100%

        );

    display: flex;

    align-items: center;

    justify-content: center;

    position: relative;

}


.donut::before {

    content: "";

    width: 205px;

    height: 205px;

    background:
        rgba(7,19,26,0.94);

    border-radius: 50%;

    position: absolute;

}


.donut-centro {

    position: relative;

    z-index: 3;

    text-align: center;

}


.donut-numero {

    font-size: 54px;

    font-weight: 800;

}


.donut-texto {

    margin-top: 8px;

    font-size: 15px;

    color: #cdebf0;

    max-width: 140px;

}


.metricas {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 12px;

    margin-bottom: 18px;

}


.metrica {

    background:
        rgba(9,22,29,0.60);

    border:
        1px solid
        rgba(255,255,255,0.18);

    padding: 18px;

    border-radius: 14px;

}


.metrica-numero {

    font-size: 31px;

    font-weight: 800;

}


.metrica-label {

    font-size: 13px;

    color: #cde0e5;

    margin-top: 4px;

}


.resultado-explicacion {

    background:
        rgba(9,22,29,0.59);

    border:
        1px solid
        rgba(255,255,255,0.19);

    border-radius: 16px;

    padding: 21px;

    line-height: 1.6;

}


.modelo-educativo {

    margin-top: 18px;

    padding:
        14px 17px;

    border-radius: 12px;

    font-size: 13px;

    line-height: 1.5;

    background:
        rgba(0,0,0,0.40);

}



/* =========================================================
   MENÚ DIQUES
========================================================= */

#menu-diques {

    background:
        linear-gradient(
            135deg,
            #071925 0%,
            #0d3041 48%,
            #12516a 100%
        );

}


.recorrido-diques {

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 10px;

    flex-wrap: wrap;

    margin:
        8px 0 28px;

    padding:
        12px 15px;

    border-radius: 14px;

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid
        rgba(255,255,255,0.12);

}


.flecha-recorrido {

    color: #63d2df;

}


.nodo-recorrido {

    font-size: 14px;

    font-weight: 700;

}


.grid-diques {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 18px;

}


.card-dique {

    overflow: hidden;

    background:
        rgba(4,18,27,0.65);

    border:
        1px solid
        rgba(255,255,255,0.18);

    border-radius: 18px;

}


.foto-card-dique,
.placeholder-card-dique {

    width: 100%;

    height: 210px;

    object-fit: cover;

}


.card-dique-body {

    padding:
        18px 18px 20px;

}


.card-dique-kicker {

    font-size: 10px;

    letter-spacing: 1.5px;

    color: #69d6dd;

    margin-bottom: 6px;

}


.card-dique-title {

    font-size: 24px;

    font-weight: 800;

    margin-bottom: 8px;

}


.card-dique-text {

    min-height: 45px;

    font-size: 14px;

    line-height: 1.45;

    color: #dce8ec;

}


.btn-explorar {

    margin-top: 15px;

    width: 100%;

    padding: 12px;

    border: none;

    border-radius: 11px;

    background:
        rgba(25,166,183,0.88);

    color: white;

    font-size: 14px;

    font-weight: 700;

    cursor: pointer;

}



/* =========================================================
   EXPLORADOR GENÉRICO
========================================================= */

#explorador-dique {

    background:
        linear-gradient(
            135deg,
            #071720,
            #0c2c3a
        );

}


.explorador-top {

    display: flex;

    justify-content:
        space-between;

    align-items:
        flex-start;

    gap: 20px;

}


.btn-volver {

    border:
        1px solid
        rgba(255,255,255,0.20);

    background:
        rgba(255,255,255,0.07);

    color: white;

    border-radius: 11px;

    padding:
        11px 16px;

    cursor: pointer;

    font-weight: 700;

}


.guia-explorador {

    margin:
        5px 0 18px;

    padding:
        11px 15px;

    border-radius: 12px;

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid
        rgba(255,255,255,0.11);

    color:
        #d5e7ec;

    font-size: 14px;

}


.explorador-grid {

    display: grid;

    grid-template-columns:
        minmax(0,1.55fr)
        minmax(280px,0.65fr);

    gap: 18px;

    align-items: start;

}



/* =========================================================
   FOTO + HOTSPOTS
========================================================= */

.mapa-hotspots {

    position: relative;

    width: 100%;

    border-radius: 17px;

    overflow: hidden;

    background: black;

    border:
        1px solid
        rgba(255,255,255,0.14);

}


.img-detalle {

    width: 100%;

    height: auto;

    display: block;

}


.hotspot {

    position: absolute;

    transform:
        translate(-50%,-50%);

    width: 46px;

    height: 46px;

    border-radius: 50%;

    border:
        2px solid white;

    background:
        rgba(6,25,34,0.76);

    color: white;

    font-weight: 800;

    cursor: pointer;

    box-shadow:
        0 4px 18px
        rgba(0,0,0,0.38);

    transition:
        0.22s;

    z-index: 5;

}


.hotspot:hover {

    transform:
        translate(-50%,-50%)
        scale(1.12);

    background:
        #2bb9c8;

}


.hotspot.activo {

    background:
        #37c6d5;

    border-color:
        #baf9ff;

    transform:
        translate(-50%,-50%)
        scale(1.15);

    box-shadow:
        0 0 0 7px
        rgba(55,198,213,0.18);

}



/* =========================================================
   PANEL COMPONENTE
========================================================= */

.panel-componente {

    min-height: 520px;

    box-sizing: border-box;

    border-radius: 17px;

    overflow: hidden;

    background:
        rgba(255,255,255,0.07);

    border:
        1px solid
        rgba(255,255,255,0.13);

}


.panel-inicial {

    min-height: 520px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    padding: 30px;

    box-sizing: border-box;

    text-align: center;

    color: #d8e7eb;

}


.icono-explorar {

    font-size: 48px;

    margin-bottom: 14px;

}


.panel-activo {

    display: none;

}


.imagen-componente {

    width: 100%;

    height: 235px;

    object-fit: cover;

    display: block;

}


.numero-componente {

    margin:
        20px 22px 4px;

    color: #64d3df;

    font-size: 12px;

    letter-spacing: 1.8px;

    font-weight: 800;

}


.titulo-componente {

    margin:
        0 22px;

    font-size: 25px;

    font-weight: 800;

}


.texto-componente {

    margin:
        18px 22px 25px;

    min-height: 110px;

    border-top:
        1px solid
        rgba(255,255,255,0.10);

    padding-top: 16px;

    font-size: 15px;

    line-height: 1.55;

    color: #dce8ec;

}



/* =========================================================
   CONTINUAR
========================================================= */

.panel-continuar {

    display: none;

    margin-top: 20px;

    padding: 18px;

    text-align: center;

    border-radius: 14px;

    background:
        rgba(99,210,223,0.12);

    border:
        1px solid
        rgba(99,210,223,0.35);

}



/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {

    .grid-procesos,
    .opciones,
    .resultado-grid,
    .grid-diques,
    .explorador-grid {

        grid-template-columns: 1fr;

    }


    .metricas {

        grid-template-columns: 1fr;

    }


    .titulo-principal {

        font-size: 32px;

    }


    .panel-componente,
    .panel-inicial {

        min-height: auto;

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
    class="
        pantalla-contenido
        pantalla-mina
    "
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
    class="
        pantalla-contenido
        pantalla-mina
    "
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
            onclick="seleccionarDecision('alta')"
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
            onclick="seleccionarDecision('media')"
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
            onclick="seleccionarDecision('nula')"
        >

            <strong>
                💧 Sin recirculación · 0 %
            </strong>

            <span>
                Consumo neto aproximado: 25 %.
            </span>

        </button>

    </div>


    <div class="botones-navegacion">

        <button
            class="btn-secundario"
            onclick="mostrarInfoMina()"
        >
            ← Volver a la información
        </button>

    </div>

</div>



<!-- =====================================================
     RESULTADO MINA
===================================================== -->

<div
    id="resultado-mina"
    class="
        pantalla-contenido
        pantalla-mina
    "
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

                para seguir hacia el sistema
                de embalses.

            </div>


            <div class="modelo-educativo">

                ℹ️ Modelo educativo simplificado.

                Los porcentajes son normalizados
                para representar la relación entre
                consumo y recuperación.

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
        🌊 Mina → Sistema de embalses
    </div>

</div>



<!-- =====================================================
     MENÚ DE DIQUES
===================================================== -->

<div
    id="menu-diques"
    class="pantalla-contenido"
>

    <div class="titulo-etapa">
        PARADA 2 · SISTEMA DE EMBALSES
    </div>

    <div class="titulo-principal">
        🏞️ Sistema de regulación del Río San Juan
    </div>

    <div class="descripcion">

        Los principales aprovechamientos
        funcionan de manera encadenada.

        Podés explorar cada dique antes
        de continuar con la simulación.

    </div>


    <div class="recorrido-diques">

        <span class="nodo-recorrido">
            🏔 Cordillera
        </span>

        <span class="flecha-recorrido">
            →
        </span>

        <span class="nodo-recorrido">
            Los Caracoles
        </span>

        <span class="flecha-recorrido">
            →
        </span>

        <span class="nodo-recorrido">
            Punta Negra
        </span>

        <span class="flecha-recorrido">
            →
        </span>

        <span class="nodo-recorrido">
            Ullum
        </span>

        <span class="flecha-recorrido">
            →
        </span>

        <span class="nodo-recorrido">
            🌾 Valle de Tulum
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
            ↻ Reproducir Mina → Embalses
        </button>

        <button
            class="btn-principal"
            onclick="continuarSimulacion()"
        >
            Continuar con la simulación →
        </button>

    </div>


    <div
        id="panel-continuar"
        class="panel-continuar"
    >

        ✅ Exploración de los embalses disponible.

        <br><br>

        El próximo paso será incorporar
        la decisión de gestión de los embalses.

    </div>

</div>



<!-- =====================================================
     EXPLORADOR GENÉRICO DE DIQUES
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
                Complejo Hidroeléctrico
            </div>

        </div>


        <button
            class="btn-volver"
            onclick="mostrarMenuDiques()"
        >
            ← Volver a los diques
        </button>

    </div>


    <div class="guia-explorador">

        Seleccioná uno de los puntos numerados
        para conocer cada componente del aprovechamiento.

    </div>


    <div class="explorador-grid">


        <!-- FOTO GRANDE -->

        <div
            id="mapa-hotspots"
            class="mapa-hotspots"
        >

            <img
                id="imagen-detalle-dique"
                class="img-detalle"
                src=""
            >


            <div
                id="contenedor-hotspots"
            >
            </div>

        </div>



        <!-- PANEL LATERAL -->

        <div class="panel-componente">


            <div
                id="panel-inicial"
                class="panel-inicial"
            >

                <div class="icono-explorar">
                    ◎
                </div>

                <strong>
                    Explorá el aprovechamiento
                </strong>

                <br><br>

                Tocá uno de los círculos
                numerados sobre la fotografía.

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


</div>



<script>


// ==========================================================
// BASE DE DATOS DIQUES
// ==========================================================

const diquesInteractivos =
    __DIQUES_INTERACTIVOS__;


// ==========================================================
// ESTADO
// ==========================================================

let decisionActual = null;

let recirculacionActual = 0;

let consumoActual = 0;

let restanteActual = 100;

let diqueActual = null;


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

    "explorador-dique"

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
    document.getElementById(
        "video-1"
    );


const video2 =
    document.getElementById(
        "video-2"
    );


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
    function() {

        mostrarInfoMina();

    }
);


// ==========================================================
// INFORMACIÓN MINA
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


function seleccionarDecision(tipo) {


    if (tipo === "alta") {

        decisionActual =
            "Alta recirculación";

        recirculacionActual = 80;

        consumoActual = 5;

        restanteActual = 95;

    }


    else if (tipo === "media") {

        decisionActual =
            "Recirculación intermedia";

        recirculacionActual = 60;

        consumoActual = 10;

        restanteActual = 90;

    }


    else if (tipo === "nula") {

        decisionActual =
            "Sin recirculación";

        recirculacionActual = 0;

        consumoActual = 25;

        restanteActual = 75;

    }


    actualizarResultadoMina();

    mostrarResultadoMina();

}


// ==========================================================
// RESULTADO MINA
// ==========================================================

function actualizarResultadoMina() {


    document.getElementById(
        "resultado-titulo"
    ).textContent =
        decisionActual;


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

}


function mostrarResultadoMina() {

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
    function() {

        mostrarMenuDiques();

    }
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
// EXPLORAR DIQUE
// ==========================================================

function explorarDique(clave) {


    const dique =
        diquesInteractivos[
            clave
        ];


    if (!dique) {
        return;
    }


    diqueActual =
        clave;


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


    // Reset panel lateral

    document.getElementById(
        "panel-inicial"
    ).style.display =
        "flex";


    document.getElementById(
        "panel-activo"
    ).style.display =
        "none";


    // Limpiar hotspots previos

    const contenedor =
        document.getElementById(
            "contenedor-hotspots"
        );


    contenedor.innerHTML =
        "";


    // Crear hotspots del dique

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


            boton.addEventListener(
                "click",
                function() {

                    seleccionarComponente(
                        numero
                    );

                }
            );


            contenedor.appendChild(
                boton
            );

        }
    );

}


// ==========================================================
// SELECCIONAR COMPONENTE
// ==========================================================

function seleccionarComponente(
    numero
) {


    if (!diqueActual) {
        return;
    }


    const dique =
        diquesInteractivos[
            diqueActual
        ];


    const dato =
        dique.componentes[
            numero
        ];


    if (!dato) {
        return;
    }


    // Quitar selección anterior

    document.querySelectorAll(
        ".hotspot"
    ).forEach(
        function(elemento) {

            elemento.classList.remove(
                "activo"
            );

        }
    );


    // Activar seleccionado

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


    // ======================================================
    // IMAGEN
    // ======================================================

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

        // Si no existe imagen,
        // directamente no mostramos
        // una caja vacía.

        imagen.src =
            "";

        imagen.style.display =
            "none";

    }


    // ======================================================
    // NÚMERO
    // ======================================================

    document.getElementById(
        "numero-componente"
    ).textContent =
        numero +
        " · COMPONENTE";


    // ======================================================
    // TÍTULO
    // ======================================================

    document.getElementById(
        "titulo-componente"
    ).textContent =
        dato.nombre;


    // ======================================================
    // TEXTO
    // ======================================================
    //
    // Por ahora queda vacío.
    // Lo completaremos después.
    //

    document.getElementById(
        "texto-componente"
    ).textContent =
        dato.texto || "";

}


// ==========================================================
// CONTINUAR
// ==========================================================

function continuarSimulacion() {

    const panel =
        document.getElementById(
            "panel-continuar"
        );


    panel.style.display =
        "block";


    panel.scrollIntoView({

        behavior:
            "smooth",

        block:
            "nearest"

    });

}


</script>

"""


    # ========================================================
    # REEMPLAZOS HTML
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
    # MOSTRAR COMPONENTE
    # ========================================================

    st.components.v1.html(
        html,
        height=920,
        scrolling=False
    )