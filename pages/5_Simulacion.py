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





