import streamlit as st
from pathlib import Path
import base64
import mimetypes

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
        f"El escenario {escenario} todavía no tiene "
        "cargada la experiencia audiovisual."
    )

    if st.button("← Volver"):

        st.switch_page(
            "pages/1_Simulador.py"
        )

    st.stop()


# ============================================================
# RUTAS
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

    st.code(
        str(video_path)
    )

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
# PANTALLA DE INICIO
# ============================================================

if not st.session_state.experiencia_iniciada:

    st.markdown(
        """
        La cuenca inicia con una **alta disponibilidad hídrica**.

        El recorrido comenzará en la **Cordillera de los Andes**
        y seguirá el curso del **Río San Juan** hasta la primera
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
    # TARJETAS
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

        imagen=img_tradicional_data_uri

    )


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


    # ========================================================
    # FONDO
    # ========================================================

    if fondo_mina_data_uri:

        fondo_css = f"""
        linear-gradient(
            90deg,
            rgba(0,0,0,0.48) 0%,
            rgba(0,0,0,0.34) 48%,
            rgba(0,0,0,0.20) 100%
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


    # ========================================================
    # HTML COMPLETO
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

    -webkit-backdrop-filter:
        blur(7px);

    font-size: 18px;

    font-weight: 600;

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

    overflow-y: auto;

    animation:
        aparecer 0.55s ease;

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

    backdrop-filter:
        blur(8px);

    -webkit-backdrop-filter:
        blur(8px);

    box-shadow:
        0 10px 25px
        rgba(0,0,0,0.22);

}


.foto-proceso {

    width: 100%;

    height: 200px;

    object-fit: cover;

    display: block;

}


.placeholder-foto {

    height: 200px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(255,255,255,0.10);

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
        rgba(10,20,25,0.52);

    border:
        1px solid
        rgba(112,214,222,0.42);

    line-height: 1.55;

    backdrop-filter:
        blur(8px);

}



/* =========================================================
   BOTONES DE NAVEGACIÓN
========================================================= */

.botones-navegacion {

    display: flex;

    justify-content: center;

    align-items: center;

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
        rgba(10,20,25,0.62);

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

    backdrop-filter:
        blur(8px);

    -webkit-backdrop-filter:
        blur(8px);

    box-shadow:
        0 9px 24px
        rgba(0,0,0,0.22);

    transition:
        0.25s;

    cursor: pointer;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

}


.opcion:hover {

    transform:
        translateY(-5px);

    background:
        rgba(32,150,161,0.36);

    border-color:
        #71d9df;

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

}


.donut-texto {

    margin-top: 8px;

    font-size: 15px;

    color: #cdebf0;

    max-width: 140px;

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
        repeat(3, 1fr);

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

    backdrop-filter:
        blur(8px);

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

    backdrop-filter:
        blur(8px);

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

    border:
        1px solid
        rgba(255,255,255,0.16);

    color: #dce7ea;

}



/* =========================================================
   MENSAJE SIGUIENTE TRAMO
========================================================= */

.siguiente-panel {

    display: none;

    margin-top: 18px;

    padding: 18px;

    text-align: center;

    border-radius: 13px;

    background:
        rgba(76,193,209,0.18);

    border:
        1px solid
        rgba(76,193,209,0.45);

}



/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {

    .grid-procesos,
    .opciones,
    .resultado-grid {

        grid-template-columns:
            1fr;

    }


    .metricas {

        grid-template-columns:
            1fr;

    }


    .titulo-mina {

        font-size: 33px;

    }


    .donut {

        width: 250px;

        height: 250px;

    }


    .donut::before {

        width: 165px;

        height: 165px;

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
        autoplay
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

        <button
            id="btn-repetir-info"
            class="btn-secundario"
        >

            ↻ Volver a reproducir la simulación

        </button>


        <button
            id="btn-ir-decision"
            class="btn-principal"
        >

            Continuar a la toma de decisión →

        </button>

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

        Para este modelo educativo se considera que
        el proceso requiere un volumen equivalente al
        <strong>25 % del caudal inicial</strong>.

        La cantidad realmente consumida dependerá de
        cuánto de ese volumen pueda recuperarse y reutilizarse.

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

                Alta recuperación y reutilización.

                El consumo neto equivalente será
                aproximadamente 5 % del caudal inicial.

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

                Recuperación parcial.

                El consumo neto equivalente será
                aproximadamente 10 % del caudal inicial.

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

                Todo el requerimiento se cubre
                mediante nuevos aportes.

                El consumo neto equivalente será 25 %.

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
            id="btn-repetir-decision"
            class="btn-secundario"
        >

            ↻ Reproducir recorrido

        </button>

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

        <strong id="resultado-titulo">
            -
        </strong>

        <br>

        La visualización muestra la relación entre
        recirculación, consumo neto y disponibilidad
        de agua para continuar aguas abajo.

    </div>



    <div class="resultado-grid">


        <!-- =========================================
             DONUT
        ========================================== -->

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



        <!-- =========================================
             DATOS
        ========================================== -->

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

                        Consumo neto simulado

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

                <strong>
                    ¿Qué ocurrió?
                </strong>

                <br><br>

                El proceso requiere un volumen equivalente
                al <strong>25 %</strong> del caudal inicial.

                <br><br>

                Con una recirculación del

                <strong id="texto-recirculacion">
                    80 %
                </strong>,

                parte del agua utilizada vuelve
                al circuito.

                <br><br>

                El consumo neto equivalente resulta en

                <strong id="texto-consumo">
                    5 %
                </strong>

                del caudal inicial.

                Por lo tanto,

                <strong id="texto-restante">
                    95 %
                </strong>

                continúa disponible aguas abajo.

            </div>



            <div class="modelo-educativo">

                <strong>
                    ℹ️ Modelo educativo simplificado:
                </strong>

                estos porcentajes son valores normalizados
                utilizados para visualizar la relación
                entre demanda, recuperación y consumo neto.

                No representan directamente el porcentaje
                real del caudal del Río San Juan utilizado
                por una operación minera específica.

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
            id="btn-repetir-resultado"
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



    <div
        id="siguiente-panel"
        class="siguiente-panel"
    >

    </div>


</div>


</div>



<script>


// ==========================================================
// VARIABLES DE LA DECISIÓN
// ==========================================================

let decisionActual = null;

let recirculacionActual = 0;

let consumoActual = 0;

let restanteActual = 100;

let videoSiguiente = "";



// ==========================================================
// ELEMENTOS
// ==========================================================

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



// ==========================================================
// FUNCIONES DE NAVEGACIÓN
// ==========================================================

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


function mostrarVideo() {

    ocultarTodo();

    pantallaVideo.style.display =
        "block";

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

    resultadoMina.style.display =
        "block";

}



// ==========================================================
// REPETIR VIDEO
// ==========================================================

function reproducirDesdeInicio() {

    mostrarVideo();

    video.currentTime = 0;

    const reproduccion =
        video.play();

    if (
        reproduccion !== undefined
    ) {

        reproduccion.catch(
            function(error) {

                console.log(
                    "Autoplay bloqueado:",
                    error
                );

            }
        );

    }

}



// ==========================================================
// DECISIONES
// ==========================================================

function seleccionarDecision(tipo) {


    // ------------------------------------------------------
    // ALTA
    // ------------------------------------------------------

    if (tipo === "alta") {

        decisionActual =
            "Alta recirculación";

        recirculacionActual =
            80;

        consumoActual =
            5;

        restanteActual =
            95;

        videoSiguiente =
            "Caudal_alto.mp4";

    }


    // ------------------------------------------------------
    // MEDIA
    // ------------------------------------------------------

    else if (tipo === "media") {

        decisionActual =
            "Recirculación intermedia";

        recirculacionActual =
            60;

        consumoActual =
            10;

        restanteActual =
            90;

        videoSiguiente =
            "Caudal_medio.mp4";

    }


    // ------------------------------------------------------
    // NULA
    // ------------------------------------------------------

    else if (tipo === "nula") {

        decisionActual =
            "Sin recirculación";

        recirculacionActual =
            0;

        consumoActual =
            25;

        restanteActual =
            75;

        videoSiguiente =
            "Caudal_bajo.mp4";

    }


    // ------------------------------------------------------
    // ACTUALIZAR INTERFAZ
    // ------------------------------------------------------

    actualizarResultado();

    mostrarResultado();

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
        "texto-recirculacion"
    ).textContent =
        recirculacionActual + " %";


    document.getElementById(
        "texto-consumo"
    ).textContent =
        consumoActual + " %";


    document.getElementById(
        "texto-restante"
    ).textContent =
        restanteActual + " %";


    document.getElementById(
        "siguiente-panel"
    ).style.display =
        "none";

}



// ==========================================================
// FIN DEL VIDEO
// ==========================================================

video.addEventListener(
    "ended",
    function() {

        mostrarInformacion();

    }
);



// ==========================================================
// BOTONES INFORMACIÓN
// ==========================================================

document.getElementById(
    "btn-ir-decision"
).addEventListener(
    "click",
    function() {

        mostrarDecision();

    }
);


document.getElementById(
    "btn-repetir-info"
).addEventListener(
    "click",
    function() {

        reproducirDesdeInicio();

    }
);



// ==========================================================
// BOTONES DECISIÓN
// ==========================================================

document.getElementById(
    "btn-volver-info"
).addEventListener(
    "click",
    function() {

        mostrarInformacion();

    }
);


document.getElementById(
    "btn-repetir-decision"
).addEventListener(
    "click",
    function() {

        reproducirDesdeInicio();

    }
);



// ==========================================================
// BOTONES RESULTADO
// ==========================================================

document.getElementById(
    "btn-cambiar-decision"
).addEventListener(
    "click",
    function() {

        mostrarDecision();

    }
);


document.getElementById(
    "btn-repetir-resultado"
).addEventListener(
    "click",
    function() {

        reproducirDesdeInicio();

    }
);


document.getElementById(
    "btn-continuar-diques"
).addEventListener(
    "click",
    function() {

        const panel =
            document.getElementById(
                "siguiente-panel"
            );


        panel.innerHTML =

            "✅ Decisión registrada." +

            "<br><br>" +

            "Caudal disponible: " +

            "<strong>" +
            restanteActual +
            "%</strong>" +

            "<br><br>" +

            "El siguiente tramo utilizará: " +

            "<strong>" +

            "02_Mina_Diques/" +
            videoSiguiente +

            "</strong>";


        panel.style.display =
            "block";


        panel.scrollIntoView({

            behavior:
                "smooth",

            block:
                "nearest"

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


    # ========================================================
    # MOSTRAR
    # ========================================================

    st.components.v1.html(
        html,
        height=920,
        scrolling=False
    )