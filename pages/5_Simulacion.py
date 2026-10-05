import streamlit as st
from pathlib import Path
import base64

from core.state_manager import init_session_state


# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="Simulación",
    page_icon="🌊",
    layout="wide"
)

init_session_state()

BASE_DIR = Path(__file__).resolve().parents[1]


# ==================================================
# ESCENARIO SELECCIONADO
# ==================================================

escenario = st.session_state.get("escenario_seleccionado")

if not escenario:
    st.warning("Primero debes seleccionar un escenario.")

    if st.button("← Volver al simulador"):
        st.switch_page("pages/1_Simulador.py")

    st.stop()


# ==================================================
# ENCABEZADO
# ==================================================

st.title("🌊 Simulación Hídrica")

st.markdown(
    f"""
    ### Escenario inicial: **{escenario}**
    """
)


# ==================================================
# POR AHORA PROBAMOS SOLO SUPERAVITARIO
# ==================================================

if escenario != "Superavitario":

    st.info(
        f"El escenario {escenario} todavía no tiene cargada "
        "la experiencia audiovisual."
    )

    if st.button("← Volver"):
        st.switch_page("pages/1_Simulador.py")

    st.stop()


# ==================================================
# VIDEO CORDILLERA → MINA
# ==================================================

video_path = (
    BASE_DIR
    / "assets"
    / "videos"
    / "01_Cordillera_Mina"
    / "Superavitario.mp4"
)


if not video_path.exists():

    st.error("No se encontró el video Superavitario.mp4")

    st.code(str(video_path))

    st.stop()


# ==================================================
# ESTADO DE LA EXPERIENCIA
# ==================================================

if "experiencia_iniciada" not in st.session_state:
    st.session_state.experiencia_iniciada = False


# ==================================================
# PANTALLA INICIAL
# ==================================================

if not st.session_state.experiencia_iniciada:

    st.markdown(
        """
        La cuenca inicia con una **alta disponibilidad hídrica**.

        El recorrido comenzará en la Cordillera de los Andes y
        seguirá el Río San Juan hasta la primera parada del simulador:
        **la actividad minera**.
        """
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "▶ INICIAR EXPERIENCIA",
            type="primary",
            use_container_width=True
        ):

            st.session_state.experiencia_iniciada = True
            st.rerun()


# ==================================================
# EXPERIENCIA AUDIOVISUAL
# ==================================================

else:

    # Convertimos el video a base64 para reproducirlo
    # dentro de HTML sin mostrar controles.
    video_bytes = video_path.read_bytes()

    video_base64 = base64.b64encode(
        video_bytes
    ).decode()


    # ------------------------------------------------
    # HTML DE LA EXPERIENCIA
    # ------------------------------------------------

    html = f"""
    <style>

        body {{
            margin: 0;
            background: #08131d;
            font-family: Arial, sans-serif;
        }}

        .experiencia {{
            width: 100%;
            min-height: 680px;
            background: #08131d;
            border-radius: 18px;
            overflow: hidden;
            position: relative;
        }}

        #pantalla-video {{
            width: 100%;
            height: 680px;
            position: relative;
            background: black;
        }}

        #video-rio {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .etiqueta {{
            position: absolute;
            top: 30px;
            left: 35px;

            background: rgba(0,0,0,0.60);
            color: white;

            padding: 12px 20px;
            border-radius: 10px;

            font-size: 18px;
        }}


        /* ---------------------------------------
           PARADA MINA
        --------------------------------------- */

        #mina {{
            display: none;

            min-height: 680px;

            padding: 45px;

            box-sizing: border-box;

            background:
                linear-gradient(
                    135deg,
                    #0c1b27,
                    #132b38
                );

            color: white;

            animation: aparecer 1s ease;
        }}


        @keyframes aparecer {{

            from {{
                opacity: 0;
            }}

            to {{
                opacity: 1;
            }}

        }}


        .titulo-etapa {{
            font-size: 15px;
            letter-spacing: 2px;
            color: #72c7d4;
            margin-bottom: 10px;
        }}


        .titulo-mina {{
            font-size: 38px;
            font-weight: 700;
            margin-bottom: 10px;
        }}


        .descripcion {{
            font-size: 18px;
            line-height: 1.6;
            max-width: 900px;
            color: #dbe7ec;
        }}


        .datos {{
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 15px;

            margin-top: 30px;
            margin-bottom: 35px;
        }}


        .dato {{
            background:
                rgba(255,255,255,0.07);

            border:
                1px solid
                rgba(255,255,255,0.12);

            border-radius: 14px;

            padding: 20px;
        }}


        .dato strong {{
            display: block;

            font-size: 22px;

            margin-bottom: 7px;
        }}


        .pregunta {{
            font-size: 23px;
            font-weight: 600;
            margin-bottom: 20px;
        }}


        .opciones {{

            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 15px;

        }}


        .opcion {{

            display: block;

            text-decoration: none;

            color: white;

            background:
                rgba(255,255,255,0.08);

            border:
                1px solid
                rgba(255,255,255,0.18);

            border-radius: 14px;

            padding: 22px;

            transition: 0.25s;

        }}


        .opcion:hover {{

            transform:
                translateY(-4px);

            background:
                rgba(66, 180, 190, 0.25);

            border-color:
                #52bec7;

        }}


        .opcion strong {{

            display: block;

            font-size: 19px;

            margin-bottom: 8px;

        }}


        .opcion span {{

            font-size: 14px;

            color: #c9d9df;

        }}


    </style>



    <div class="experiencia">


        <!-- ===========================
             VIDEO
        ============================ -->

        <div id="pantalla-video">

            <video
                id="video-rio"
                autoplay
                muted
                playsinline
            >

                <source
                    src="data:video/mp4;base64,{video_base64}"
                    type="video/mp4"
                >

            </video>


            <div class="etiqueta">

                🏔️ Cordillera → Mina

            </div>

        </div>



        <!-- ===========================
             PARADA MINA
        ============================ -->

        <div id="mina">


            <div class="titulo-etapa">

                PARADA 1 · CUENCA ALTA

            </div>


            <div class="titulo-mina">

                ⛏️ Actividad minera

            </div>


            <p class="descripcion">

                El agua utilizada en los procesos mineros
                puede ser recuperada y recirculada dentro
                del sistema.

                Una mayor eficiencia en la recirculación
                reduce la necesidad de incorporar agua nueva
                desde la cuenca.

            </p>



            <div class="datos">


                <div class="dato">

                    <strong>♻️ Recirculación</strong>

                    Recuperación y reutilización del agua
                    dentro del proceso.

                </div>


                <div class="dato">

                    <strong>💧 Agua fresca</strong>

                    El consumo neto depende de la eficiencia
                    del circuito.

                </div>


                <div class="dato">

                    <strong>🌊 Consecuencia</strong>

                    La decisión modificará el caudal
                    disponible aguas abajo.

                </div>


            </div>



            <div class="pregunta">

                ¿Qué estrategia de gestión aplicarías?

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
                        Mantener una gestión equilibrada
                        del recurso.
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
                        Mayor incorporación de agua
                        fresca al proceso.
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


        const mina =
            document.getElementById(
                "mina"
            );


        video.addEventListener(
            "ended",
            function() {{

                pantallaVideo.style.display =
                    "none";

                mina.style.display =
                    "block";

            }}
        );

    </script>
    """


    st.components.v1.html(
        html,
        height=700,
        scrolling=False
    )


# ==================================================
# LEER DECISIÓN DE LA MINA
# ==================================================

decision = st.query_params.get("decision_mina")


if decision:

    st.session_state["decision_mina"] = decision

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
        f"Decisión registrada. "
        f"Caudal actual: "
        f"{st.session_state.caudal_actual}"
    )