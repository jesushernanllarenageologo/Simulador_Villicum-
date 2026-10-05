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
    """
    Convierte videos e imágenes locales a formato Data URI
    para utilizarlos dentro del HTML.
    """

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
# POR AHORA SOLO PROBAMOS SUPERAVITARIO
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

# VIDEO CORDILLERA → MINA

video_path = (
    BASE_DIR
    / "assets"
    / "videos"
    / "01_Cordillera_Mina"
    / "Superavitario.mp4"
)


# FOTO MÉTODO MODERNO

img_moderno_path = (
    BASE_DIR
    / "assets"
    / "images"
    / "mina"
    / "metodo_moderno_recirculacion.jpg"
)


# FOTO MÉTODO TRADICIONAL

img_tradicional_path = (
    BASE_DIR
    / "assets"
    / "images"
    / "mina"
    / "metodo_tradicional_abierto.jpg"
)


# FONDO GENERAL DE LA MINA

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
# CONVERTIR ARCHIVOS A DATA URI
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
# ENCABEZADO STREAMLIT
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

    # ------------------------------------------------
    # TARJETA MÉTODO TRADICIONAL
    # ------------------------------------------------

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


    # ------------------------------------------------
    # TARJETA MÉTODO MODERNO
    # ------------------------------------------------

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


    # ------------------------------------------------
    # SI NO EXISTE FONDO, USAR COLOR
    # ------------------------------------------------

    if fondo_mina_data_uri:

        fondo_css = f"""
        linear-gradient(
            90deg,
            rgba(4,14,23,0.91) 0%,
            rgba(4,14,23,0.77) 45%,
            rgba(4,14,23,0.50) 100%
        ),
        url("{fondo_mina_data_uri}")
        """

    else:

        fondo_css = """
        linear-gradient(
            135deg,
            #071722,
            #183241
        )
        """


    # ==================================================
    # HTML COMPLETO
    # ==================================================

    html = f"""

    <style>


    /* ==================================================
       GENERAL
    ================================================== */

    body {{

        margin: 0;

        background:
            #071722;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

    }}


    .experiencia {{

        width: 100%;

        min-height: 780px;

        position: relative;

        border-radius: 18px;

        overflow: hidden;

        background: #071722;

        box-shadow:
            0 18px 45px
            rgba(0,0,0,0.25);

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

        padding:
            12px 20px;

        background:
            rgba(3,14,23,0.70);

        color: white;

        border:
            1px solid
            rgba(255,255,255,0.15);

        border-radius: 12px;

        backdrop-filter:
            blur(9px);

        -webkit-backdrop-filter:
            blur(9px);

        font-size: 18px;

        font-weight: 600;

    }}



    /* ==================================================
       PANTALLAS MINA
    ================================================== */

    #info-mina,
    #decision-mina {{

        display: none;

        min-height: 780px;

        box-sizing: border-box;

        padding:
            42px 48px;

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

        color: #6ed1dc;

        font-weight: 700;

        margin-bottom: 12px;

        text-shadow:
            0 2px 8px
            rgba(0,0,0,0.40);

    }}


    .titulo-mina {{

        font-size: 43px;

        font-weight: 800;

        margin-bottom: 15px;

        text-shadow:
            0 3px 12px
            rgba(0,0,0,0.55);

    }}


    .descripcion {{

        font-size: 18px;

        line-height: 1.65;

        max-width: 1000px;

        color: #f0f6f8;

        margin-bottom: 30px;

        text-shadow:
            0 2px 8px
            rgba(0,0,0,0.40);

    }}



    /* ==================================================
       TARJETAS DE INFORMACIÓN
    ================================================== */

    .grid-procesos {{

        display: grid;

        grid-template-columns:
            repeat(2, 1fr);

        gap: 22px;

        margin-top: 22px;

        margin-bottom: 25px;

    }}


    .card-proceso {{

        background:
            rgba(10,25,35,0.58);

        border:
            1px solid
            rgba(255,255,255,0.20);

        border-radius: 18px;

        overflow: hidden;

        backdrop-filter:
            blur(11px);

        -webkit-backdrop-filter:
            blur(11px);

        box-shadow:
            0 12px 30px
            rgba(0,0,0,0.28);

        transition:
            0.25s;

    }}


    .card-proceso:hover {{

        transform:
            translateY(-3px);

        border-color:
            rgba(110,209,220,0.55);

    }}


    .foto-proceso {{

        width: 100%;

        height: 245px;

        object-fit: cover;

        display: block;

    }}


    .placeholder-foto {{

        width: 100%;

        height: 245px;

        display: flex;

        align-items: center;

        justify-content: center;

        background:
            rgba(255,255,255,0.08);

        color: #dce8ec;

    }}


    .card-proceso-body {{

        padding: 20px 22px 24px 22px;

    }}


    .card-subtitle {{

        font-size: 12px;

        letter-spacing: 1.5px;

        color: #6ed1dc;

        font-weight: 700;

        margin-bottom: 8px;

    }}


    .card-title {{

        font-size: 24px;

        font-weight: 750;

        margin-bottom: 12px;

        color: white;

    }}


    .card-text {{

        font-size: 15px;

        line-height: 1.55;

        color: #e1eaee;

    }}



    /* ==================================================
       MENSAJE CLAVE
    ================================================== */

    .info-clave {{

        margin-top: 15px;

        padding:
            18px 22px;

        border-radius: 16px;

        background:
            rgba(10,25,35,0.57);

        border:
            1px solid
            rgba(110,209,220,0.38);

        color: #f0f7f9;

        line-height: 1.6;

        backdrop-filter:
            blur(10px);

        -webkit-backdrop-filter:
            blur(10px);

        box-shadow:
            0 10px 28px
            rgba(0,0,0,0.20);

    }}



    /* ==================================================
       BOTÓN CONTINUAR
    ================================================== */

    .boton-centro {{

        text-align: center;

        margin-top: 25px;

    }}


    .btn-continuar {{

        display: inline-block;

        text-decoration: none;

        color: white;

        background:
            rgba(28,154,170,0.92);

        border:
            1px solid
            rgba(255,255,255,0.22);

        border-radius: 13px;

        padding:
            16px 30px;

        font-size: 16px;

        font-weight: 700;

        box-shadow:
            0 8px 24px
            rgba(0,0,0,0.28);

        transition:
            all 0.25s ease;

    }}


    .btn-continuar:hover {{

        transform:
            translateY(-3px);

        background:
            rgba(41,181,196,0.98);

        box-shadow:
            0 12px 30px
            rgba(0,0,0,0.32);

    }}



    /* ==================================================
       DECISIONES
    ================================================== */

    .pregunta {{

        font-size: 25px;

        font-weight: 700;

        margin-top: 35px;

        margin-bottom: 20px;

        text-shadow:
            0 3px 10px
            rgba(0,0,0,0.45);

    }}


    .opciones {{

        display: grid;

        grid-template-columns:
            repeat(3, 1fr);

        gap: 18px;

    }}


    .opcion {{

        display: block;

        text-decoration: none;

        color: white;

        background:
            rgba(9,26,37,0.59);

        border:
            1px solid
            rgba(255,255,255,0.22);

        border-radius: 18px;

        padding: 24px;

        backdrop-filter:
            blur(11px);

        -webkit-backdrop-filter:
            blur(11px);

        box-shadow:
            0 10px 26px
            rgba(0,0,0,0.25);

        transition:
            all 0.25s ease;

    }}


    .opcion:hover {{

        transform:
            translateY(-5px);

        background:
            rgba(40,155,169,0.29);

        border-color:
            #65cbd5;

        box-shadow:
            0 15px 32px
            rgba(0,0,0,0.30);

    }}


    .opcion strong {{

        display: block;

        font-size: 20px;

        margin-bottom: 9px;

    }}


    .opcion span {{

        font-size: 15px;

        line-height: 1.5;

        color: #dce9ed;

    }}



    /* ==================================================
       RESPONSIVE
    ================================================== */

    @media (max-width: 900px) {{

        .grid-procesos,
        .opciones {{

            grid-template-columns:
                1fr;

        }}

        #info-mina,
        #decision-mina {{

            padding:
                28px 24px;

        }}

        .titulo-mina {{

            font-size:
                34px;

        }}

    }}


    </style>



    <div class="experiencia">


        <!-- =================================================
             VIDEO CORDILLERA → MINA
        ================================================== -->

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



        <!-- =================================================
             PANTALLA INFORMATIVA
        ================================================== -->

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

                una mayor eficiencia de recuperación y
                recirculación disminuye la necesidad de
                incorporar agua fresca al proceso.

                Como consecuencia, una mayor cantidad de agua
                puede permanecer disponible para continuar
                aguas abajo en la cuenca.

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



        <!-- =================================================
             PANTALLA DE DECISIÓN
        ================================================== -->

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


                <!-- ALTA -->

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



                <!-- MEDIA -->

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



                <!-- BAJA -->

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


    // ==================================================
    // REFERENCIAS
    // ==================================================

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



    // ==================================================
    // CUANDO TERMINA EL VIDEO
    // ==================================================

    video.addEventListener(
        "ended",
        function() {{

            pantallaVideo.style.display =
                "none";

            infoMina.style.display =
                "block";

        }}
    );



    // ==================================================
    // PASAR DE INFORMACIÓN A DECISIÓN
    // ==================================================

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
        height=820,
        scrolling=False
    )


# ==================================================
# LEER DECISIÓN DEL USUARIO
# ==================================================

decision = st.query_params.get(
    "decision_mina"
)


if decision:

    # Evitar aplicar la misma decisión dos veces
    decision_anterior = st.session_state.get(
        "decision_mina"
    )

    if decision != decision_anterior:

        st.session_state[
            "decision_mina"
        ] = decision


        # ----------------------------------------------
        # MODIFICACIÓN PROVISORIA DEL CAUDAL
        # ----------------------------------------------

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


    # Limpiar parámetros de URL
    st.query_params.clear()


    st.success(
        f"Decisión registrada: {decision}. "
        f"Caudal actual: "
        f"{st.session_state.caudal_actual}"
    )