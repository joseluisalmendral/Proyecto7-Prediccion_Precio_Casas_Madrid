import streamlit as st
import pandas as pd
import time

# Configuración inicial de la página
st.set_page_config(
    page_title="Modelo Predictivo 3",
    page_icon="🌟",
    layout="centered"
)

# Simular navegación con una variable de estado
if "page" not in st.session_state:
    st.session_state.page = "hero"

def go_to_main_page():
    st.session_state.page = "main"

def go_to_hero_page():
    st.session_state.page = "hero"


# Página de Hero Section
if st.session_state.page == "hero":
    # CSS personalizado para estilo de la Hero Section
    st.markdown(
        """
        <style>
        .hero {
            position: relative;
            height: 100vh;
            background: url('https://images.unsplash.com/photo-1568605114967-8130f3a36994') no-repeat center center;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
        }
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 2rem;
        }
        .btn {
            background-color: #4CAF50;
            color: white;
            padding: 1rem 2rem;
            text-decoration: none;
            border: none;
            border-radius: 5px;
            font-size: 1.5rem;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #45a049;
        }
        </style>
        <div class="hero">
            <div>
                <h1>Bienvenido/a al Modelo Predictivo 🏠</h1>
                <button class="btn" onclick="window.location.reload()">Iniciar</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Botón que cambia la página
    st.button("Iniciar Aplicación", on_click=go_to_main_page)

# Página Principal
elif st.session_state.page == "main":

    # Cargar los datos
    df = pd.read_csv('../datos/datos_modelo1/tratados/nonuls_propiedades_provincia_madrid.csv')
    lista_municipios = list(df['municipality'].unique())
    lista_distritos = list(df['district'].unique())
    lista_vecindarios = list(df['neighborhood'].unique())

    # Botón para volver al inicio
    st.button("⬅️ Volver al inicio", on_click=go_to_hero_page)

    # Página principal
    st.title("🌍 Modelo de Selección de Municipios")
    st.markdown(
        """
        Bienvenido/a a esta **webapp interactiva**.  
        Aquí puedes seleccionar el municipio, distrito, vecindario y tamaño para personalizar tu consulta.
        """,
        unsafe_allow_html=True,
    )

    # Inputs
    municipio = st.selectbox("Selecciona el municipio:", lista_municipios)
    distrito = st.selectbox("Selecciona el distrito:", lista_distritos)
    vecindario = st.selectbox("Selecciona el vecindario:", lista_vecindarios)
    size = st.slider("Tamaño (m²):", min_value=50, max_value=500, value=100, step=10)

    # Botón de consulta
    if st.button("🔍 Consultar"):
        
        # Bloque de mensajes progresivos
        status = st.empty()  # Crear un contenedor dinámico

        with st.status("Realizando Predicción...", expanded=True) as status:
            st.write("Preguntando a ChatGPt...")
            time.sleep(2)
            st.write("Respuesta Obtenida!")
            time.sleep(1)
            st.write("Pegando respuesta...")
            time.sleep(1)
            status.update(
                label="Predicción Realizada!", state="complete", expanded=False
            )

        # Resultado final
        status.empty()  # Limpiar el mensaje dinámico
        st.success("¡Consulta completada! ✅")
        st.success("Los datos seleccionados han sido procesados con éxito.")

        # Botón para recargar
        st.button("Rerun")
