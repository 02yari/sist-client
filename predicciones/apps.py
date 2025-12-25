import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import base64
from io import BytesIO

# Configuración de página
st.set_page_config(
    page_title="ChurnChaser - Sistema de Predicción de Abandono",
    page_icon="assets/Churn Chaser icon_1753961019024.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado con colores pastel
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Paleta de colores pastel */
    :root {
        --pastel-primary: #A8D5E2;       /* Azul pastel suave */
        --pastel-primary-dark: #89B8CA;   /* Azul pastel oscuro */
        --pastel-secondary: #D4A5C8;      /* Lila pastel */
        --pastel-accent: #FFB6C1;         /* Rosa pastel */
        --pastel-success: #C1E1C1;        /* Verde pastel */
        --pastel-warning: #FFD8A8;        /* Naranja pastel */
        --pastel-danger: #FFA7A7;         /* Rojo pastel */
        --pastel-info: #B5D2E7;           /* Azul claro pastel */
        --pastel-light: #FAF9F6;          /* Blanco crema */
        --pastel-dark: #5A6D7B;           /* Gris azulado suave */
        --pastel-border: #E8E6E1;         /* Borde suave */
        --pastel-shadow: rgba(168, 213, 226, 0.15);
    }

    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Estilos principales */
    .stApp {
        background-color: var(--pastel-light);
        font-family: 'Inter', sans-serif;
        color: var(--pastel-dark);
    }
    
    /* Fuentes para encabezados */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600;
        color: var(--pastel-dark);
    }
    
    /* Ocultar barra lateral */
    .css-1d391kg {
        display: none !important;
    }
    
    /* Estilo de contenedor principal */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100%;
        background-color: var(--pastel-light);
    }
    
    /* Transiciones suaves */
    .metric-card, .stButton > button, .stFileUploader > div > div > div > div {
        transition: all 0.3s ease;
    }

    /* Encabezado principal con gradiente suave */
    .main-header {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--pastel-primary), var(--pastel-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem;
        letter-spacing: -0.5px;
        font-family: 'Poppins', sans-serif;
    }

    /* Subtítulo con estilo suave */
    .subtitle {
        text-align: center;
        color: var(--pastel-dark);
        font-size: 1.3rem;
        font-weight: 400;
        margin-bottom: 2.5rem;
        padding: 0 2rem;
        font-family: 'Inter', sans-serif;
        opacity: 0.8;
        line-height: 1.6;
    }

    /* Encabezados de sección con acentos pastel */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--pastel-dark);
        padding: 1.2rem 1.5rem;
        margin: 2.5rem 0 1.5rem 0;
        background: linear-gradient(90deg, var(--pastel-primary), transparent);
        border-left: 5px solid var(--pastel-secondary);
        border-radius: 0 15px 15px 0;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 2px 8px var(--pastel-shadow);
        position: relative;
        overflow: hidden;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transform: translateX(-100%);
    }
    
    .section-header:hover::before {
        transform: translateX(100%);
        transition: transform 0.6s ease;
    }

    /* Tarjetas de métricas mejoradas con colores pastel */
    .metric-card {
        background: linear-gradient(135deg, var(--pastel-primary), var(--pastel-info));
        padding: 1.8rem 1.2rem;
        border-radius: 18px;
        color: var(--pastel-dark);
        text-align: center;
        margin: 0.8rem;
        box-shadow: 0 4px 15px var(--pastel-shadow);
        border: 2px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        transform: rotate(45deg);
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(168, 213, 226, 0.25);
        border-color: var(--pastel-secondary);
    }
    
    .metric-card h3 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
        text-shadow: 1px 1px 2px rgba(90, 109, 123, 0.2);
        position: relative;
        z-index: 2;
    }
    
    .metric-card p {
        font-size: 0.95rem;
        color: white;
        margin: 0;
        font-weight: 500;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }

    /* Indicadores de riesgo pastel */
    .risk-high { 
        color: #FF6B6B;
        font-weight: 600;
        padding: 6px 16px;
        background: rgba(255, 107, 107, 0.15);
        border-radius: 20px;
        display: inline-block;
        border: 1px solid rgba(255, 107, 107, 0.3);
        font-family: 'Inter', sans-serif;
    }
    
    .risk-medium { 
        color: #FFA726;
        font-weight: 600;
        padding: 6px 16px;
        background: rgba(255, 167, 38, 0.15);
        border-radius: 20px;
        display: inline-block;
        border: 1px solid rgba(255, 167, 38, 0.3);
        font-family: 'Inter', sans-serif;
    }
    
    .risk-low { 
        color: #66BB6A;
        font-weight: 600;
        padding: 6px 16px;
        background: rgba(102, 187, 106, 0.15);
        border-radius: 20px;
        display: inline-block;
        border: 1px solid rgba(102, 187, 106, 0.3);
        font-family: 'Inter', sans-serif;
    }

    /* Subidor de archivos con estilo pastel */
    .stFileUploader > div > div > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px dashed var(--pastel-primary);
        border-radius: 15px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div > div > div:hover {
        border-color: var(--pastel-secondary);
        background-color: rgba(168, 213, 226, 0.1);
        transform: translateY(-2px);
    }

    /* Estilo de botones con gradiente pastel */
    .stButton > button {
        background: linear-gradient(135deg, var(--pastel-primary), var(--pastel-secondary));
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        font-family: 'Poppins', sans-serif;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px var(--pastel-shadow);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--pastel-secondary), var(--pastel-primary));
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(168, 213, 226, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    .stButton > button:disabled {
        background: linear-gradient(135deg, #E0E0E0, #BDBDBD);
        color: #9E9E9E;
        transform: none;
        box-shadow: none;
    }

    /* Estilo de pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(168, 213, 226, 0.1);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--pastel-primary) !important;
        color: white !important;
        font-weight: 600;
    }

    /* Estilo de expansores */
    .streamlit-expanderHeader {
        background-color: rgba(168, 213, 226, 0.1);
        border: 1px solid var(--pastel-border);
        border-radius: 12px;
        font-weight: 600;
        color: var(--pastel-dark);
        font-family: 'Inter', sans-serif;
        padding: 1rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(168, 213, 226, 0.2);
        border-color: var(--pastel-primary);
        transform: translateX(5px);
    }
    
    .streamlit-expanderContent {
        background-color: rgba(255, 255, 255, 0.9);
        border: 1px solid var(--pastel-border);
        border-radius: 0 0 12px 12px;
        padding: 1.5rem;
        margin-top: -1px;
    }

    /* Estilo de dataframes */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--pastel-border);
    }
    
    .dataframe th {
        background: linear-gradient(135deg, var(--pastel-primary), var(--pastel-info)) !important;
        color: white !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif;
    }
    
    .dataframe td {
        border-bottom: 1px solid var(--pastel-border) !important;
        font-family: 'Inter', sans-serif;
    }
    
    .dataframe tr:hover {
        background-color: rgba(168, 213, 226, 0.1) !important;
    }

    /* Estilo de divisores */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--pastel-primary), transparent);
        margin: 3rem 0;
    }

    /* Mensajes de éxito/error */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid var(--pastel-primary);
        font-family: 'Inter', sans-serif;
    }

    /* Barra de progreso */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--pastel-primary), var(--pastel-secondary));
        border-radius: 10px;
    }

    /* Estilo de métricas */
    .stMetric {
        background: rgba(168, 213, 226, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid var(--pastel-border);
    }
    
    .stMetric [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--pastel-dark);
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: var(--pastel-dark);
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }

    /* Contenedor de gráficos Plotly */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid var(--pastel-border);
        box-shadow: 0 4px 12px var(--pastel-shadow);
        background-color: white;
    }

    /* Estilo de botón de descarga */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--pastel-success), var(--pastel-info));
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, var(--pastel-info), var(--pastel-success));
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(193, 225, 193, 0.3);
    }

    /* Barra de desplazamiento personalizada */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(168, 213, 226, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--pastel-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--pastel-primary-dark);
    }

    /* Responsividad móvil */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        .main-header {
            font-size: 2.5rem;
        }
        
        .subtitle {
            font-size: 1.1rem;
            padding: 0 1rem;
        }
        
        .section-header {
            font-size: 1.5rem;
            padding: 1rem;
        }
        
        .metric-card {
            padding: 1.2rem;
            margin: 0.5rem 0;
        }
        
        .metric-card h3 {
            font-size: 2rem;
        }
    }

    /* Animación para elementos */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-card, .section-header {
        animation: fadeIn 0.6s ease-out;
    }

    /* Estilo de caja de información */
    .stInfo {
        background: linear-gradient(135deg, rgba(168, 213, 226, 0.1), rgba(212, 165, 200, 0.1));
        border-left: 4px solid var(--pastel-info);
        border-radius: 0 12px 12px 0;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-family: 'Inter', sans-serif;
    }

    /* Estilo de caja de selección */
    .stSelectbox [data-baseweb="select"] {
        border-radius: 10px;
        border: 2px solid var(--pastel-border);
        font-family: 'Inter', sans-serif;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: var(--pastel-primary);
    }

    /* Estilo de casillas de verificación */
    .stCheckbox [data-baseweb="checkbox"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stCheckbox label {
        font-family: 'Inter', sans-serif;
        color: var(--pastel-dark);
    }
</style>
""", unsafe_allow_html=True)

def get_logo_path():
    """Obtener la ruta del logo principal de ChurnChaser"""
    return "assets/churnchaser_logo_1753893225186.png"

def get_favicon_path():
    """Obtener la ruta del favicon (nuevo icono de ChurnChaser)"""
    return "assets/Churn Chaser icon_1753961019024.png"

def get_img_as_base64(img_path):
    """Convertir imagen a cadena base64 para incrustar en HTML"""
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def create_dummy_model():
    """Crear y guardar un modelo Random Forest de prueba"""
    if not os.path.exists("models"):
        os.makedirs("models")

    if not os.path.exists("models/churn_model.pkl"):
        # Crear un modelo Random Forest simple
        np.random.seed(42)
        X_dummy = np.random.rand(1000, 5)  # 5 características
        y_dummy = np.random.randint(0, 2, 1000)  # Objetivo binario

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_dummy, y_dummy)

        with open("models/churn_model.pkl", "wb") as f:
            pickle.dump(model, f)

def load_model():
    """Cargar el modelo entrenado"""
    try:
        with open("models/churn_model.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error("Archivo de modelo no encontrado. Creando modelo de prueba...")
        create_dummy_model()
        with open("models/churn_model.pkl", "rb") as f:
            return pickle.load(f)

def validate_data(df):
    """Validar que los datos subidos tengan las columnas requeridas"""
    required_columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'SupportTickets', 'Tenure']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return False, missing_columns
    return True, []

def categorize_risk(probability):
    """Categorizar probabilidad de abandono en niveles de riesgo"""
    if probability >= 0.7:
        return "Alto"
    elif probability >= 0.4:
        return "Medio"
    else:
        return "Bajo"

def style_risk(risk):
    """Aplicar estilos CSS a categorías de riesgo"""
    if risk == "Alto":
        return f'<span class="risk-high">{risk}</span>'
    elif risk == "Medio":
        return f'<span class="risk-medium">{risk}</span>'
    else:
        return f'<span class="risk-low">{risk}</span>'

def create_sample_data():
    """Crear datos de muestra para pruebas"""
    if not os.path.exists("sample_data"):
        os.makedirs("sample_data")

    if not os.path.exists("sample_data/customer_data.csv"):
        np.random.seed(42)
        n_customers = 100

        data = {
            'CustomerID': [f'CUST_{i:04d}' for i in range(1, n_customers + 1)],
            'Recency': np.random.randint(1, 365, n_customers),
            'Frequency': np.random.uniform(0.1, 10.0, n_customers).round(2),
            'Monetary': np.random.uniform(10.0, 1000.0, n_customers).round(2),
            'SupportTickets': np.random.randint(0, 15, n_customers),
            'Tenure': np.random.randint(1, 60, n_customers)
        }

        df = pd.DataFrame(data)
        df.to_csv("sample_data/customer_data.csv", index=False)

def main():
    # Inicializar estado de sesión
    if 'predictions' not in st.session_state:
        st.session_state.predictions = None

    # Crear datos de muestra y modelo si no existen
    create_sample_data()
    create_dummy_model()

    # Encabezado con logo y texto
    st.markdown('''
    <div style="text-align: center; padding: 2rem 0;">
        <h1 class="main-header">ChurnChaser</h1>
        <p class="subtitle">Predice el Riesgo de Abandono de Clientes con Análisis Impulsado por IA</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("---")

    # Contenido principal
    st.markdown('<div class="section-header">📊 Carga y Validación de Datos</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(168, 213, 226, 0.1), rgba(212, 165, 200, 0.1)); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; border: 2px dashed rgba(168, 213, 226, 0.3);">
        <p style="text-align: center; color: var(--pastel-dark); font-size: 1.1rem; margin: 0;">
            Sube tu archivo CSV de datos de clientes para comenzar el análisis
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Selecciona tu archivo CSV de datos de clientes",
        type=['csv'],
        help="Columnas requeridas: CustomerID, Recency, Frequency, Monetary, SupportTickets, Tenure"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Validación de datos
            is_valid, missing_cols = validate_data(df)

            if not is_valid:
                st.error(f"❌ Columnas requeridas faltantes: {', '.join(missing_cols)}")
                st.info("Columnas requeridas: CustomerID, Recency, Frequency, Monetary, SupportTickets, Tenure")
                return

            st.success("✅ ¡Validación de datos exitosa!")
        except Exception as e:
            st.error(f"❌ Error al leer archivo CSV: {str(e)}")
            return

        # Vista previa de datos
        st.markdown('<div class="section-header">👀 Vista Previa de Datos</div>', unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True)

        # Resumen de datos con tarjetas mejoradas
        st.markdown('<div class="section-header">📈 Resumen de Datos</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'''
            <div class="metric-card" style="background: linear-gradient(135deg, var(--pastel-primary), var(--pastel-info));">
                <h3>{len(df)}</h3>
                <p>Clientes Totales</p>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="metric-card" style="background: linear-gradient(135deg, var(--pastel-secondary), var(--pastel-accent));">
                <h3>{df.shape[1]}</h3>
                <p>Características</p>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            avg_tenure = df['Tenure'].mean()
            st.markdown(f'''
            <div class="metric-card" style="background: linear-gradient(135deg, var(--pastel-success), var(--pastel-info));">
                <h3>{avg_tenure:.1f}</h3>
                <p>Antigüedad Promedio (meses)</p>
            </div>
            ''', unsafe_allow_html=True)
        with col4:
            avg_monetary = df['Monetary'].mean()
            st.markdown(f'''
            <div class="metric-card" style="background: linear-gradient(135deg, var(--pastel-warning), var(--pastel-accent));">
                <h3>${avg_monetary:.0f}</h3>
                <p>Valor Promedio de Orden</p>
            </div>
            ''', unsafe_allow_html=True)

        # Sección de predicción
        st.markdown('<div class="section-header">🤖 Predicción de Abandono</div>', unsafe_allow_html=True)
        
        if st.button("🔮 Generar Predicciones", type="primary", use_container_width=True):
            with st.spinner("Analizando datos de clientes y prediciendo abandono..."):
                # Cargar modelo y hacer predicciones
                model = load_model()

                # Preparar características (excluir CustomerID)
                feature_columns = ['Recency', 'Frequency', 'Monetary', 'SupportTickets', 'Tenure']
                X = df[feature_columns]

                # Hacer predicciones
                probabilities = model.predict_proba(X)[:, 1]  # Probabilidad de abandono

                # Crear dataframe de resultados
                results_df = pd.DataFrame({
                    'CustomerID': df['CustomerID'],
                    'Probabilidad_Abandono': probabilities,
                    'Categoria_Riesgo': [categorize_risk(p) for p in probabilities]
                })

                # Ordenar por probabilidad de abandono (mayor primero)
                results_df = results_df.sort_values('Probabilidad_Abandono', ascending=False)

                st.session_state.predictions = results_df
                st.success("✅ ¡Predicciones generadas exitosamente!")

        # Mostrar predicciones si están disponibles
        if st.session_state.predictions is not None:
            results_df = st.session_state.predictions

            st.markdown('<div class="section-header">📈 Resultados de Predicción</div>', unsafe_allow_html=True)

            # Métricas de resumen
            alto_riesgo = len(results_df[results_df['Categoria_Riesgo'] == 'Alto'])
            medio_riesgo = len(results_df[results_df['Categoria_Riesgo'] == 'Medio'])
            bajo_riesgo = len(results_df[results_df['Categoria_Riesgo'] == 'Bajo'])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🔴 Alto Riesgo", alto_riesgo, f"{alto_riesgo/len(results_df)*100:.1f}%")
            with col2:
                st.metric("🟡 Riesgo Medio", medio_riesgo, f"{medio_riesgo/len(results_df)*100:.1f}%")
            with col3:
                st.metric("🟢 Bajo Riesgo", bajo_riesgo, f"{bajo_riesgo/len(results_df)*100:.1f}%")

            # Tabla de resultados
            st.markdown('<div class="section-header">📋 Resultados Detallados</div>', unsafe_allow_html=True)
            display_df = results_df.copy()
            display_df['Probabilidad_Abandono'] = display_df['Probabilidad_Abandono'].apply(lambda x: f"{x:.3f}")
            st.dataframe(display_df, use_container_width=True)

            # Visualizaciones
            st.markdown('<div class="section-header">📊 Distribución de Riesgo</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                # Gráfico de pastel con colores pastel
                risk_counts = results_df['Categoria_Riesgo'].value_counts()
                colors = {'Alto': '#FF6B6B', 'Medio': '#FFA726', 'Bajo': '#66BB6A'}

                fig_pie = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Distribución de Riesgo de Abandono",
                    color=risk_counts.index,
                    color_discrete_map=colors
                )
                fig_pie.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    marker=dict(line=dict(color='white', width=2))
                )
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif")
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                # Top 10 clientes con mayor riesgo
                top_10 = results_df.head(10)
                fig_bar = px.bar(
                    top_10,
                    x='Probabilidad_Abandono',
                    y='CustomerID',
                    orientation='h',
                    title="Top 10 Clientes en Riesgo",
                    color='Probabilidad_Abandono',
                    color_continuous_scale='reds'
                )
                fig_bar.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif")
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # Sección de exportación con formatos personalizables
            st.markdown('<div class="section-header">💾 Exportación de Datos con Un Clic</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Formato de Exportación**")
                export_format = st.selectbox(
                    "Elige formato:",
                    ["CSV", "Excel", "JSON", "CSV Filtrado"],
                    help="Selecciona tu formato de exportación preferido"
                )
            
            with col2:
                st.markdown("**🎯 Opciones de Exportación**")
                risk_filter = "Todos los Clientes"
                include_insights = True
                
                if export_format == "CSV Filtrado":
                    risk_filter = st.selectbox(
                        "Filtrar por riesgo:",
                        ["Todos los Clientes", "Solo Alto Riesgo", "Solo Riesgo Medio", "Solo Bajo Riesgo", "Alto + Riesgo Medio"],
                        help="Elige qué clientes incluir"
                    )
                else:
                    include_insights = st.checkbox("Incluir Reporte Resumen", value=True, help="Agregar resumen de análisis a la exportación")

            # Preparar datos de exportación basados en selección
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            avg_prob = results_df['Probabilidad_Abandono'].mean()
            
            if export_format == "CSV Filtrado":
                # Filtrar datos basados en selección
                if risk_filter == "Solo Alto Riesgo":
                    export_df = results_df[results_df['Categoria_Riesgo'] == 'Alto'].copy()
                    filename = f"clientes_alto_riesgo_{timestamp}.csv"
                elif risk_filter == "Solo Riesgo Medio":
                    export_df = results_df[results_df['Categoria_Riesgo'] == 'Medio'].copy()
                    filename = f"clientes_riesgo_medio_{timestamp}.csv"
                elif risk_filter == "Solo Bajo Riesgo":
                    export_df = results_df[results_df['Categoria_Riesgo'] == 'Bajo'].copy()
                    filename = f"clientes_bajo_riesgo_{timestamp}.csv"
                elif risk_filter == "Alto + Riesgo Medio":
                    export_df = results_df[results_df['Categoria_Riesgo'].isin(['Alto', 'Medio'])].copy()
                    filename = f"clientes_en_riesgo_{timestamp}.csv"
                else:
                    export_df = results_df.copy()
                    filename = f"todas_predicciones_{timestamp}.csv"
                
                export_data = export_df.to_csv(index=False)
                mime_type = "text/csv"
                
            elif export_format == "JSON":
                export_data = results_df.to_json(orient='records', indent=2)
                filename = f"predicciones_abandono_{timestamp}.json"
                mime_type = "application/json"
                
            elif export_format == "Excel":
                # Crear archivo Excel con múltiples hojas
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
                    # Hoja principal de datos
                    results_df.to_excel(writer, sheet_name='Predicciones', index=False)
                    
                    # Hoja de resumen
                    summary_data = {
                        'Métrica': ['Clientes Totales', 'Alto Riesgo', 'Riesgo Medio', 'Bajo Riesgo', 'Probabilidad Promedio de Abandono'],
                        'Valor': [len(results_df), alto_riesgo, medio_riesgo, bajo_riesgo, f"{avg_prob:.1%}"],
                        'Porcentaje': ['100%', f"{alto_riesgo/len(results_df)*100:.1f}%", 
                                     f"{medio_riesgo/len(results_df)*100:.1f}%", 
                                     f"{bajo_riesgo/len(results_df)*100:.1f}%", '-']
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Resumen', index=False)
                    
                    # Solo clientes de alto riesgo
                    if alto_riesgo > 0:
                        alto_riesgo_df = results_df[results_df['Categoria_Riesgo'] == 'Alto']
                        alto_riesgo_df.to_excel(writer, sheet_name='Clientes Alto Riesgo', index=False)
                
                export_data = output.getvalue()
                filename = f"analisis_abandono_{timestamp}.xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
            else:  # CSV
                if include_insights:
                    # Agregar resumen como comentarios de encabezado
                    summary_text = f"""# Reporte de Análisis ChurnChaser - {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
# Clientes Totales: {len(results_df)}
# Alto Riesgo: {alto_riesgo} ({alto_riesgo/len(results_df)*100:.1f}%)
# Riesgo Medio: {medio_riesgo} ({medio_riesgo/len(results_df)*100:.1f}%)
# Bajo Riesgo: {bajo_riesgo} ({bajo_riesgo/len(results_df)*100:.1f}%)
# Probabilidad Promedio de Abandono: {avg_prob:.1%}
#
"""
                    export_data = summary_text + results_df.to_csv(index=False)
                else:
                    export_data = results_df.to_csv(index=False)
                filename = f"predicciones_abandono_{timestamp}.csv"
                mime_type = "text/csv"

            # Botones de exportación
            st.markdown('<div class="section-header">📥 Opciones de Descarga</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label=f"🚀 Exportar {export_format}",
                    data=export_data,
                    file_name=filename,
                    mime=mime_type,
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                # Exportación rápida para clientes de alto riesgo
                if alto_riesgo > 0:
                    alto_riesgo_data = results_df[results_df['Categoria_Riesgo'] == 'Alto'].to_csv(index=False)
                    st.download_button(
                        label="⚠️ Solo Alto Riesgo",
                        data=alto_riesgo_data,
                        file_name=f"clientes_urgentes_{timestamp}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.button("⚠️ Solo Alto Riesgo", disabled=True, use_container_width=True, help="No se encontraron clientes de alto riesgo")
            
            with col3:
                # Exportar reporte de resumen
                summary_report = f"""Resumen de Análisis ChurnChaser
Generado: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

Análisis de Riesgo de Clientes:
- Clientes Totales Analizados: {len(results_df)}
- Alto Riesgo (≥70%): {alto_riesgo} clientes ({alto_riesgo/len(results_df)*100:.1f}%)
- Riesgo Medio (40-69%): {medio_riesgo} clientes ({medio_riesgo/len(results_df)*100:.1f}%)
- Bajo Riesgo (<40%): {bajo_riesgo} clientes ({bajo_riesgo/len(results_df)*100:.1f}%)

Hallazgos Clave:
- Probabilidad Promedio de Abandono: {avg_prob:.1%}
- Clientes que Requieren Acción Inmediata: {alto_riesgo}
- Clientes a Monitorear: {medio_riesgo}

Recomendaciones:
{f"🚨 URGENTE: {alto_riesgo} clientes necesitan esfuerzos de retención inmediata" if alto_riesgo > 0 else ""}
{f"⚠️ MONITOREAR: {medio_riesgo} clientes deben ser atendidos proactivamente" if medio_riesgo > 0 else ""}
{f"✅ ESTABLE: {bajo_riesgo} clientes probablemente permanecerán leales" if bajo_riesgo > 0 else ""}
"""
                st.download_button(
                    label="📋 Reporte Resumen",
                    data=summary_report,
                    file_name=f"resumen_abandono_{timestamp}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            # Perspectivas adicionales
            with st.expander("📋 Perspectivas Accionables", expanded=False):
                avg_prob = results_df['Probabilidad_Abandono'].mean()
                st.write(f"**Riesgo General de Abandono:** {avg_prob:.1%}")

                if alto_riesgo > 0:
                    st.write(f"🚨 **Acción Inmediata Requerida:** {alto_riesgo} clientes tienen alto riesgo de abandono (≥70%)")
                    st.write("- Considera campañas de retención dirigidas")
                    st.write("- Ofrece descuentos o incentivos personalizados")
                    st.write("- Contacta con llamadas de éxito del cliente")

                if medio_riesgo > 0:
                    st.write(f"⚠️ **Monitorear de Cerca:** {medio_riesgo} clientes tienen riesgo medio de abandono (40-69%)")
                    st.write("- Implementa campañas de engagement")
                    st.write("- Recolecta retroalimentación mediante encuestas")
                    st.write("- Ofrece beneficios del programa de lealtad")

    else:
        # Mostrar información de datos de muestra cuando no se sube archivo
        st.info("👆 Sube un archivo CSV para comenzar, o descarga los datos de muestra de abajo para probar la aplicación.")

        st.markdown('<div class="section-header">📋 Formato de Datos Requerido</div>', unsafe_allow_html=True)

        required_format = pd.DataFrame({
            'Columna': ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'SupportTickets', 'Tenure'],
            'Descripción': [
                'Identificador único del cliente',
                'Días desde la última compra',
                'Compras promedio por mes',
                'Valor promedio de orden ($)',
                'Número de tickets de soporte/quejas',
                'Meses como cliente'
            ],
            'Tipo de Dato': ['String/Entero', 'Entero', 'Decimal', 'Decimal', 'Entero', 'Entero'],
            'Ejemplo': ['CUST_0001', '45', '2.5', '150.00', '3', '24']
        })

        st.dataframe(required_format, use_container_width=True)

        # Cómo funciona y sección de datos de muestra
        st.markdown('<div class="section-header">❓ Cómo Funciona & Datos de Muestra</div>', unsafe_allow_html=True)
        
        with st.expander("🔄 Cómo Funciona ChurnChaser", expanded=False):
            st.markdown("""
            **ChurnChaser es una herramienta de predicción de retención de clientes impulsada por IA diseñada para negocios de eCommerce.**
            
            Sube tus datos de clientes y obtén perspectivas instantáneas sobre qué clientes están en riesgo de abandonar.
            
            **Proceso de 5 Pasos:**
            1. **Sube** tu archivo CSV de clientes
            2. **Valida** formato de datos y columnas  
            3. **Predice** probabilidad de abandono usando ML
            4. **Visualiza** distribución de riesgo
            5. **Exporta** resultados para tomar acción
            """)
        
        with st.expander("📊 Descargar Conjuntos de Datos de Muestra", expanded=False):
            st.markdown("**Elige entre 3 conjuntos de datos realistas para probar ChurnChaser:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📦 Tienda General**")
                st.write("100 clientes con mezcla balanceada de comportamientos")
                if st.button("Descargar Datos Tienda General", key="general_btn", use_container_width=True):
                    sample_df = pd.read_csv("sample_data/customer_data.csv")
                    csv = sample_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name="tienda_general_muestra.csv",
                        mime="text/csv",
                        key="general_download",
                        use_container_width=True
                    )
            
            with col2:
                st.markdown("**👗 Tienda de Moda**")
                st.write("200 clientes con patrones estacionales")
                if st.button("Descargar Datos Tienda de Moda", key="fashion_btn", use_container_width=True):
                    sample_df = pd.read_csv("sample_data/fashion_store_data.csv")
                    csv = sample_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name="tienda_moda_muestra.csv",
                        mime="text/csv",
                        key="fashion_download",
                        use_container_width=True
                    )
            
            with col3:
                st.markdown("**💻 Tienda de Tecnología**")
                st.write("250 clientes con transacciones de alto valor")
                if st.button("Descargar Datos Tienda de Tecnología", key="tech_btn", use_container_width=True):
                    sample_df = pd.read_csv("sample_data/tech_store_data.csv")
                    csv = sample_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name="tienda_tecnologia_muestra.csv",
                        mime="text/csv",
                        key="tech_download",
                        use_container_width=True
                    )
        
        with st.expander("🎯 Entendiendo las Categorías de Riesgo", expanded=False):
            st.markdown("""
            **Rangos de Probabilidad de Abandono:**
            
            - 🔴 **Alto Riesgo (≥70%)**: Clientes muy propensos a abandonar - requieren acción inmediata
            - 🟡 **Riesgo Medio (40-69%)**: Clientes mostrando señales de advertencia - deben ser monitoreados  
            - 🟢 **Bajo Riesgo (<40%)**: Clientes leales - probablemente permanecerán comprometidos
            
            **Factores Clave Considerados:**
            - **Recencia**: Días desde la última compra (mayor = más riesgo)
            - **Frecuencia**: Frecuencia de compra (menor = más riesgo)
            - **Monetario**: Valor promedio de orden (menor = más riesgo)
            - **Tickets de Soporte**: Número de quejas (mayor = más riesgo)
            - **Antigüedad**: Meses como cliente (menor = más riesgo)
            """)
        
        with st.expander("📈 Opciones de Exportación Explicadas", expanded=False):
            st.markdown("""
            **Formatos de Exportación Disponibles:**
            
            - **CSV**: Formato estándar con comentarios de resumen
            - **Excel**: Libro de trabajo multi-hoja con Predicciones, Resumen y Clientes Alto Riesgo
            - **JSON**: Formato legible por máquina para integración API
            - **CSV Filtrado**: Exportar categorías de riesgo específicas solamente
            
            **Opciones de Exportación Rápida:**
            - **Solo Alto Riesgo**: Lista de acción inmediata para clientes urgentes
            - **Reporte Resumen**: Resumen ejecutivo con hallazgos clave y recomendaciones
            
            Todas las exportaciones incluyen timestamp y están listas para tu CRM o herramientas de marketing.
            """)
            
        st.info("💡 **Consejo**: ¡Comienza descargando cualquiera de los conjuntos de datos de arriba para ver ChurnChaser en acción con registros de clientes realistas!")

if __name__ == "__main__":
    main()