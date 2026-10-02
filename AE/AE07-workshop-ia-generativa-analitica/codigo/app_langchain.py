 #!/usr/bin/env python3
"""
Sistema de Chat con Agentes IA para Análisis de Datos - LangChain Version
"""

import os
import sys
import ast
import logging
import importlib
import streamlit as st
from dotenv import load_dotenv

logging.getLogger('root').setLevel(logging.CRITICAL)
load_dotenv()

app_nombre = os.getenv("APP_NOMBRE", "Análisis de Datos")

def cargar_info_datasets():
    info = {}
    try:
        with open('data/datasets_info.txt', 'r', encoding='utf-8') as f:
            contenido = f.readlines()
            dataset_actual = None
            descripcion = []

            for linea in contenido:
                linea = linea.strip()
                if linea.endswith('.csv'):
                    if dataset_actual and descripcion:
                        info[dataset_actual] = ' '.join(descripcion)
                    dataset_actual = linea.replace('.csv', '')
                    descripcion = []
                elif linea:
                    descripcion.append(linea)

            if dataset_actual and descripcion:
                info[dataset_actual] = ' '.join(descripcion)
    except:
        info = {
            'customer_data': 'Información de clientes',
            'sales_data': 'Información de ventas',
            'marketing_campaign': 'Información de campañas'
        }

    return info


def cargar_agentes():
    agentes = {}
    agents_path = os.path.join(os.path.dirname(__file__), 'agents')

    if not os.path.exists(agents_path):
        return agentes

    for archivo in sorted(os.listdir(agents_path)):
        if not archivo.endswith('.py') or archivo.startswith('_'):
            continue

        modulo = archivo.replace('.py', '')
        nombre = (
            modulo
            .replace('_langchain', '')
            .replace('_', ' ')
            .title()
        )

        try:
            if f'agents.{modulo}' in sys.modules:
                mod = importlib.reload(sys.modules[f'agents.{modulo}'])
            else:
                mod = __import__(f'agents.{modulo}', fromlist=['create_agent'])

            if not hasattr(mod, 'create_agent'):
                continue

            agente = mod.create_agent()
            agentes[modulo] = {
                'agente': agente,
                'nombre': nombre,
                'descripcion': getattr(mod, 'DESCRIPTION', 'Agente con LangChain')
            }
        except Exception as e:
            st.sidebar.warning(f"⚠️ {nombre}: {str(e)}")

    return agentes


st.set_page_config(
    page_title="Análisis de Datos IA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* ── Tokens ── */
    :root {
        --ink:     #0f0e1a;   /* casi negro azulado — títulos y peso */
        --ink-2:   #25264a;   /* texto cuerpo */
        --g-200:   #d8dae6;
        --g-400:   #7e8399;
        --lila:    #a78bfa;
        --violeta: #7c3aed;
        --v-dark:  #4c1d95;   /* violeta oscuro — acento bordes */
        --az-100:  #cdd6f4;
        --az-200:  #8da4e8;
    }

    * { font-family: 'Inter', -apple-system, sans-serif; font-weight: 400; }

    /* ── Header ── */
    [data-testid="stHeader"]    { background: transparent !important; border-bottom: none !important; box-shadow: none !important; }
    [data-testid="stDecoration"] { display: none !important; }

    /* ── Fondo ── */
    .main { background: linear-gradient(160deg, #ededf5 0%, #e8eaf4 45%, #eceaf8 100%); }
    .block-container { padding: 1.5rem 2rem 8rem; max-width: 1100px; }
    hr { border: none; height: 0.5px; background: var(--g-200); margin: 0.75rem 0; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(236,237,245,0.98);
        border-right: 1px solid var(--g-200);
        padding: 0.25rem 1rem 1.5rem;
    }
    [data-testid="stSidebar"] h2 {
        font-size: 0.60rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.11em;
        color: var(--g-400);
        border: none;
        margin-bottom: 0.5rem;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stCaption { font-size: 0.75rem; color: var(--ink-2); line-height: 1.55; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.85) !important;
        border: 0.5px solid var(--g-200) !important;
        border-radius: 10px !important;
        font-size: 0.82rem !important;
        color: #1e1b4b !important;
        font-weight: 500 !important;
        box-shadow: none !important;
    }
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="popover"] [role="option"] { font-size: 0.82rem !important; color: #1e1b4b !important; }
    [data-baseweb="popover"] [role="option"]:hover { background: rgba(167,139,250,0.08) !important; }
    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        background: rgba(255,255,255,0.70);
        color: #4a4f6a;
        border: 0.5px solid var(--g-200);
        border-radius: 9px;
        padding: 0.4rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 500;
        transition: background 0.15s, border-color 0.15s;
        box-shadow: none;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.95);
        border-color: var(--lila);
        box-shadow: none;
    }

    /* ── Mensajes asistente ── */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: rgba(225,228,245,0.65);
        border: 0.5px solid var(--az-100);
        border-radius: 14px;
        padding: 0.65rem 0.9rem;
        margin: 0.3rem 0;
        box-shadow: none;
    }
    /* ── Mensajes usuario ── */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(215,218,238,0.50);
        border: 0.5px solid var(--g-200);
        border-radius: 14px 3px 14px 14px;
        padding: 0.65rem 0.9rem;
        margin: 0.3rem 0;
        box-shadow: none;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] td { font-size: 0.875rem; line-height: 1.65; margin: 0; color: var(--ink-2); }
    [data-testid="stChatMessage"] ul,
    [data-testid="stChatMessage"] ol { padding-left: 1.25rem; margin: 0.25rem 0; }
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] h4 { font-size: 0.875rem; font-weight: 600; line-height: 1.6; margin: 0; color: var(--ink); }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        width: 100%;
        overflow-x: hidden;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] > div {
        width: 100%;
        overflow-x: auto;
    }
    [data-testid="stChatMessage"] table {
        width: auto;
        max-width: 100%;
        border-collapse: collapse;
        margin: 0.2rem 0 0;
    }
    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] td {
        padding: 0.25rem 0.45rem;
        white-space: nowrap;
        border-bottom: 0.5px solid var(--g-200);
    }
    [data-testid="stChatMessage"] th {
        font-weight: 600;
        color: var(--ink);
        background: rgba(255,255,255,0.35);
    }

    /* ── Avatar asistente ── */
    [data-testid="chatAvatarIcon-assistant"] {
        width: 32px !important; height: 32px !important;
        border-radius: 10px !important;
        background: linear-gradient(135deg, #5b21b6, #7c3aed) !important;
        display: flex !important; align-items: center !important;
        justify-content: center !important; overflow: hidden !important;
    }
    [data-testid="chatAvatarIcon-assistant"]::before { content: "✦"; font-size: 14px; color: #e9d5ff; line-height: 1; }
    [data-testid="chatAvatarIcon-assistant"] > * { display: none !important; }

    /* ── Avatar usuario ── */
    [data-testid="chatAvatarIcon-user"] {
        width: 32px !important; height: 32px !important;
        border-radius: 10px !important;
        background: linear-gradient(135deg, #c7cde8, #a5aed4) !important;
        border: 0.5px solid rgba(143,155,200,0.30) !important;
        display: flex !important; align-items: center !important;
        justify-content: center !important; overflow: hidden !important;
    }
    [data-testid="chatAvatarIcon-user"]::before { content: "👤"; font-size: 15px; color: #fff; line-height: 1; }
    [data-testid="chatAvatarIcon-user"] > * { display: none !important; }

    /* ── Input ── */
    .stChatFloatingInputContainer,
    .stChatFloatingInputContainer > div,
    .stChatFloatingInputContainer > div > div,
    .stChatInputContainer,
    .stChatInputContainer > div { background: transparent !important; border: none !important; box-shadow: none !important; }
    [data-testid="stChatInputToolbar"],
    [data-testid="stChatInputToolbarContainer"] { display: none !important; }
    .stChatInputContainer [data-baseweb="textarea"] {
        background: rgba(255,255,255,0.80) !important;
        border: 0.5px solid var(--g-200) !important;
        border-radius: 14px !important;
        box-shadow: none !important;
    }
    .stChatInputContainer [data-baseweb="textarea"]:focus-within {
        background: #fff !important;
        border-color: var(--lila) !important;
    }
    .stChatInputContainer textarea {
        background: transparent !important;
        border: none !important; box-shadow: none !important; outline: none !important;
        padding: .55rem 3.5rem .55rem 1rem !important;
        font-size: .88rem !important;
        color: #25264a !important;
        max-height: 2.8rem !important; min-height: 2.8rem !important;
        resize: none !important; overflow-y: auto !important;
    }
    .stChatInputContainer button {
        background: rgba(255,255,255,0.80) !important;
        border: 0.5px solid var(--g-200) !important;
        border-radius: 10px !important;
        color: var(--g-400) !important;
        width: 2.1rem !important; height: 2.1rem !important;
        padding: 0 !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        align-self: center !important;
        margin-bottom: 0 !important; margin-right: 0.4rem !important;
        transition: background 0.15s, border-color 0.15s, color 0.15s !important;
    }
    .stChatInputContainer button:hover {
        background: var(--violeta) !important;
        border-color: var(--violeta) !important;
        color: #fff !important;
    }
    .stChatInputContainer button svg { width: 1rem !important; height: 1rem !important; }
</style>
""", unsafe_allow_html=True)

if not os.getenv("GROQ_API_KEY") and not os.getenv("OLLAMA_MODEL"):
    st.error("⚠️ No se encontró GROQ_API_KEY")
    st.info("Configura la API key en el archivo .env")
    st.stop()


def main():
    st.markdown(f"""
    <div style="padding: 0.5rem 0 1rem; border-bottom: 1px solid var(--g-200); overflow: visible;">
        <span style="font-size: 0.60rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--g-400); display: block; margin-bottom: 3px;">Asistente</span>
        <p style="font-size: 1.1rem; font-weight: 600; color: var(--ink); margin: 0; line-height: 1.3;">{app_nombre}</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        if "agentes_disponibles" not in st.session_state:
            with st.spinner("Cargando..."):
                st.session_state.agentes_disponibles = cargar_agentes()
        agentes_disponibles = st.session_state.agentes_disponibles

        if not agentes_disponibles:
            st.error("No hay agentes disponibles")
            st.stop()

        st.subheader("AGENTE")
        opciones = {id_agente: info['nombre'] for id_agente, info in agentes_disponibles.items()}

        agente_seleccionado = st.selectbox(
            "Elige un agente:",
            options=list(opciones.keys()),
            format_func=lambda x: opciones[x],
            key="selector_agente",
            label_visibility="collapsed"
        )

        if agente_seleccionado in agentes_disponibles:
            st.caption(agentes_disponibles[agente_seleccionado]['descripcion'])

        st.markdown("---")
        st.subheader("DATASETS")

        info_datasets = cargar_info_datasets()
        nombres = {
            'customer_data': 'Clientes',
            'sales_data': 'Ventas',
            'marketing_campaign': 'Marketing'
        }
        for id_ds, nombre in nombres.items():
            if id_ds in info_datasets:
                st.caption(f"• **{nombre}**: {info_datasets[id_ds]}")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Recargar"):
                st.cache_data.clear()
                st.rerun()
        with c2:
            if st.button("🗑️ Limpiar"):
                st.session_state.mensajes = []
                if "agentes_disponibles" in st.session_state:
                    del st.session_state.agentes_disponibles
                st.rerun()

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

    for msg in st.session_state.mensajes:
        with st.chat_message(msg["rol"]):
            st.markdown(msg["contenido"])

    if pregunta := st.chat_input("Escribe tu pregunta..."):
        st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})

        with st.chat_message("user"):
            st.markdown(pregunta)

        with st.chat_message("assistant"):
            with st.spinner(f"{opciones[agente_seleccionado]} trabajando..."):
                agente_dict = agentes_disponibles[agente_seleccionado]['agente']
                try:
                    respuesta = agente_dict["run"](pregunta)

                    try:
                        parsed_response = ast.literal_eval(respuesta)
                    except Exception:
                        parsed_response = None

                    if isinstance(parsed_response, dict) and "plot_path" in parsed_response:
                        # Un solo gráfico
                        plot_path = parsed_response["plot_path"]
                        if os.path.exists(plot_path):
                            st.image(plot_path)
                            os.remove(plot_path)
                        st.session_state.mensajes.append({"rol": "assistant", "contenido": "Gráfico generado."})
                    elif isinstance(parsed_response, list) and all(
                        isinstance(p, dict) and "plot_path" in p for p in parsed_response
                    ):
                        # Múltiples gráficos
                        for p in parsed_response:
                            plot_path = p["plot_path"]
                            if os.path.exists(plot_path):
                                st.image(plot_path)
                                os.remove(plot_path)
                        st.session_state.mensajes.append({"rol": "assistant", "contenido": f"{len(parsed_response)} gráficos generados."})
                    else:
                        st.markdown(respuesta)
                        st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta})
                except Exception as e:
                    error = f"Error: {str(e)}"
                    st.error(error)
                    st.session_state.mensajes.append({"rol": "assistant", "contenido": error})


if __name__ == "__main__":
    main()
