import streamlit as st
from pathlib import Path
import base64
import mimetypes

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
# FUNCIONES
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

    """
    Busca recursivamente el primer archivo
    que tenga alguna de las extensiones indicadas.
    """

    if not carpeta.exists():
        return None

    archivos = []

    for archivo in carpeta.rglob("*"):

        if (
            archivo.is_file()
            and archivo.suffix.lower() in extensiones
        ):
            archivos.append(archivo)

    if not archivos:
        return None

    return sorted(archivos)[0]


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
    titulo,
    texto,
    imagen
):

    if imagen:

        bloque_imagen = f"""
        <img
            src="{imagen}"
            class="foto-dique"
        >
        """

    else:

        bloque_imagen = """
        <div class="placeholder-dique">
            Imagen no disponible
        </div>
        """

    return f"""
    <div class="card-dique">

        {bloque_imagen}

        <div class="dique-contenido">

            <div class="dique-titulo">
                {titulo}
            </div>

            <div class="dique-texto">
                {texto}
            </div>

        </div>

    </div>
    """


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

    st.code(str(video_1_path))

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


# Primero intenta encontrar Mina_Diques.mp4
video_2_path = (
    carpeta_video_2
    / "Mina_Diques.mp4"
)


# Si no existe con ese nombre,
# busca automáticamente el primer video.
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
        "No se encontró ningún video "
        "dentro de assets/videos/02_Mina_Diques/"
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
# IMÁGENES DIQUES
# ============================================================

carpeta_diques = (
    BASE_DIR
    / "assets"
    / "images"
    / "Diques"
)


img_caracoles_path = buscar_archivo(
    carpeta_diques / "Caracoles",
    {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }
)


img_punta_negra_path = buscar_archivo(
    carpeta_diques / "Punta_Negra",
    {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }
)


img_ullum_path = buscar_archivo(
    carpeta_diques / "Ullum",
    {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }
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

img_caracoles_data = file_to_data_uri(
    img_caracoles_path
)

img_punta_negra_data = file_to_data_uri(
    img_punta_negra_path
)

img_ullum_data = file_to_data_uri(
    img_ullum_path
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

    # --------------------------------------------------------
    # TARJETAS MINA
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # TARJETAS DIQUES
    # --------------------------------------------------------

    caracoles_html = crear_tarjeta_dique(

        titulo="Dique Caracoles",

        texto="""
        Forma parte del sistema de regulación del Río San Juan
        y permite almacenar agua proveniente de la cuenca alta.
        """,

        imagen=img_caracoles_data

    )


    punta_negra_html = crear_tarjeta_dique(

        titulo="Dique Punta Negra",

        texto="""
        Integra el sistema de embalses y participa en la
        regulación del agua que continúa hacia el valle.
        """,

        imagen=img_punta_negra_data

    )


    ullum_html = crear_tarjeta_dique(

        titulo="Dique de Ullum",

        texto="""
        Es una etapa clave antes de la distribución del agua
        hacia los distintos usos de la cuenca baja.
        """,

        imagen=img_ullum_data

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

body {
    margin: 0;
    background: #101820;
    font-family: Arial, Helvetica, sans-serif;
}

.experiencia {
    width: 100%;
    height: 900px;
    position: relative;
    border-radius: 18px;
    overflow: hidden;
    background: #101820;
    box-shadow: 0 18px 45px rgba(0,0,0,0.20);
}


/* =======================================================
   VIDEOS
======================================================= */

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
    background: rgba(0,0,0,0.48);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px;
    backdrop-filter: blur(7px);
    font-size: 18px;
    font-weight: 700;
}


/* =======================================================
   PANTALLAS GENERALES
======================================================= */

.pantalla-contenido {
    display: none;
    width: 100%;
    height: 900px;
    box-sizing: border-box;
    padding: 35px 38px;
    color: white;
    overflow-y: auto;
    animation: aparecer 0.55s ease;
}

.pantalla-mina {
    background:
        __FONDO_MINA__;
    background-size: cover;
    background-position: center;
}

@keyframes aparecer {
    from { opacity: 0; }
    to { opacity: 1; }
}


/* =======================================================
   TÍTULOS
======================================================= */

.titulo-etapa {
    font-size: 14px;
    letter-spacing: 2.4px;
    color: #69d6dd;
    font-weight: 700;
    margin-bottom: 10px;
    text-shadow: 0 2px 7px rgba(0,0,0,0.60);
}

.titulo-principal {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 12px;
    color: white;
    text-shadow: 0 3px 10px rgba(0,0,0,0.70);
}

.descripcion {
    font-size: 17px;
    line-height: 1.6;
    max-width: 1050px;
    margin-bottom: 24px;
    color: white;
    text-shadow: 0 2px 7px rgba(0,0,0,0.80);
}


/* =======================================================
   TARJETAS MINA
======================================================= */

.grid-procesos {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
    margin-top: 18px;
    margin-bottom: 20px;
}

.card-proceso {
    background: rgba(12,22,27,0.52);
    border: 1px solid rgba(255,255,255,0.24);
    border-radius: 17px;
    overflow: hidden;
    backdrop-filter: blur(8px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.22);
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
    background: rgba(255,255,255,0.10);
}

.card-proceso-body {
    padding: 17px 20px 19px;
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


/* =======================================================
   CONCEPTO CLAVE
======================================================= */

.info-clave {
    margin-top: 10px;
    padding: 16px 20px;
    border-radius: 15px;
    background: rgba(10,20,25,0.52);
    border: 1px solid rgba(112,214,222,0.42);
    line-height: 1.55;
    backdrop-filter: blur(8px);
}


/* =======================================================
   BOTONES
======================================================= */

.botones-navegacion {
    display: flex;
    justify-content: center;
    gap: 14px;
    margin-top: 22px;
    flex-wrap: wrap;
}

.btn-principal,
.btn-secundario {
    border: 1px solid rgba(255,255,255,0.28);
    border-radius: 13px;
    padding: 15px 25px;
    color: white;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.25s;
}

.btn-principal {
    background: rgba(22,156,171,0.95);
}

.btn-principal:hover {
    transform: translateY(-3px);
    background: rgba(42,187,199,1);
}

.btn-secundario {
    background: rgba(10,20,25,0.62);
}

.btn-secundario:hover {
    transform: translateY(-3px);
    background: rgba(255,255,255,0.16);
}


/* =======================================================
   DECISIÓN MINA
======================================================= */

.pregunta {
    font-size: 25px;
    font-weight: 700;
    margin-top: 32px;
    margin-bottom: 20px;
}

.opciones {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 17px;
}

.opcion {
    width: 100%;
    box-sizing: border-box;
    text-align: left;
    color: white;
    background: rgba(10,20,25,0.58);
    border: 1px solid rgba(255,255,255,0.24);
    border-radius: 17px;
    padding: 23px;
    backdrop-filter: blur(8px);
    cursor: pointer;
    transition: 0.25s;
    font-family: Arial, Helvetica, sans-serif;
}

.opcion:hover {
    transform: translateY(-5px);
    background: rgba(32,150,161,0.36);
    border-color: #71d9df;
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


/* =======================================================
   RESULTADO MINA
======================================================= */

.resultado-grid {
    display: grid;
    grid-template-columns: 0.85fr 1.15fr;
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
            #e9a23b 0% calc(var(--consumo) * 1%),
            #4dc1d1 calc(var(--consumo) * 1%) 100%
        );
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: 0 18px 45px rgba(0,0,0,0.30);
}

.donut::before {
    content: "";
    width: 205px;
    height: 205px;
    background: rgba(7,19,26,0.94);
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
    grid-template-columns: repeat(3,1fr);
    gap: 12px;
    margin-bottom: 18px;
}

.metrica {
    background: rgba(9,22,29,0.60);
    border: 1px solid rgba(255,255,255,0.18);
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
    background: rgba(9,22,29,0.59);
    border: 1px solid rgba(255,255,255,0.19);
    border-radius: 16px;
    padding: 21px;
    line-height: 1.6;
}

.modelo-educativo {
    margin-top: 18px;
    padding: 14px 17px;
    border-radius: 12px;
    font-size: 13px;
    line-height: 1.5;
    background: rgba(0,0,0,0.40);
    border: 1px solid rgba(255,255,255,0.16);
}


/* =======================================================
   DIQUES
======================================================= */

#info-diques {
    background:
        linear-gradient(
            135deg,
            #102533 0%,
            #17394a 50%,
            #1e5367 100%
        );
}

.grid-diques {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 18px;
    margin-top: 28px;
}

.card-dique {
    background: rgba(5,18,27,0.62);
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 18px;
    overflow: hidden;
    backdrop-filter: blur(8px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.25);
    transition: 0.25s;
}

.card-dique:hover {
    transform: translateY(-5px);
    border-color: #6bd5df;
}

.foto-dique,
.placeholder-dique {
    width: 100%;
    height: 230px;
    object-fit: cover;
}

.placeholder-dique {
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.08);
}

.dique-contenido {
    padding: 20px;
}

.dique-titulo {
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 10px;
}

.dique-texto {
    font-size: 15px;
    line-height: 1.5;
    color: #e8f2f5;
}

.estado-caudal {
    margin-top: 25px;
    padding: 18px 22px;
    border-radius: 15px;
    background: rgba(5,18,27,0.58);
    border: 1px solid rgba(107,213,223,0.35);
    font-size: 16px;
    line-height: 1.55;
}

.aviso-proxima-decision {
    display: none;
    margin-top: 18px;
    padding: 17px;
    border-radius: 14px;
    text-align: center;
    background: rgba(107,213,223,0.14);
    border: 1px solid rgba(107,213,223,0.38);
}


/* =======================================================
   RESPONSIVE
======================================================= */

@media (max-width: 900px) {

    .grid-procesos,
    .opciones,
    .resultado-grid,
    .grid-diques {
        grid-template-columns: 1fr;
    }

    .metricas {
        grid-template-columns: 1fr;
    }

    .titulo-principal {
        font-size: 33px;
    }

}

</style>



<div class="experiencia">


<!-- =====================================================
     VIDEO 1 · CORDILLERA → MINA
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
     INFORMACIÓN MINA
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

        Antes de tomar una decisión, observá cómo
        diferentes formas de gestión pueden modificar
        el consumo neto de agua de una operación minera.

        La recuperación y recirculación permiten reutilizar
        parte del agua utilizada y reducir la necesidad
        de incorporar nuevos aportes.

    </div>

    <div class="grid-procesos">

        __TRADICIONAL__

        __MODERNO__

    </div>

    <div class="info-clave">

        <strong>💡 Concepto clave:</strong>

        una mayor eficiencia en recuperación y recirculación
        disminuye la necesidad de incorporar agua fresca.

    </div>

    <div class="botones-navegacion">

        <button
            id="btn-repetir-1-info"
            class="btn-secundario"
        >
            ↻ Reproducir recorrido
        </button>

        <button
            id="btn-ir-decision"
            class="btn-principal"
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

        Para este modelo educativo se considera
        una demanda equivalente al 25 % del caudal inicial.

        La cantidad realmente consumida dependerá
        de cuánto pueda recuperarse y recircularse.

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
                Consumo neto equivalente:
                aproximadamente 5 %.
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
                Consumo neto equivalente:
                aproximadamente 10 %.
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
                Consumo neto equivalente:
                25 %.
            </span>

        </button>

    </div>

    <div class="botones-navegacion">

        <button
            id="btn-volver-info"
            class="btn-secundario"
        >
            ← Volver a la información
        </button>

        <button
            id="btn-repetir-1-decision"
            class="btn-secundario"
        >
            ↻ Reproducir recorrido
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
                    style="--consumo: 5;"
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

                El proceso utiliza agua,
                pero parte de ella puede recuperarse
                y volver al circuito.

                <br><br>

                Con la estrategia seleccionada,
                el consumo neto representa

                <strong id="texto-consumo">
                    5 %
                </strong>

                del caudal inicial normalizado.

                <br><br>

                Por lo tanto,

                <strong id="texto-restante">
                    95 %
                </strong>

                continúa disponible para seguir
                hacia el sistema de embalses.

            </div>


            <div class="modelo-educativo">

                <strong>
                    ℹ️ Modelo educativo simplificado:
                </strong>

                los porcentajes se utilizan para visualizar
                la relación entre demanda, recuperación
                y consumo neto.

                No representan directamente el porcentaje real
                del Río San Juan utilizado por una mina específica.

            </div>

        </div>


    </div>


    <div class="botones-navegacion">

        <button
            id="btn-cambiar-decision"
            class="btn-secundario"
        >
            ← Cambiar decisión
        </button>

        <button
            id="btn-repetir-1-resultado"
            class="btn-secundario"
        >
            ↻ Reproducir recorrido
        </button>

        <button
            id="btn-continuar-diques"
            class="btn-principal"
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
     INFORMACIÓN DIQUES
===================================================== -->

<div
    id="info-diques"
    class="pantalla-contenido"
>

    <div class="titulo-etapa">
        PARADA 2 · SISTEMA DE EMBALSES
    </div>

    <div class="titulo-principal">
        🏞️ Regulación y almacenamiento del agua
    </div>

    <div class="descripcion">

        El agua continúa su recorrido hacia el sistema
        de embalses del Río San Juan.

        Los diques permiten almacenar y regular el recurso
        antes de su posterior distribución hacia la cuenca baja.

    </div>


    <div class="grid-diques">

        __CARACOLES__

        __PUNTA_NEGRA__

        __ULLUM__

    </div>


    <div class="estado-caudal">

        🌊 <strong>Estado actual del recorrido:</strong>

        luego de la decisión tomada en la mina,
        permanece disponible aproximadamente

        <strong id="caudal-llegada-diques">
            95 %
        </strong>

        del caudal inicial normalizado.

    </div>


    <div class="botones-navegacion">

        <button
            id="btn-volver-resultado-mina"
            class="btn-secundario"
        >
            ← Volver al resultado de la mina
        </button>

        <button
            id="btn-repetir-2"
            class="btn-secundario"
        >
            ↻ Reproducir Mina → Diques
        </button>

        <button
            id="btn-proxima-decision"
            class="btn-principal"
        >
            Continuar →
        </button>

    </div>


    <div
        id="aviso-proxima-decision"
        class="aviso-proxima-decision"
    >

        ✅ Llegaste a la <strong>Parada 2</strong>.

        <br><br>

        El próximo paso será definir
        la decisión de operación de los embalses
        y cómo esa decisión modificará
        el agua disponible aguas abajo.

    </div>

</div>



</div>



<script>


// ==========================================================
// VARIABLES DEL ESTADO
// ==========================================================

let decisionActual = null;

let recirculacionActual = 0;

let consumoActual = 0;

let restanteActual = 100;


// ==========================================================
// PANTALLAS
// ==========================================================

const video1Screen =
    document.getElementById("video-1-screen");

const infoMina =
    document.getElementById("info-mina");

const decisionMina =
    document.getElementById("decision-mina");

const resultadoMina =
    document.getElementById("resultado-mina");

const video2Screen =
    document.getElementById("video-2-screen");

const infoDiques =
    document.getElementById("info-diques");


// ==========================================================
// VIDEOS
// ==========================================================

const video1 =
    document.getElementById("video-1");

const video2 =
    document.getElementById("video-2");


// ==========================================================
// OCULTAR TODO
// ==========================================================

function ocultarTodo() {

    video1Screen.style.display = "none";

    infoMina.style.display = "none";

    decisionMina.style.display = "none";

    resultadoMina.style.display = "none";

    video2Screen.style.display = "none";

    infoDiques.style.display = "none";

}


// ==========================================================
// MOSTRAR PANTALLAS
// ==========================================================

function mostrarInfoMina() {

    ocultarTodo();

    infoMina.style.display = "block";

}


function mostrarDecisionMina() {

    ocultarTodo();

    decisionMina.style.display = "block";

}


function mostrarResultadoMina() {

    ocultarTodo();

    resultadoMina.style.display = "block";

}


function mostrarInfoDiques() {

    ocultarTodo();

    infoDiques.style.display = "block";

    document.getElementById(
        "caudal-llegada-diques"
    ).textContent =
        restanteActual + " %";

}


// ==========================================================
// REPRODUCIR VIDEO 1
// ==========================================================

function reproducirVideo1() {

    ocultarTodo();

    video1Screen.style.display = "block";

    video1.currentTime = 0;

    video1.play();

}


// ==========================================================
// REPRODUCIR VIDEO 2
// ==========================================================

function reproducirVideo2() {

    ocultarTodo();

    video2Screen.style.display = "block";

    video2.currentTime = 0;

    video2.play();

}


// ==========================================================
// FIN VIDEO 1
// ==========================================================

video1.addEventListener(
    "ended",
    function() {

        mostrarInfoMina();

    }
);


// ==========================================================
// FIN VIDEO 2
// ==========================================================

video2.addEventListener(
    "ended",
    function() {

        mostrarInfoDiques();

    }
);


// ==========================================================
// DECISIÓN MINA
// ==========================================================

function seleccionarDecision(tipo) {


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


    else if (tipo === "media") {

        decisionActual =
            "Recirculación intermedia";

        recirculacionActual =
            60;

        consumoActual =
            10;

        restanteActual =
            90;

    }


    else if (tipo === "nula") {

        decisionActual =
            "Sin recirculación";

        recirculacionActual =
            0;

        consumoActual =
            25;

        restanteActual =
            75;

    }


    actualizarResultado();

    mostrarResultadoMina();

}


// ==========================================================
// ACTUALIZAR RESULTADO
// ==========================================================

function actualizarResultado() {


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


// ==========================================================
// BOTONES MINA
// ==========================================================

document.getElementById(
    "btn-ir-decision"
).addEventListener(
    "click",
    function() {

        mostrarDecisionMina();

    }
);


document.getElementById(
    "btn-repetir-1-info"
).addEventListener(
    "click",
    reproducirVideo1
);


document.getElementById(
    "btn-volver-info"
).addEventListener(
    "click",
    mostrarInfoMina
);


document.getElementById(
    "btn-repetir-1-decision"
).addEventListener(
    "click",
    reproducirVideo1
);


document.getElementById(
    "btn-cambiar-decision"
).addEventListener(
    "click",
    mostrarDecisionMina
);


document.getElementById(
    "btn-repetir-1-resultado"
).addEventListener(
    "click",
    reproducirVideo1
);


// ==========================================================
// RESULTADO → VIDEO 2
// ==========================================================

document.getElementById(
    "btn-continuar-diques"
).addEventListener(
    "click",
    function() {

        reproducirVideo2();

    }
);


// ==========================================================
// BOTONES DIQUES
// ==========================================================

document.getElementById(
    "btn-volver-resultado-mina"
).addEventListener(
    "click",
    mostrarResultadoMina
);


document.getElementById(
    "btn-repetir-2"
).addEventListener(
    "click",
    reproducirVideo2
);


document.getElementById(
    "btn-proxima-decision"
).addEventListener(
    "click",
    function() {

        document.getElementById(
            "aviso-proxima-decision"
        ).style.display =
            "block";

    }
);


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


    # ========================================================
    # MOSTRAR COMPONENTE
    # ========================================================

    st.components.v1.html(
        html,
        height=920,
        scrolling=False
    )