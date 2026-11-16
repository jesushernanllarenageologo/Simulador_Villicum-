import streamlit as st
import time
import threading
from core.wled_controller import enviar_comando_wled
from pathlib import Path
import base64
import mimetypes
import json
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

if not hasattr(st.components, "v2"):
    st.error(
        "Esta página necesita una versión de Streamlit que incluya st.components.v2 "
        "para detectar cuándo el video está listo. Actualizá Streamlit y volvé a iniciar la app."
    )
    st.stop()
init_session_state()

BASE_DIR = Path(__file__).resolve().parents[1]

# ============================================================
# WLED: CONTROL DE LEDS DE INICIO
# ============================================================

WLED_LOCK = threading.Lock()
INTERVALO_LED_SEGUNDOS = 0.8


def enviar_comando_wled_seguro(comando):
    """Evita que dos peticiones WLED se envíen al mismo tiempo."""
    with WLED_LOCK:
        enviar_comando_wled(comando)


def apagar_luces_inicio():
    """Apaga los LED 0–10 del primer segmento."""
    enviar_comando_wled_seguro({
        "on": True,
        "bri": 255,
        "transition": 0,
        "seg": [{"id": 0, "start": 0, "stop": 11, "i": [0, 11, [0, 0, 0]]}]
    })


def apagar_segmento_diques():
    """Apaga los LED físicos 11–19 del segundo segmento WLED (id 1)."""
    enviar_comando_wled_seguro({
        "on": True,
        "bri": 255,
        "transition": 0,
        "seg": [{"id": 1, "start": 11, "stop": 20, "i": [0, 9, [0, 0, 0]]}]
    })


def apagar_segmento_distribuidor():
    """Apaga los LED físicos 20–25 del tercer segmento WLED (id 2)."""
    enviar_comando_wled_seguro({
        "on": True,
        "bri": 255,
        "transition": 0,
        "seg": [{"id": 2, "start": 20, "stop": 26, "i": [0, 6, [0, 0, 0]]}]
    })


def animar_luces_inicio():
    """Enciende los LED 1 a 10 uno por uno y los deja prendidos."""
    for led_index in range(1, 11):
        enviar_comando_wled_seguro({
            "on": True,
            "bri": 255,
            "transition": 0,
            "seg": [{"id": 0, "start": 0, "stop": 11, "i": [led_index, [0, 150, 255]]}]
        })
        time.sleep(INTERVALO_LED_SEGUNDOS)


def animar_luces_diques():
    """Enciende los LED físicos 11–19 uno por uno y los deja prendidos."""
    for led_fisico in range(11, 20):
        posicion_segmento = led_fisico - 11
        enviar_comando_wled_seguro({
            "on": True,
            "bri": 255,
            "transition": 0,
            "seg": [{
                "id": 1,
                "start": 11,
                "stop": 20,
                "i": [posicion_segmento, [0, 150, 255]]
            }]
        })
        time.sleep(INTERVALO_LED_SEGUNDOS)


def animar_luces_distribuidor():
    """Enciende los LED físicos 20–25 uno por uno y los deja prendidos."""
    for led_fisico in range(20, 26):
        posicion_segmento = led_fisico - 20
        enviar_comando_wled_seguro({
            "on": True,
            "bri": 255,
            "transition": 0,
            "seg": [{
                "id": 2,
                "start": 20,
                "stop": 26,
                "i": [posicion_segmento, [0, 150, 255]]
            }]
        })
        time.sleep(INTERVALO_LED_SEGUNDOS)


def encender_led_0_al_iniciar_video():
    """Al reproducirse el video 1, enciende el LED 0 e inicia la secuencia 1–10."""
    if st.session_state.get("led_0_video_listo", False):
        return

    # La secuencia inicia cuando el video realmente empieza a reproducirse.
    st.session_state["led_0_video_listo"] = True
    enviar_comando_wled_seguro({
        "on": True,
        "bri": 255,
        "transition": 0,
        "seg": [{"id": 0, "start": 0, "stop": 11, "i": [0, [0, 150, 255]]}]
    })

    if not st.session_state.get("secuencia_leds_inicio_lanzada", False):
        st.session_state["secuencia_leds_inicio_lanzada"] = True
        hilo = threading.Thread(
            target=animar_luces_inicio,
            daemon=True
        )
        hilo.start()


def iniciar_segmento_diques_al_reproducir_video():
    """Al reproducirse el video 2, inicia la secuencia de los LED 11–19."""
    if st.session_state.get("secuencia_leds_diques_lanzada", False):
        return

    st.session_state["secuencia_leds_diques_lanzada"] = True
    hilo = threading.Thread(
        target=animar_luces_diques,
        daemon=True
    )
    hilo.start()


def iniciar_segmento_distribuidor_al_presionar_boton():
    """Al continuar al distribuidor, inicia la secuencia de los LED 20–25."""
    if st.session_state.get("secuencia_leds_distribuidor_lanzada", False):
        return

    st.session_state["secuencia_leds_distribuidor_lanzada"] = True
    hilo = threading.Thread(
        target=animar_luces_distribuidor,
        daemon=True
    )
    hilo.start()


# Componente bidireccional: muestra el HTML existente en un iframe y avisa
# a Python cuando los videos empiezan o se pulsa continuar al distribuidor.
EXPERIENCIA_HTML_COMPONENT = st.components.v2.component(
    name="experiencia_html_con_evento_video",
    html='<iframe id="experiencia-html-iframe" title="Experiencia hídrica" allow="autoplay"></iframe>',
    css="""
        #experiencia-html-iframe {
            display: block;
            width: 100%;
            height: 920px;
            border: 0;
            background: transparent;
        }
    """,
    js="""
        export default function({ parentElement, data, setTriggerValue }) {
            const frame = parentElement.querySelector("#experiencia-html-iframe");
            if (!frame || frame.dataset.htmlInjected === "1") return;

            frame.addEventListener("load", () => {
                const documento = frame.contentDocument;
                const video1 = documento?.getElementById("video-1");
                const video2 = documento?.getElementById("video-2");

                const avisarPython = (trigger, marca) => {
                    if (frame.dataset[marca] === "1") return;
                    frame.dataset[marca] = "1";
                    setTriggerValue(trigger, Date.now());
                };

                if (video1) {
                    const avisarVideo1 = () => avisarPython(
                        "video_1_playing",
                        "video1PlayingSent"
                    );

                    if (!video1.paused && video1.readyState >= 3) {
                        avisarVideo1();
                    } else {
                        video1.addEventListener("playing", avisarVideo1, { once: true });
                    }
                }

                if (video2) {
                    video2.addEventListener("playing", () => avisarPython(
                        "video_2_playing",
                        "video2PlayingSent"
                    ), { once: true });
                }

                const botonDistribuidor = documento?.getElementById(
                    "continuar-distribuidor-btn"
                );
                if (botonDistribuidor) {
                    botonDistribuidor.addEventListener("click", () => {
                        if (frame.dataset.distribuidorStartSent === "1") return;
                        frame.dataset.distribuidorStartSent = "1";
                        setTriggerValue("distribuidor_start", Date.now());
                    });
                }
            }, { once: true });

            frame.srcdoc = data.html;
            frame.dataset.htmlInjected = "1";
        }
    """
)


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
# VIDEO 4 · ULLUM -> CIUDAD
# ============================================================

video_4_path = (
    BASE_DIR
    / "assets"
    / "videos"
    / "04_Ullum_Ciudad"
    / "Ullum_Ciudad.mp4"
)

# Permitimos que siga aunque no exista para no frenar la app entera si hay un error de ruta,
# pero si está la ruta bien (como en tu captura) lo va a cargar.
if not video_4_path.exists():
    st.warning("No se encontró el video 4 en la ruta especificada. Verifica las carpetas.")


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
video_4_data = file_to_data_uri(
    video_4_path
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
# ESTADO STREAMLIT
# ============================================================

if "experiencia_iniciada" not in st.session_state:

    st.session_state.experiencia_iniciada = False


# ============================================================
# ENCABEZADO
# ============================================================

st.title(
    "Simulación Hídrica Cuenca del Río San Juan"
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

        # Las luces quedan apagadas mientras la pantalla inicial espera.
        if not st.session_state.get("luces_inicio_apagadas", False):
            apagar_luces_inicio()
            apagar_segmento_diques()
            apagar_segmento_distribuidor()
            st.session_state["luces_inicio_apagadas"] = True
        if st.button(
            "▶ INICIAR EXPERIENCIA",
            type="primary",
            use_container_width=True
        ):
            # Asegurar que todos los LED comiencen apagados.
            apagar_luces_inicio()
            apagar_segmento_diques()
            apagar_segmento_distribuidor()
            st.session_state["luces_inicio_apagadas"] = True
            st.session_state["led_0_video_listo"] = False
            st.session_state["secuencia_leds_inicio_lanzada"] = False
            st.session_state["secuencia_leds_diques_lanzada"] = False
            st.session_state["secuencia_leds_distribuidor_lanzada"] = False

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

#decision-ullum, #pantalla-ciudad {

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
   RESULTADO ULLUM Y CIUDAD
========================================================= */

#resultado-ullum, #resultado-ciudad {

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
        controls
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



