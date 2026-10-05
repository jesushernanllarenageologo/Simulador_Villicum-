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

    if not file_path.exists():
        return None

    mime_type, _ = mimetypes.guess_type(str(file_path))

    if mime_type is None:
        mime_type = "application/octet-stream"

    encoded = base64.b64encode(
        file_path.read_bytes()
    ).decode()

    return f"data:{mime_type};base64,{encoded}"


def crear_tarjeta_proceso(
    titulo,
    subtitulo,
    texto,
    imagen
):

    if imagen:

        contenido_imagen = f"""
        <img
            src="{imagen}"
            class="foto-proceso"
        >
        """

    else:

        contenido_imagen = """
        <div class="placeholder-foto">
            Imagen no disponible
        </div>
        """

    return f"""
    <div class="card-proceso">

        {contenido_imagen}

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
# ARCHIVOS
# ============================================================

video_path = (
    BASE_DIR
    / "assets"
    / "videos"
    / "01_Cordillera_Mina"
    / "Superavitario.mp4"
)


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
# COMPROBAR VIDEO
# ============================================================

if not video_path.exists():

    st.error(
        "No se encontró el video Superavitario.mp4"
    )

    st.code(str(video_path))

    st.stop()


# ============================================================
# CONVERTIR ARCHIVOS
# ============================================================

video_data_uri = file_to_data_uri(
    video_path
)

img_moderno_data_uri = file_to_data_uri(
    img_moderno_path
)

img_tradicional_data_uri = file_to_data_uri(
    img_tradicional_path
)

fondo_mina_data_uri = file_to_data_uri(
    fondo_mina_path
)


# ============================================================
# CONFIGURACIÓN EDUCATIVA DE LAS DECISIONES
# ============================================================
#
# Modelo normalizado:
#
# Caudal inicial = 100 %
# Demanda bruta del proceso minero = 25 %
#
# Consumo neto =
# demanda bruta × (1 - recirculación)
#
# Alta:
# 25 × (1 - 0.80) = 5 %
#
# Media:
# 25 × (1 - 0.60) = 10 %
#
# Nula:
# 25 × (1 - 0.00) = 25 %
#
# ============================================================

DECISIONES_MINA = {

    "alta": {

        "titulo": "Alta recirculación",

        "recirculacion": 80,

        "consumo_neto": 5,

        "caudal_restante": 95,

        "video_siguiente": "Caudal_alto.mp4"

    },

    "media": {

        "titulo": "Recirculación intermedia",

        "recirculacion": 60,

        "consumo_neto": 10,

        "caudal_restante": 90,

        "video_siguiente": "Caudal_medio.mp4"

    },

    "nula": {

        "titulo": "Sin recirculación",

        "recirculacion": 0,

        "consumo_neto": 25,

        "caudal_restante": 75,

        "video_siguiente": "Caudal_bajo.mp4"

    }

}


# ============================================================
# ESTADO
# ============================================================

if "experiencia_iniciada" not in st.session_state:

    st.session_state.experiencia_iniciada = False


# Guardamos el caudal con el que el río llega a la mina.
# Así cambiar la decisión no resta agua varias veces.

if "caudal_inicio_mina" not in st.session_state:

    st.session_state.caudal_inicio_mina = float(
        st.session_state.caudal_actual
    )


# ============================================================
# LEER DECISIÓN DESDE URL
# ============================================================

decision_url = st.query_params.get(
    "decision_mina"
)


if decision_url in DECISIONES_MINA:

    configuracion = DECISIONES_MINA[
        decision_url
    ]

    st.session_state.decision_mina = (
        decision_url
    )

    st.session_state.mostrar_resultado_mina = (
        True
    )

    # Recalculamos SIEMPRE desde el caudal inicial
    # de la parada. Así el usuario puede cambiar
    # de decisión sin descontar agua dos veces.

    caudal_base = (
        st.session_state.caudal_inicio_mina
    )

    porcentaje_restante = (
        configuracion["caudal_restante"]
        / 100
    )

    nuevo_caudal = (
        caudal_base
        * porcentaje_restante
    )

    st.session_state.caudal_actual = round(
        nuevo_caudal,
        2
    )


# ============================================================
# RESULTADO ACTUAL
# ============================================================

mostrar_resultado = (
    st.session_state.get(
        "mostrar_resultado_mina",
        False
    )
)


decision_guardada = (
    st.session_state.get(
        "decision_mina"
    )
)


if (
    mostrar_resultado
    and decision_guardada in DECISIONES_MINA
):

    resultado = DECISIONES_MINA[
        decision_guardada
    ]

else:

    resultado = {

        "titulo": "",

        "recirculacion": 0,

        "consumo_neto": 0,

        "caudal_restante": 100,

        "video_siguiente": ""

    }


# ============================================================
# ENCABEZADO STREAMLIT
# ============================================================

st.title(
    "🌊 Simulación Hídrica"
)

st.markdown(
    f"### Escenario inicial: **{escenario}**"
)


# ============================================================
# INICIO
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
# EXPERIENCIA
# ============================================================

else:

    # --------------------------------------------------------
    # TARJETA TRADICIONAL
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

        imagen=img_tradicional_data_uri

    )


    # --------------------------------------------------------
    # TARJETA MODERNA
    # --------------------------------------------------------

    moderno_html = crear_tarjeta_proceso(

        titulo="Circuito cerrado y recirculación",

        subtitulo="GESTIÓN HÍDRICA MODERNA",

        texto="""
        Mediante sistemas de recuperación, parte del agua
        utilizada puede ser captada, tratada y reutilizada
        nuevamente dentro del proceso.

        Esto reduce la necesidad de incorporar agua fresca.
        """,

        imagen=img_moderno_data_uri

    )


    # --------------------------------------------------------
    # FONDO
    # --------------------------------------------------------

    if fondo_mina_data_uri:

        fondo_css = f"""
        linear-gradient(
            90deg,
            rgba(0,0,0,0.52) 0%,
            rgba(0,0,0,0.38) 45%,
            rgba(0,0,0,0.22) 100%
        ),
        url("{fondo_mina_data_uri}")
        """

    else:

        fondo_css = """
        linear-gradient(
            135deg,
            #28343b,
            #50616a
        )
        """


    # --------------------------------------------------------
    # ESTADO INICIAL DEL COMPONENTE
    # --------------------------------------------------------

    if mostrar_resultado:

        estado_inicial = "resultado"

        autoplay_video = ""

    else:

        estado_inicial = "video"

        autoplay_video = "autoplay"


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

    background: #101820;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

}


.experiencia {

    width: 100%;

    height: 900px;

    position: relative;

    border-radius: 18px;

    overflow: hidden;

    background: #101820;

    box-shadow:
        0 18px 45px
        rgba(0,0,0,0.20);

}



/* =========================================================
   VIDEO
========================================================= */

#pantalla-video {

    width: 100%;

    height: 900px;

    position: relative;

    overflow: hidden;

    background: black;

}


#video-rio {

    position: absolute;

    top: 0;

    left: 0;

    width: 100%;

    height: 100%;

    object-fit: cover;

    object-position: center;

    display: block;

}


.etiqueta-video {

    position: absolute;

    top: 30px;

    left: 35px;

    padding: 12px 20px;

    background:
        rgba(0,0,0,0.48);

    color: white;

    border:
        1px solid
        rgba(255,255,255,0.18);

    border-radius: 12px;

    backdrop-filter: blur(7px);

    -webkit-backdrop-filter: blur(7px);

    font-size: 18px;

    font-weight: 600;

    z-index: 5;

}



/* =========================================================
   PANTALLAS
========================================================= */

#info-mina,
#decision-mina,
#resultado-mina {

    display: none;

    width: 100%;

    height: 900px;

    box-sizing: border-box;

    padding:
        35px 38px;

    color: white;

    background:
        __FONDO__;

    background-size:
        cover;

    background-position:
        center;

    background-repeat:
        no-repeat;

    overflow-y:
        auto;

    animation:
        aparecer 0.65s ease;

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

    text-shadow:
        0 2px 7px
        rgba(0,0,0,0.55);

}


.titulo-mina {

    font-size: 42px;

    font-weight: 800;

    margin-bottom: 12px;

    color: white;

    text-shadow:
        0 3px 10px
        rgba(0,0,0,0.65);

}


.descripcion {

    font-size: 17px;

    line-height: 1.6;

    max-width: 1050px;

    color: white;

    margin-bottom: 24px;

    text-shadow:
        0 2px 7px
        rgba(0,0,0,0.80);

}



/* =========================================================
   TARJETAS INFORMATIVAS
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

    backdrop-filter: blur(8px);

    -webkit-backdrop-filter:
        blur(8px);

    box-shadow:
        0 10px 25px
        rgba(0,0,0,0.22);

    transition:
        0.25s;

}


.card-proceso:hover {

    transform:
        translateY(-3px);

    border-color:
        rgba(110,209,220,0.70);

}


.foto-proceso {

    width: 100%;

    height: 200px;

    object-fit: cover;

    display: block;

}


.placeholder-foto {

    width: 100%;

    height: 200px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(255,255,255,0.10);

    color: white;

}


.card-proceso-body {

    padding:
        17px 20px 19px 20px;

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

    color: white;

}


.card-text {

    font-size: 15px;

    line-height: 1.5;

    color: #f3f3f3;

}



/* =========================================================
   CONCEPTO CLAVE
========================================================= */

.info-clave {

    margin-top: 10px;

    padding:
        16px 20px;

    border-radius: 15px;

    background:
        rgba(10,20,25,0.50);

    border:
        1px solid
        rgba(112,214,222,0.42);

    color: white;

    line-height: 1.55;

    backdrop-filter:
        blur(8px);

    -webkit-backdrop-filter:
        blur(8px);

}



/* =========================================================
   BOTONES
========================================================= */

.botones-navegacion {

    display: flex;

    justify-content: center;

    align-items: center;

    gap: 14px;

    margin-top: 22px;

    margin-bottom: 15px;

    flex-wrap: wrap;

}


.btn-principal,
.btn-secundario {

    display: inline-block;

    text-decoration: none;

    color: white;

    border:
        1px solid
        rgba(255,255,255,0.28);

    border-radius: 13px;

    padding:
        15px 25px;

    font-size: 16px;

    font-weight: 700;

    cursor: pointer;

    transition:
        0.25s;

}


.btn-principal {

    background:
        rgba(22,156,171,0.95);

}


.btn-principal:hover {

    transform:
        translateY(-3px);

    background:
        rgba(42,187,199,1);

}


.btn-secundario {

    background:
        rgba(10,20,25,0.58);

    backdrop-filter:
        blur(8px);

}


.btn-secundario:hover {

    transform:
        translateY(-3px);

    background:
        rgba(255,255,255,0.16);

}



/* =========================================================
   DECISIONES
========================================================= */

.pregunta {

    font-size: 25px;

    font-weight: 700;

    margin-top: 32px;

    margin-bottom: 20px;

    color: white;

    text-shadow:
        0 3px 9px
        rgba(0,0,0,0.70);

}


.opciones {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 17px;

}


.opcion {

    display: block;

    text-decoration: none;

    color: white;

    background:
        rgba(10,20,25,0.50);

    border:
        1px solid
        rgba(255,255,255,0.24);

    border-radius: 17px;

    padding: 23px;

    backdrop-filter:
        blur(8px);

    -webkit-backdrop-filter:
        blur(8px);

    box-shadow:
        0 9px 24px
        rgba(0,0,0,0.22);

    transition:
        0.25s;

}


.opcion:hover {

    transform:
        translateY(-5px);

    background:
        rgba(32,150,161,0.32);

    border-color:
        #71d9df;

}


.opcion strong {

    display: block;

    font-size: 20px;

    margin-bottom: 9px;

}


.opcion span {

    font-size: 15px;

    line-height: 1.5;

    color: #f0f0f0;

}



/* =========================================================
   RESULTADO
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

    align-items: center;

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

    box-shadow:
        0 18px 45px
        rgba(0,0,0,0.30);

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

    border:
        1px solid
        rgba(255,255,255,0.12);

}


.donut-centro {

    position: relative;

    z-index: 3;

    text-align: center;

}


.donut-numero {

    font-size: 54px;

    font-weight: 800;

    line-height: 1;

    color: white;

}


.donut-texto {

    margin-top: 8px;

    font-size: 15px;

    color: #cdebf0;

    max-width: 130px;

}


.leyenda {

    display: flex;

    justify-content: center;

    gap: 25px;

    margin-top: 18px;

    font-size: 14px;

}


.punto {

    width: 12px;

    height: 12px;

    display: inline-block;

    border-radius: 3px;

    margin-right: 6px;

}


.punto-consumo {

    background:
        #e9a23b;

}


.punto-restante {

    background:
        #4dc1d1;

}



/* =========================================================
   MÉTRICAS
========================================================= */

.metricas {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 12px;

    margin-bottom: 18px;

}


.metrica {

    background:
        rgba(9,22,29,0.57);

    border:
        1px solid
        rgba(255,255,255,0.18);

    padding: 18px;

    border-radius: 14px;

    backdrop-filter:
        blur(8px);

}


.metrica-numero {

    font-size: 31px;

    font-weight: 800;

    color: white;

}


.metrica-label {

    font-size: 13px;

    color: #cde0e5;

    margin-top: 4px;

}


.resultado-explicacion {

    background:
        rgba(9,22,29,0.55);

    border:
        1px solid
        rgba(255,255,255,0.19);

    border-radius: 16px;

    padding: 21px;

    line-height: 1.6;

    color: white;

    backdrop-filter:
        blur(8px);

}


.modelo-educativo {

    margin-top: 18px;

    padding: 14px 17px;

    border-radius: 12px;

    font-size: 13px;

    line-height: 1.5;

    background:
        rgba(0,0,0,0.36);

    border:
        1px solid
        rgba(255,255,255,0.16);

    color: #dce7ea;

}


.siguiente-panel {

    display: none;

    margin-top: 18px;

    padding: 17px;

    text-align: center;

    border-radius: 13px;

    background:
        rgba(76,193,209,0.16);

    border:
        1px solid
        rgba(76,193,209,0.42);

}



/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {

    .grid-procesos,
    .opciones,
    .resultado-grid {

        grid-template-columns: 1fr;

    }


    .metricas {

        grid-template-columns: 1fr;

    }


    .donut {

        width: 250px;

        height: 250px;

    }


    .donut::before {

        width: 165px;

        height: 165px;

    }


    .titulo-mina {

        font-size: 33px;

    }

}

</style>



<div class="experiencia">


<!-- =====================================================
     VIDEO
===================================================== -->

<div id="pantalla-video">

    <video
        id="video-rio"
        __AUTOPLAY__
        muted
        playsinline
    >

        <source
            src="__VIDEO_DATA__"
            type="video/mp4"
        >

    </video>


    <div class="etiqueta-video">

        🏔️ Cordillera → Mina

    </div>

</div>



<!-- =====================================================
     INFORMACIÓN
===================================================== -->

<div id="info-mina">

    <div class="titulo-etapa">

        PARADA 1 · CUENCA ALTA

    </div>


    <div class="titulo-mina">

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

        Por lo tanto, el consumo neto de la operación puede
        reducirse significativamente.

    </div>


    <div class="botones-navegacion">

        <a
            href="#"
            id="btn-repetir-info"
            class="btn-secundario"
        >

            ↻ Volver a reproducir la simulación

        </a>


        <a
            href="#"
            id="btn-ir-decision"
            class="btn-principal"
        >

            Continuar a la toma de decisión →

        </a>

    </div>

</div>



<!-- =====================================================
     DECISIÓN
===================================================== -->

<div id="decision-mina">

    <div class="titulo-etapa">

        PARADA 1 · DECISIÓN

    </div>


    <div class="titulo-mina">

        ♻️ ¿Cómo gestionarías el agua?

    </div>


    <div class="descripcion">

        Para este modelo educativo se considera que el
        proceso requiere un volumen equivalente al 25 %
        del caudal inicial.

        La cantidad realmente consumida dependerá de
        cuánto de ese volumen pueda recuperarse y reutilizarse.

    </div>


    <div class="pregunta">

        Seleccioná una estrategia

    </div>


    <div class="opciones">


        <a
            class="opcion"
            href="?decision_mina=alta"
            target="_parent"
        >

            <strong>

                ♻️ Alta recirculación · 80 %

            </strong>

            <span>

                Alta recuperación y reutilización.

                El consumo neto equivalente será
                aproximadamente 5 % del caudal inicial.

            </span>

        </a>



        <a
            class="opcion"
            href="?decision_mina=media"
            target="_parent"
        >

            <strong>

                ⚖️ Recirculación intermedia · 60 %

            </strong>

            <span>

                Recuperación parcial del agua.

                El consumo neto equivalente será
                aproximadamente 10 % del caudal inicial.

            </span>

        </a>



        <a
            class="opcion"
            href="?decision_mina=nula"
            target="_parent"
        >

            <strong>

                💧 Sin recirculación · 0 %

            </strong>

            <span>

                Todo el requerimiento se cubre mediante
                nuevos aportes de agua.

                El consumo neto equivalente será 25 %.

            </span>

        </a>


    </div>


    <div class="botones-navegacion">

        <a
            href="#"
            id="btn-volver-info"
            class="btn-secundario"
        >

            ← Volver a la información

        </a>


        <a
            href="#"
            id="btn-repetir-decision"
            class="btn-secundario"
        >

            ↻ Reproducir recorrido

        </a>

    </div>

</div>



<!-- =====================================================
     RESULTADO
===================================================== -->

<div id="resultado-mina">

    <div class="titulo-etapa">

        RESULTADO · PARADA 1

    </div>


    <div class="titulo-mina">

        📊 Impacto de tu decisión

    </div>


    <div class="descripcion">

        Elegiste:

        <strong>
            __RESULTADO_TITULO__
        </strong>

        La siguiente visualización muestra cómo se
        distribuye el caudal inicial normalizado después
        de considerar el consumo neto de la mina.

    </div>



    <div class="resultado-grid">


        <!-- GRÁFICO -->

        <div>


            <div class="donut-wrapper">

                <div
                    class="donut"
                    style="
                        --consumo:
                        __RESULTADO_CONSUMO__;
                    "
                >

                    <div class="donut-centro">

                        <div class="donut-numero">

                            __RESULTADO_RESTANTE__%

                        </div>

                        <div class="donut-texto">

                            continúa disponible
                            aguas abajo

                        </div>

                    </div>

                </div>

            </div>


            <div class="leyenda">

                <div>

                    <span
                        class="
                            punto
                            punto-restante
                        "
                    ></span>

                    Caudal restante

                </div>


                <div>

                    <span
                        class="
                            punto
                            punto-consumo
                        "
                    ></span>

                    Consumo neto

                </div>

            </div>


        </div>



        <!-- DATOS -->

        <div>


            <div class="metricas">


                <div class="metrica">

                    <div class="metrica-numero">

                        __RESULTADO_RECIRC__%

                    </div>

                    <div class="metrica-label">

                        Recirculación seleccionada

                    </div>

                </div>



                <div class="metrica">

                    <div class="metrica-numero">

                        -__RESULTADO_CONSUMO__%

                    </div>

                    <div class="metrica-label">

                        Consumo neto simulado

                    </div>

                </div>



                <div class="metrica">

                    <div class="metrica-numero">

                        __RESULTADO_RESTANTE__%

                    </div>

                    <div class="metrica-label">

                        Caudal disponible

                    </div>

                </div>


            </div>



            <div class="resultado-explicacion">

                <strong>
                    ¿Qué ocurrió?
                </strong>

                <br><br>

                El proceso requiere un volumen equivalente
                al <strong>25 %</strong> del caudal inicial.

                Con una recirculación del

                <strong>
                    __RESULTADO_RECIRC__ %
                </strong>,

                una parte importante del agua utilizada
                vuelve al circuito.

                <br><br>

                El consumo neto equivalente resulta en

                <strong>
                    __RESULTADO_CONSUMO__ %
                </strong>

                del caudal inicial.

                Por lo tanto,

                <strong>
                    __RESULTADO_RESTANTE__ %
                </strong>

                continúa disponible para el siguiente tramo
                de la cuenca.

            </div>



            <div class="modelo-educativo">

                <strong>
                    ℹ️ Modelo educativo simplificado:
                </strong>

                los porcentajes representan valores
                normalizados utilizados para mostrar
                la relación entre demanda, recuperación
                y consumo neto.

                No representan directamente el porcentaje
                real del caudal del Río San Juan utilizado
                por una operación minera específica.

            </div>


        </div>


    </div>



    <div class="botones-navegacion">


        <a
            href="#"
            id="btn-cambiar-decision"
            class="btn-secundario"
        >

            ← Cambiar decisión

        </a>


        <a
            href="#"
            id="btn-repetir-resultado"
            class="btn-secundario"
        >

            ↻ Reproducir recorrido

        </a>


        <a
            href="#"
            id="btn-continuar-diques"
            class="btn-principal"
        >

            Continuar hacia los diques →

        </a>


    </div>



    <div
        id="siguiente-panel"
        class="siguiente-panel"
    >

        ✅ Resultado registrado.

        <br><br>

        El siguiente tramo utilizará:

        <strong>
            02_Mina_Diques/__VIDEO_SIGUIENTE__
        </strong>

    </div>


</div>



</div>



<script>

/* =========================================================
   ELEMENTOS
========================================================= */

const video =
    document.getElementById(
        "video-rio"
    );


const pantallaVideo =
    document.getElementById(
        "pantalla-video"
    );


const infoMina =
    document.getElementById(
        "info-mina"
    );


const decisionMina =
    document.getElementById(
        "decision-mina"
    );


const resultadoMina =
    document.getElementById(
        "resultado-mina"
    );


const btnDecision =
    document.getElementById(
        "btn-ir-decision"
    );


const btnRepetirInfo =
    document.getElementById(
        "btn-repetir-info"
    );


const btnVolverInfo =
    document.getElementById(
        "btn-volver-info"
    );


const btnRepetirDecision =
    document.getElementById(
        "btn-repetir-decision"
    );


const btnCambiarDecision =
    document.getElementById(
        "btn-cambiar-decision"
    );


const btnRepetirResultado =
    document.getElementById(
        "btn-repetir-resultado"
    );


const btnContinuarDiques =
    document.getElementById(
        "btn-continuar-diques"
    );


const siguientePanel =
    document.getElementById(
        "siguiente-panel"
    );



/* =========================================================
   FUNCIONES
========================================================= */

function ocultarTodo() {

    pantallaVideo.style.display =
        "none";

    infoMina.style.display =
        "none";

    decisionMina.style.display =
        "none";

    resultadoMina.style.display =
        "none";

}


function reproducirDesdeInicio() {

    ocultarTodo();

    pantallaVideo.style.display =
        "block";

    video.currentTime = 0;

    video.play();

}


function mostrarInformacion() {

    ocultarTodo();

    infoMina.style.display =
        "block";

}


function mostrarDecision() {

    ocultarTodo();

    decisionMina.style.display =
        "block";

}


function mostrarResultado() {

    ocultarTodo();

    video.pause();

    resultadoMina.style.display =
        "block";

}



/* =========================================================
   ESTADO INICIAL
========================================================= */

const estadoInicial =
    "__ESTADO_INICIAL__";


if (
    estadoInicial ===
    "resultado"
) {

    mostrarResultado();

}

else {

    pantallaVideo.style.display =
        "block";

}



/* =========================================================
   FIN DEL VIDEO
========================================================= */

video.addEventListener(
    "ended",
    function() {

        mostrarInformacion();

    }
);



/* =========================================================
   INFORMACIÓN → DECISIÓN
========================================================= */

btnDecision.addEventListener(
    "click",
    function(event) {

        event.preventDefault();

        mostrarDecision();

    }
);



/* =========================================================
   REPETIR DESDE INFORMACIÓN
========================================================= */

btnRepetirInfo.addEventListener(
    "click",
    function(event) {

        event.preventDefault();

        reproducirDesdeInicio();

    }
);



/* =========================================================
   DECISIÓN → INFORMACIÓN
========================================================= */

btnVolverInfo.addEventListener(
    "click",
    function(event) {

        event.preventDefault();

        mostrarInformacion();

    }
);



/* =========================================================
   REPETIR DESDE DECISIÓN
========================================================= */

btnRepetirDecision.addEventListener(
    "click",
    function(event) {

        event.preventDefault();

        reproducirDesdeInicio();

    }
);



/* =========================================================
   RESULTADO → CAMBIAR DECISIÓN
========================================================= */

btnCambiarDecision.addEventListener(
    "click",
    function(event) {

        event.preventDefault();

        mostrarDecision();

    }
);



/* =========================================================
   REPETIR DESDE RESULTADO
========================================================= */

btnRepetirResultado.addEventListener(
    "click",
    function(event) {

        event.preventDefault();

        reproducirDesdeInicio();

    }
);



/* =========================================================
   CONTINUAR HACIA DIQUES
========================================================= */

btnContinuarDiques.addEventListener(
    "click",
    function(event) {

        event.preventDefault();

        siguientePanel.style.display =
            "block";

        siguientePanel.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

    }
);

</script>

"""


    # ========================================================
    # REEMPLAZOS
    # ========================================================

    html = html_template

    html = html.replace(
        "__FONDO__",
        fondo_css
    )

    html = html.replace(
        "__VIDEO_DATA__",
        video_data_uri or ""
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
        "__AUTOPLAY__",
        autoplay_video
    )

    html = html.replace(
        "__ESTADO_INICIAL__",
        estado_inicial
    )


    # RESULTADO

    html = html.replace(
        "__RESULTADO_TITULO__",
        str(resultado["titulo"])
    )

    html = html.replace(
        "__RESULTADO_RECIRC__",
        str(resultado["recirculacion"])
    )

    html = html.replace(
        "__RESULTADO_CONSUMO__",
        str(resultado["consumo_neto"])
    )

    html = html.replace(
        "__RESULTADO_RESTANTE__",
        str(resultado["caudal_restante"])
    )

    html = html.replace(
        "__VIDEO_SIGUIENTE__",
        str(resultado["video_siguiente"])
    )


    # ========================================================
    # MOSTRAR COMPONENTE
    # ========================================================

    st.components.v1.html(
        html,
        height=920,
        scrolling=False
    )