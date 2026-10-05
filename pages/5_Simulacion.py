import streamlit as st
from pathlib import Path
import base64
import mimetypes

from core.state_manager import init_session_state


# ==================================================
# CONFIGURACIÓN GENERAL
# ==================================================

st.set_page_config(
    page_title="Simulación",
    page_icon="🌊",
    layout="wide"
)

init_session_state()

BASE_DIR = Path(__file__).resolve().parents[1]


# ==================================================
# FUNCIONES AUXILIARES
# ==================================================

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


# ==================================================
# ESCENARIO SELECCIONADO
# ==================================================

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


# ==================================================
# POR AHORA SOLO SUPERAVITARIO
# ==================================================

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


# ==================================================
# RUTAS DE ARCHIVOS
# ==================================================

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


# ==================================================
# COMPROBAR VIDEO
# ==================================================

if not video_path.exists():

    st.error(
        "No se encontró el video Superavitario.mp4"
    )

    st.code(
        str(video_path)
    )

    st.stop()


# ==================================================
# CONVERTIR ARCHIVOS
# ==================================================

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


# ==================================================
# ESTADO DE LA EXPERIENCIA
# ==================================================

if "experiencia_iniciada" not in st.session_state:

    st.session_state.experiencia_iniciada = False


# ==================================================
# ENCABEZADO
# ==================================================

st.title(
    "🌊 Simulación Hídrica"
)

st.markdown(
    f"### Escenario inicial: **{escenario}**"
)


# ==================================================
# PANTALLA INICIAL
# ==================================================

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


# ==================================================
# EXPERIENCIA
# ==================================================

else:

    # ==================================================
    # TARJETA TRADICIONAL
    # ==================================================

    tradicional_html = crear_tarjeta_proceso(

        titulo="Método tradicional abierto",

        subtitulo="MAYOR USO DE AGUA FRESCA",

        texto="""
        En un esquema tradicional con menor recuperación
        interna, una mayor cantidad del agua utilizada debe
        ser reemplazada mediante nuevos aportes desde la cuenca.

        Esto genera un mayor consumo neto de agua.
        """,

        imagen=img_tradicional_data_uri

    )


    # ==================================================
    # TARJETA MODERNA
    # ==================================================

    moderno_html = crear_tarjeta_proceso(

        titulo="Circuito cerrado y recirculación",

        subtitulo="GESTIÓN HÍDRICA MODERNA",

        texto="""
        En operaciones con sistemas de recuperación,
        el agua utilizada puede ser captada, tratada y
        reutilizada nuevamente dentro del proceso.

        Esto disminuye la necesidad de incorporar agua fresca.
        """,

        imagen=img_moderno_data_uri

    )


    # ==================================================
    # FONDO
    # ==================================================

    if fondo_mina_data_uri:

        fondo_css = f"""
        linear-gradient(
            90deg,
            rgba(0, 0, 0, 0.52) 0%,
            rgba(0, 0, 0, 0.38) 45%,
            rgba(0, 0, 0, 0.22) 100%
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


    # ==================================================
    # HTML
    # ==================================================

    html = f"""

    <style>


    /* ==================================================
       GENERAL
    ================================================== */

    body {{

        margin: 0;

        background: #101820;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

    }}


    .experiencia {{

        width: 100%;

        min-height: 900px;

        position: relative;

        border-radius: 18px;

        overflow: hidden;

        background: #101820;

        box-shadow:
            0 18px 45px
            rgba(0,0,0,0.20);

    }}



    /* ==================================================
       VIDEO
    ================================================== */

    #pantalla-video {{

        width: 100%;

        height: 780px;

        position: relative;

        background: black;

    }}


    #video-rio {{

        width: 100%;

        height: 100%;

        object-fit: cover;

        display: block;

    }}


    .etiqueta-video {{

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

    }}



    /* ==================================================
       PANTALLAS MINA
    ================================================== */

    #info-mina,
    #decision-mina {{

        display: none;

        min-height: 900px;

        box-sizing: border-box;

        padding:
            35px 38px;

        color: white;

        background:
            {fondo_css};

        background-size:
            cover;

        background-position:
            center;

        background-repeat:
            no-repeat;

        animation:
            aparecer 0.8s ease;

    }}


    @keyframes aparecer {{

        from {{
            opacity: 0;
        }}

        to {{
            opacity: 1;
        }}

    }}



    /* ==================================================
       TÍTULOS
    ================================================== */

    .titulo-etapa {{

        font-size: 14px;

        letter-spacing: 2.4px;

        color: #69d6dd;

        font-weight: 700;

        margin-bottom: 10px;

        text-shadow:
            0 2px 7px
            rgba(0,0,0,0.55);

    }}


    .titulo-mina {{

        font-size: 42px;

        font-weight: 800;

        margin-bottom: 12px;

        color: white;

        text-shadow:
            0 3px 10px
            rgba(0,0,0,0.65);

    }}


    .descripcion {{

        font-size: 17px;

        line-height: 1.6;

        max-width: 1050px;

        color: white;

        margin-bottom: 24px;

        text-shadow:
            0 2px 7px
            rgba(0,0,0,0.80);

    }}



    /* ==================================================
       TARJETAS
    ================================================== */

    .grid-procesos {{

        display: grid;

        grid-template-columns:
            repeat(2, 1fr);

        gap: 18px;

        margin-top: 18px;

        margin-bottom: 20px;

    }}


    .card-proceso {{

        background:
            rgba(12, 22, 27, 0.52);

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

        transition:
            0.25s;

    }}


    .card-proceso:hover {{

        transform:
            translateY(-3px);

        border-color:
            rgba(110,209,220,0.70);

    }}


    .foto-proceso {{

        width: 100%;

        height: 200px;

        object-fit: cover;

        display: block;

    }}


    .placeholder-foto {{

        width: 100%;

        height: 200px;

        display: flex;

        align-items: center;

        justify-content: center;

        background:
            rgba(255,255,255,0.10);

        color: white;

    }}


    .card-proceso-body {{

        padding:
            17px 20px 19px 20px;

    }}


    .card-subtitle {{

        font-size: 12px;

        letter-spacing: 1.5px;

        color: #75dce2;

        font-weight: 700;

        margin-bottom: 7px;

    }}


    .card-title {{

        font-size: 23px;

        font-weight: 750;

        margin-bottom: 10px;

        color: white;

        text-shadow:
            0 2px 5px
            rgba(0,0,0,0.4);

    }}


    .card-text {{

        font-size: 15px;

        line-height: 1.5;

        color: #f3f3f3;

    }}



    /* ==================================================
       CONCEPTO CLAVE
    ================================================== */

    .info-clave {{

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

        box-shadow:
            0 8px 24px
            rgba(0,0,0,0.18);

    }}



    /* ==================================================
       BOTÓN CONTINUAR
    ================================================== */

    .boton-centro {{

        text-align: center;

        margin-top: 22px;

        margin-bottom: 15px;

    }}


    .btn-continuar {{

        display: inline-block;

        text-decoration: none;

        color: white;

        background:
            rgba(22, 156, 171, 0.95);

        border:
            1px solid
            rgba(255,255,255,0.28);

        border-radius: 13px;

        padding:
            15px 29px;

        font-size: 16px;

        font-weight: 700;

        box-shadow:
            0 8px 22px
            rgba(0,0,0,0.25);

        transition:
            all 0.25s ease;

    }}


    .btn-continuar:hover {{

        transform:
            translateY(-3px);

        background:
            rgba(42, 187, 199, 1);

        box-shadow:
            0 12px 28px
            rgba(0,0,0,0.30);

    }}



    /* ==================================================
       DECISIONES
    ================================================== */

    .pregunta {{

        font-size: 25px;

        font-weight: 700;

        margin-top: 32px;

        margin-bottom: 20px;

        color: white;

        text-shadow:
            0 3px 9px
            rgba(0,0,0,0.70);

    }}


    .opciones {{

        display: grid;

        grid-template-columns:
            repeat(3, 1fr);

        gap: 17px;

    }}


    .opcion {{

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
            all 0.25s ease;

    }}


    .opcion:hover {{

        transform:
            translateY(-5px);

        background:
            rgba(32,150,161,0.32);

        border-color:
            #71d9df;

        box-shadow:
            0 14px 30px
            rgba(0,0,0,0.28);

    }}


    .opcion strong {{

        display: block;

        font-size: 20px;

        margin-bottom: 9px;

        color: white;

    }}


    .opcion span {{

        font-size: 15px;

        line-height: 1.5;

        color: #f0f0f0;

    }}



    /* ==================================================
       RESPONSIVE
    ================================================== */

    @media (max-width: 900px) {{

        .grid-procesos,
        .opciones {{

            grid-template-columns: 1fr;

        }}

        #info-mina,
        #decision-mina {{

            padding: 26px 22px;

        }}

        .titulo-mina {{

            font-size: 33px;

        }}

    }}


    </style>



    <div class="experiencia">


        <!-- ===========================================
             VIDEO
        ============================================ -->

        <div id="pantalla-video">


            <video
                id="video-rio"
                autoplay
                muted
                playsinline
            >

                <source
                    src="{video_data_uri}"
                    type="video/mp4"
                >

            </video>


            <div class="etiqueta-video">

                🏔️ Cordillera → Mina

            </div>


        </div>



        <!-- ===========================================
             INFORMACIÓN MINERA
        ============================================ -->

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

                La recuperación y recirculación permiten
                reutilizar parte del agua utilizada y reducir
                la necesidad de incorporar nuevos aportes.

            </div>



            <div class="grid-procesos">


                {tradicional_html}


                {moderno_html}


            </div>



            <div class="info-clave">

                <strong>💡 Concepto clave:</strong>

                una mayor eficiencia en la recuperación y
                recirculación disminuye la necesidad de
                incorporar agua fresca al proceso.

                Esto reduce el consumo neto de agua de la
                operación y permite conservar una mayor
                disponibilidad del recurso en la cuenca.

            </div>



            <div class="boton-centro">


                <a
                    href="#"
                    id="btn-ir-decision"
                    class="btn-continuar"
                >

                    Continuar a la toma de decisión →

                </a>


            </div>


        </div>



        <!-- ===========================================
             DECISIÓN
        ============================================ -->

        <div id="decision-mina">


            <div class="titulo-etapa">

                PARADA 1 · DECISIÓN

            </div>


            <div class="titulo-mina">

                ♻️ ¿Cómo gestionarías el agua?

            </div>


            <div class="descripcion">

                El Río San Juan ha llegado a la zona minera.

                Ahora deberás seleccionar una estrategia
                de gestión hídrica.

                Tu decisión modificará el caudal disponible
                para continuar el recorrido hacia los diques.

            </div>



            <div class="pregunta">

                ¿Qué estrategia aplicarías?

            </div>



            <div class="opciones">


                <a
                    class="opcion"
                    href="?decision_mina=alta"
                    target="_parent"
                >

                    <strong>

                        ♻️ Alta recirculación

                    </strong>

                    <span>

                        Priorizar la recuperación y
                        reutilización del agua.

                        Menor consumo neto de agua fresca.

                    </span>

                </a>



                <a
                    class="opcion"
                    href="?decision_mina=media"
                    target="_parent"
                >

                    <strong>

                        ⚖️ Recirculación intermedia

                    </strong>

                    <span>

                        Mantener una gestión intermedia
                        entre recuperación y aporte
                        de agua fresca.

                    </span>

                </a>



                <a
                    class="opcion"
                    href="?decision_mina=baja"
                    target="_parent"
                >

                    <strong>

                        💧 Baja recirculación

                    </strong>

                    <span>

                        Mayor incorporación de agua fresca
                        al proceso y mayor consumo neto
                        desde la cuenca.

                    </span>

                </a>


            </div>


        </div>


    </div>



    <script>


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


    const botonDecision =
        document.getElementById(
            "btn-ir-decision"
        );



    // CUANDO TERMINA EL VIDEO
    video.addEventListener(
        "ended",
        function() {{

            pantallaVideo.style.display =
                "none";

            infoMina.style.display =
                "block";

        }}
    );



    // PASAR DE INFORMACIÓN A DECISIÓN
    botonDecision.addEventListener(
        "click",
        function(event) {{

            event.preventDefault();

            infoMina.style.display =
                "none";

            decisionMina.style.display =
                "block";

        }}
    );


    </script>

    """


    # ==================================================
    # MOSTRAR COMPONENTE
    # ==================================================

    st.components.v1.html(
        html,
        height=1050,
        scrolling=False
    )


# ==================================================
# LEER DECISIÓN
# ==================================================

decision = st.query_params.get(
    "decision_mina"
)


if decision:

    decision_anterior = st.session_state.get(
        "decision_mina"
    )

    if decision != decision_anterior:

        st.session_state[
            "decision_mina"
        ] = decision


        # ==================================================
        # MODIFICACIÓN PROVISORIA DEL CAUDAL
        # ==================================================

        if decision == "alta":

            st.session_state.caudal_actual = (
                st.session_state.caudal_actual
                - 5
            )


        elif decision == "media":

            st.session_state.caudal_actual = (
                st.session_state.caudal_actual
                - 10
            )


        elif decision == "baja":

            st.session_state.caudal_actual = (
                st.session_state.caudal_actual
                - 20
            )


    st.query_params.clear()


    st.success(
        f"Decisión registrada: {decision}. "
        f"Caudal actual: "
        f"{st.session_state.caudal_actual}"
    )