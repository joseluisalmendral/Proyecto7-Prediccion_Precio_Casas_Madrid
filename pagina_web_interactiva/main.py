import streamlit as st
import pandas as pd
import pickle
import time

# Configuración inicial de la página
st.set_page_config(
    page_title="Predictor Alquileres",
    page_icon="📊",
    layout="centered"
)

# Simular navegación con una variable de estado
if "page" not in st.session_state:
    st.session_state.page = "hero"

def go_to_main_page():
    st.session_state.page = "main"

def go_to_hero_page():
    st.session_state.page = "hero"


# Cargar los modelos y transformadores entrenados
def cargar_modelos():
    with open('../src/modelos/target_encoder.pkl', 'rb') as f:
        target_encoder_ = pickle.load(f)
    with open('../src/modelos/robust_scaler.pkl', 'rb') as f:
        robust_scaler_ = pickle.load(f)
    with open('../src/modelos/model_decision_tree_regressor.pkl', 'rb') as f:
        decision_tree_regressor_ = pickle.load(f)
    return target_encoder_, robust_scaler_, decision_tree_regressor_

target_encoder, robust_scaler, decision_tree_regressor = cargar_modelos()


# Página de Hero Section
if st.session_state.page == "hero":
    # CSS personalizado para estilo de la Hero Section
    st.markdown(
        """
        <style>
        .hero {
            position: relative;
            height: 70vh;
            background: url('https://images.unsplash.com/photo-1568605114967-8130f3a36994') no-repeat center center;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
        }
        .hero h1 {
            width: 60%;
            margin: auto;
            font-size: 3rem;
            margin-bottom: 2rem;
            padding: 2rem 2.5rem;
            background-color: black;
            border: 1px solid white;
            border-radius: .4rem;
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
                <h1>Bienvenid@ al Modelo Predictivo 🏠</h1>
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
    min_max_size = [int(df['size'].min()), int(df['size'].max())]

    # Botón para volver al inicio
    st.button("⬅️ Volver al inicio", on_click=go_to_hero_page)

    # Página principal
    st.title("🌍 Modelo Prediccivo de Alquileres en Madrid [2015 - 2018]")
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
    size = st.slider("Tamaño (m²):", min_value=min_max_size[0], max_value=min_max_size[1], value=int(min_max_size[1]/2), step=1)

    # Botón de consulta
    if st.button("🔍 Consultar"):

        # Crear DataFrame con los datos ingresados
        nueva_propiedad = pd.DataFrame({
            'municipality': [municipio],
            'district': [distrito],
            'neighborhood': [vecindario],
            'price': [size],
        })

        # Columnas que el escalador espera
        expected_columns = ['bathrooms', 'distance', 'numPhotos', 'rooms', 'size']

        # Agregar columnas faltantes con valor predeterminado (ejemplo: 0)
        for col in expected_columns:
            if col not in nueva_propiedad.columns:
                nueva_propiedad[col] = 0

        # Columnas categóricas y numéricas
        categorical_columns = ['municipality', 'district', 'neighborhood']
        numerical_columns = ['numPhotos', 'size', 'rooms', 'bathrooms', 'distance']

        # Crear una copia para transformaciones
        new_house_encoded = nueva_propiedad.copy()

        # Aplicar el TargetEncoder SOLO a las columnas categóricas
        try:
            new_house_encoded[categorical_columns] = target_encoder.transform(nueva_propiedad[categorical_columns])
        except ValueError as e:
            st.error(f"Error al transformar datos categóricos: {e}")
            st.stop()

        # Aplicar el escalador a las columnas numéricas
        try:
            new_house_encoded[numerical_columns] = robust_scaler.transform(new_house_encoded[numerical_columns])
        except ValueError as e:
            st.error(f"Error al escalar datos numéricos: {e}")
            st.stop()

        # Realizar la predicción
        try:
            orden_columnas = ['size', 'municipality', 'district', 'neighborhood']
            df_predecir = new_house_encoded.drop(columns=['bathrooms', 'distance', 'numPhotos', 'price', 'rooms'])
            df_predecir = df_predecir[orden_columnas]
            prediction = decision_tree_regressor.predict(df_predecir)[0]
        except ValueError as e:
            st.error(f"Error al predecir: {e}")
            st.stop()


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
        st.success(f"El precio del alquiler ha de rondar los {round(prediction)}€")
        st.success(f"Entre los {round(prediction - 41.33, 2)}€ y los {round(prediction + 41.33, 2)}€")

        # Botón para recargar
        if st.button("Rerun"):
            st.session_state.prediction = None
