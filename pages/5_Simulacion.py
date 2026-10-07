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

    mime_type, _ = mimetypes.guess_type(
        str(file_path)
    )

    if mime_type is None:
        mime_type = "application/octet-stream"

    encoded = base64.b64encode(
        file_path.read_bytes()
    ).decode()

    return f"data:{mime_type};base64,{encoded}"


def buscar_archivo(
    carpeta: Path,
    extensiones
):

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


def buscar_por_prefijo(
    carpeta: Path,
    prefijo: str
):

    if not carpeta.exists():
        return None

    for archivo in sorted(
        carpeta.rglob("*")
    ):

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
    imagen,
    activo=True
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

    if activo:

        boton = f"""
        <button
            class="btn-explorar"
            onclick="explorarDique('{identificador}')"
        >
            Explorar dique →
        </button>
        """

    else:

        boton = f"""
        <button
            class="btn-explorar deshabilitado"
            onclick="mostrarProximamente('{nombre}')"
        >
            Explorar dique
        </button>
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

            {boton}

        </div>

    </div>
    """


# ============================================================
# ESCENARIO SELECCIONADO
# ============================================================

escenario = st.session_state.get(
    "escenario_seleccionado"
)


if not escenario:

    st.warning(
        "Primero debes seleccionar un escenario."
    )

    if st.button(
        "← Volver al simulador"
    ):

        st.switch_page(
            "pages/1_Simulador.py"
        )

    st.stop()


# ============================================================
# POR AHORA SOLO SUPERAVITARIO
# ============================================================

if escenario != "Superavitario":

    st.title(
        "🌊 Simulación Hídrica"
    )

    st.markdown(
        f"### Escenario inicial: **{escenario}**"
    )

    st.info(
        f"El escenario {escenario} todavía no "
        "tiene cargada la experiencia audiovisual."
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

    st.code(
        str(video_1_path)
    )

    st.stop()


# ============================================================
# VIDEO 2 · MINA → DIQUES
# ============================================================

carpeta_video_2 = (
    BASE_DIR
    / "assets"
    / "videos"
    / "02_Mina_Diques"
)


video_2_path = (
    carpeta_video_2
    / "Mina_Diques.mp4"
)


if not video_2_path.exists():

    video_2_path = buscar_archivo(
        carpeta_video_2,
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
# IMÁGENES MINA
# ============================================================

img_moderno_path = (
    BASE_DIR
    / "assets"
    / "images"
    / "mina"
    / "metodo_moderno_recirculacion.jpg"
)


img_tradicional_path = (
    BASE_DIR
    / "assets"
    / "images"
    / "mina"
    / "metodo_tradicional_abierto.jpg"
)


fondo_mina_path = (
    BASE_DIR
    / "assets"
    / "images"
    / "mina"
    / "fondo_mina.jpg"
)


# ============================================================
# CARPETAS DIQUES
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
# IMÁGENES MENÚ DIQUES
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
# IMAGEN DETALLE PUNTA NEGRA
# ============================================================

punta_negra_detalle_path = (
    PUNTA_NEGRA_DIR
    / "punta_negra_detalle.jpg"
)


if not punta_negra_detalle_path.exists():

    punta_negra_detalle_path = buscar_por_prefijo(
        PUNTA_NEGRA_DIR,
        "punta_negra_detalle"
    )


# ============================================================
# COMPONENTES PUNTA NEGRA
# ============================================================

COMPONENTES_DIR = (
    PUNTA_NEGRA_DIR
    / "Componentes"
)


componentes_paths = {

    "01": buscar_por_prefijo(
        COMPONENTES_DIR,
        "01_"
    ),

    "02": buscar_por_prefijo(
        COMPONENTES_DIR,
        "02_"
    ),

    "03": buscar_por_prefijo(
        COMPONENTES_DIR,
        "03_"
    ),

    "04": buscar_por_prefijo(
        COMPONENTES_DIR,
        "04_"
    ),

    "05": buscar_por_prefijo(
        COMPONENTES_DIR,
        "05_"
    ),

    "06": buscar_por_prefijo(
        COMPONENTES_DIR,
        "06_"
    ),

    "07": buscar_por_prefijo(
        COMPONENTES_DIR,
        "07_"
    ),
}


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


punta_negra_detalle_data = file_to_data_uri(
    punta_negra_detalle_path
)


# ============================================================
# DATOS COMPONENTES PUNTA NEGRA
# ============================================================

componentes_punta_negra = {

    "01": {

        "nombre": "Obra de toma",

        "imagen": file_to_data_uri(
            componentes_paths["01"]
        ) or "",

        "texto": ""

    },


    "02": {

        "nombre": "Aliviadero",

        "imagen": file_to_data_uri(
            componentes_paths["02"]
        ) or "",

        "texto": ""

    },


    "03": {

        "nombre": "Casa de máquinas",

        "imagen": file_to_data_uri(
            componentes_paths["03"]
        ) or "",

        "texto": ""

    },


    "04": {

        "nombre": "Subestación",

        "imagen": file_to_data_uri(
            componentes_paths["04"]
        ) or "",

        "texto": ""

    },


    "05": {

        "nombre": "Descargador de fondo",

        "imagen": file_to_data_uri(
            componentes_paths["05"]
        ) or "",

        "texto": ""

    },


    "06": {

        "nombre": "Presa",

        "imagen": file_to_data_uri(
            componentes_paths["06"]
        ) or "",

        "texto": ""

    },


    "07": {

        "nombre": "Embalse",

        "imagen": file_to_data_uri(
            componentes_paths["07"]
        ) or "",

        "texto": ""

    }

}


# ============================================================
# POSICIONES CORREGIDAS DE LOS HOTSPOTS
# ============================================================
#
# Estas coordenadas están ajustadas para
# punta_negra_detalle.jpg que estás usando ahora.
#
# x = porcentaje desde la izquierda
# y = porcentaje desde arriba
#
# ============================================================

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


# Añadir coordenadas a cada componente

for numero, posicion in (
    HOTSPOTS_PUNTA_NEGRA.items()
):

    componentes_punta_negra[
        numero
    ]["x"] = posicion["x"]

    componentes_punta_negra[
        numero
    ]["y"] = posicion["y"]


componentes_punta_negra_json = json.dumps(
    componentes_punta_negra,
    ensure_ascii=False
)


# ============================================================
# ESTADO STREAMLIT
# ============================================================

if (
    "experiencia_iniciada"
    not in st.session_state
):

    st.session_state.experiencia_iniciada = (
        False
    )


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

            st.session_state.experiencia_iniciada = (
                True
            )

            st.rerun()


# ============================================================
# EXPERIENCIA PRINCIPAL
# ============================================================

else:

    # ========================================================
    # TARJETA MINA TRADICIONAL
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


    # ========================================================
    # TARJETA MINA MODERNA
    # ========================================================

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
        Primer gran aprovechamiento del sistema
        en el recorrido aguas abajo.
        """,

        imagen=caracoles_menu_data,

        activo=False

    )


    punta_negra_html = crear_tarjeta_dique(

        identificador="punta_negra",

        nombre="Punta Negra",

        subtitulo="""
        Explorá sus principales componentes
        y cómo se integran dentro del aprovechamiento.
        """,

        imagen=punta_negra_menu_data,

        activo=True

    )


    ullum_html = crear_tarjeta_dique(

        identificador="ullum",

        nombre="Quebrada de Ullum",

        subtitulo="""
        Último gran aprovechamiento antes
        del ingreso hacia la cuenca baja.
        """,

        imagen=ullum_menu_data,

        activo=False

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
    # HTML PRINCIPAL
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

    top: 30px;

    left: 35px;

    padding: 12px 20px;

    color: white;

    background:
        rgba(0,0,0,0.48);

    border:
        1px solid
        rgba(255,255,255,0.18);

    border-radius: 12px;

    backdrop-filter:
        blur(7px);

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

    padding: 35px 38px;

    color: white;

    overflow-y: auto;

    animation:
        aparecer 0.50s ease;

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

    color: white;

}



/* =========================================================
   TARJETAS MINA
========================================================= */

.grid-procesos {

    display: grid;

    grid-template-columns:
        repeat(2,1fr);

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
   DECISIONES MINA
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

}


.nodo-recorrido {

    font-size: 14px;

    font-weight: 700;

}


.flecha-recorrido {

    color: #63d2df;

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


.btn-explorar.deshabilitado {

    background:
        rgba(255,255,255,0.10);

    color:
        rgba(255,255,255,0.70);

}


.mensaje-proximamente {

    display: none;

    margin-top: 20px;

    padding:
        14px 18px;

    border-radius: 13px;

    text-align: center;

    background:
        rgba(255,255,255,0.07);

}



/* =========================================================
   EXPLORADOR PUNTA NEGRA
========================================================= */

#explorador-punta-negra {

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


.indicadores-dique {

    display: flex;

    gap: 10px;

    flex-wrap: wrap;

    margin:
        12px 0 20px;

}


.indicador {

    padding:
        10px 14px;

    border-radius: 12px;

    background:
        rgba(255,255,255,0.07);

    border:
        1px solid
        rgba(255,255,255,0.13);

}


.indicador strong {

    display: block;

    font-size: 18px;

}


.indicador span {

    font-size: 11px;

    color: #cbdde3;

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
   FOTO DETALLE + HOTSPOTS
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

    min-height: 570px;

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

    min-height: 570px;

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

    font-size: 50px;

    margin-bottom: 14px;

}


.panel-activo {

    display: none;

}


.imagen-componente {

    width: 100%;

    height: 245px;

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

        grid-template-columns:
            1fr;

    }


    .metricas {

        grid-template-columns:
            1fr;

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
        observá cómo distintas formas
        de gestión modifican el consumo
        neto de agua.

    </div>

    <div class="grid-procesos">

        __TRADICIONAL__

        __MODERNO__

    </div>

    <div class="info-clave">

        <strong>💡 Concepto clave:</strong>

        una mayor recuperación y
        recirculación reduce la necesidad
        de incorporar agua fresca.

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
     VIDEO 2 · MINA → DIQUES
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
     MENÚ DIQUES
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

        El agua liberada en uno continúa
        su recorrido hacia el siguiente.

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


    <div
        id="mensaje-proximamente"
        class="mensaje-proximamente"
    >
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

        ✅ Centro interactivo completado.

        <br><br>

        El próximo paso será incorporar
        la información sobre gestión de los
        embalses y la decisión de operación.

    </div>

</div>



<!-- =====================================================
     EXPLORADOR PUNTA NEGRA
===================================================== -->

<div
    id="explorador-punta-negra"
    class="pantalla-contenido"
>

    <div class="explorador-top">

        <div>

            <div class="titulo-etapa">
                EXPLORADOR · PUNTA NEGRA
            </div>

            <div class="titulo-principal">
                Complejo Hidroeléctrico Punta Negra
            </div>

        </div>


        <button
            class="btn-volver"
            onclick="mostrarMenuDiques()"
        >
            ← Volver a los diques
        </button>

    </div>


    <div class="indicadores-dique">

        <div class="indicador">

            <strong>
                118,4 m
            </strong>

            <span>
                Altura aproximada de presa
            </span>

        </div>


        <div class="indicador">

            <strong>
                500 hm³
            </strong>

            <span>
                Capacidad aproximada
            </span>

        </div>


        <div class="indicador">

            <strong>
                300 GWh/año
            </strong>

            <span>
                Generación aproximada
            </span>

        </div>

    </div>


    <div class="explorador-grid">


        <div class="mapa-hotspots">

            <img
                src="__PUNTA_NEGRA_DETALLE__"
                class="img-detalle"
            >


            <button
                class="hotspot"
                data-numero="01"
                onclick="seleccionarComponente('01')"
            >
                01
            </button>


            <button
                class="hotspot"
                data-numero="02"
                onclick="seleccionarComponente('02')"
            >
                02
            </button>


            <button
                class="hotspot"
                data-numero="03"
                onclick="seleccionarComponente('03')"
            >
                03
            </button>


            <button
                class="hotspot"
                data-numero="04"
                onclick="seleccionarComponente('04')"
            >
                04
            </button>


            <button
                class="hotspot"
                data-numero="05"
                onclick="seleccionarComponente('05')"
            >
                05
            </button>


            <button
                class="hotspot"
                data-numero="06"
                onclick="seleccionarComponente('06')"
            >
                06
            </button>


            <button
                class="hotspot"
                data-numero="07"
                onclick="seleccionarComponente('07')"
            >
                07
            </button>

        </div>



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

                <br>

                Seleccioná uno de los puntos
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
// COMPONENTES PUNTA NEGRA
// ==========================================================

const componentesPuntaNegra =
    __COMPONENTES_PUNTA_NEGRA__;


// ==========================================================
// COLOCAR HOTSPOTS
// ==========================================================

Object.entries(
    componentesPuntaNegra
).forEach(
    function([numero, dato]) {

        const hotspot =
            document.querySelector(
                '.hotspot[data-numero="' +
                numero +
                '"]'
            );

        if (hotspot) {

            hotspot.style.left =
                dato.x + "%";

            hotspot.style.top =
                dato.y + "%";

        }

    }
);


// ==========================================================
// ESTADO DE LA SIMULACIÓN
// ==========================================================

let decisionActual = null;

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

    "explorador-punta-negra"

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

    video1.currentTime =
        0;

    video1.play();

}


video1.addEventListener(
    "ended",
    function() {

        mostrarInfoMina();

    }
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


function seleccionarDecision(
    tipo
) {


    if (tipo === "alta") {

        decisionActual =
            "Alta recirculación";

        recirculacionActual =
            80;

        consumoActual =
            5;

        restanteActual =
            95;

    }


    else if (
        tipo === "media"
    ) {

        decisionActual =
            "Recirculación intermedia";

        recirculacionActual =
            60;

        consumoActual =
            10;

        restanteActual =
            90;

    }


    else if (
        tipo === "nula"
    ) {

        decisionActual =
            "Sin recirculación";

        recirculacionActual =
            0;

        consumoActual =
            25;

        restanteActual =
            75;

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
        restanteActual +
        "%";


    document.getElementById(
        "metrica-recirculacion"
    ).textContent =
        recirculacionActual +
        "%";


    document.getElementById(
        "metrica-consumo"
    ).textContent =
        "-" +
        consumoActual +
        "%";


    document.getElementById(
        "metrica-restante"
    ).textContent =
        restanteActual +
        "%";


    document.getElementById(
        "texto-consumo"
    ).textContent =
        consumoActual +
        " %";


    document.getElementById(
        "texto-restante"
    ).textContent =
        restanteActual +
        " %";

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

    video2.currentTime =
        0;

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


function explorarDique(
    dique
) {

    if (
        dique ===
        "punta_negra"
    ) {

        ocultarTodo();

        document.getElementById(
            "explorador-punta-negra"
        ).style.display =
            "block";

    }

}


function mostrarProximamente(
    nombre
) {

    const panel =
        document.getElementById(
            "mensaje-proximamente"
        );


    panel.innerHTML =
        "<strong>" +
        nombre +
        "</strong>" +
        "<br>" +
        "La exploración interactiva de este dique " +
        "se incorporará en la próxima etapa.";


    panel.style.display =
        "block";

}


// ==========================================================
// HOTSPOTS
// ==========================================================

function seleccionarComponente(
    numero
) {


    const dato =
        componentesPuntaNegra[
            numero
        ];


    if (!dato) {
        return;
    }


    document.querySelectorAll(
        ".hotspot"
    ).forEach(
        function(elemento) {

            elemento.classList.remove(
                "activo"
            );

        }
    );


    const hotspotActivo =
        document.querySelector(
            '.hotspot[data-numero="' +
            numero +
            '"]'
        );


    if (hotspotActivo) {

        hotspotActivo.classList.add(
            "activo"
        );

    }


    document.getElementById(
        "panel-inicial"
    ).style.display =
        "none";


    const panelActivo =
        document.getElementById(
            "panel-activo"
        );


    panelActivo.style.display =
        "block";


    const imagen =
        document.getElementById(
            "imagen-componente"
        );


    if (
        dato.imagen
    ) {

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
        "__PUNTA_NEGRA_DETALLE__",
        punta_negra_detalle_data or ""
    )


    html = html.replace(
        "__COMPONENTES_PUNTA_NEGRA__",
        componentes_punta_negra_json
    )


    # ========================================================
    # MOSTRAR COMPONENTE
    # ========================================================

    st.components.v1.html(
        html,
        height=920,
        scrolling=False
    )