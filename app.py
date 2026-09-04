import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Fragilidad Predial",
    page_icon="📊",
    layout="wide",
)


# Cargar y limpiar datos
@st.cache_data
def load_data():
    df_ed = pd.read_excel("Base de Datos.xlsx", sheet_name="EDIFICACIONES")
    df_clean = df_ed.iloc[2:].copy()

    df_clean.columns = [
        "ID",
        "Direccion",
        "Longitud",
        "Latitud",
        "Ubicacion_Manzana",
        "Num_Pisos",
        "Area_Construida_m2",
        "Estado_Construccion",
        "Calidad_Construccion",
        "Servicios_Publicos",
        "Num_Habitantes",
        "Cimentacion",
        "Sistema_Entrepisos",
        "Sistema_Estructural",
        "Sistema_Cubierta",
        "Fecha_Construccion",
        "Reformas",
        "Irregularidad_Planta",
        "Irregularidad_Altura",
        "Tipologia_Estructural",
        "Causa_Daños",
        "Consecuencias_Daños",
        "Inundaciones_Previas",
        "Daños_Elem_Verticales",
        "Daños_Elem_Horizontales",
        "Daños_Elem_NoEstructurales",
        "Sistema_Aguas_Servidas",
        "Reparacion_Daños",
        "Zonas_Exposicion",
        "STIP",
        "SALT",
        "SCON",
        "SED",
        "SE",
        "Pct_SE",
        "Categoria_Fragilidad",
        "SPER",
    ]

    # Limpieza de datos
    df_clean["Num_Pisos"] = pd.to_numeric(
        df_clean["Num_Pisos"], errors="coerce"
    )
    df_clean["Area_Construida_m2"] = pd.to_numeric(
        df_clean["Area_Construida_m2"], errors="coerce"
    )
    df_clean["Num_Habitantes"] = pd.to_numeric(
        df_clean["Num_Habitantes"], errors="coerce"
    )
    df_clean["SE"] = pd.to_numeric(df_clean["SE"], errors="coerce")
    df_clean["Categoria_Fragilidad"] = (
        df_clean["Categoria_Fragilidad"]
        .astype(str)
        .str.strip()
        .replace({"Muy alta": "Muy Alta"})
    )
    df_clean["Estado_Construccion"] = (
        df_clean["Estado_Construccion"].astype(str).str.strip()
    )

    return df_clean


df = load_data()

# Encabezado principal
st.title("📊 Dashboard Interactivo de Fragilidad y Vulnerabilidad Predial")
st.markdown(
    "Evaluación del riesgo estructural y características socioeconómicas de los predios inspeccionados."
)

# --- BARRA LATERAL: FILTROS INTERACTIVOS ---
st.sidebar.header("🔍 Filtros Dinámicos")

frag_options = ["Todas"] + list(df["Categoria_Fragilidad"].unique())
selected_frag = st.sidebar.selectbox(
    "Nivel de Fragilidad:", frag_options, index=0
)

estado_options = ["Todos"] + list(df["Estado_Construccion"].unique())
selected_estado = st.sidebar.selectbox(
    "Estado de Construcción:", estado_options, index=0
)

df_filtered = df.copy()
if selected_frag != "Todas":
    df_filtered = df_filtered[
        df_filtered["Categoria_Fragilidad"] == selected_frag
    ]
if selected_estado != "Todos":
    df_filtered = df_filtered[
        df_filtered["Estado_Construccion"] == selected_estado
    ]

# --- TARJETAS DE INDICADORES (KPIs) ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_predios = len(df_filtered)
alta_muy_alta = len(
    df_filtered[
        df_filtered["Categoria_Fragilidad"].isin(["Alta", "Muy Alta"])
    ]
)
pct_critico = (
    (alta_muy_alta / total_predios * 100) if total_predios > 0 else 0
)
promedio_se = df_filtered["SE"].mean() if total_predios > 0 else 0
total_habitantes = df_filtered["Num_Habitantes"].sum()

kpi1.metric("Total Predios Filtrados", f"{total_predios}")
kpi2.metric("Vulnerabilidad Alta/Muy Alta", f"{pct_critico:.1f}%")
kpi3.metric("Índice SE Promedio", f"{promedio_se:.3f}")
kpi4.metric("Población Expuesta", f"{int(total_habitantes)} pers.")

st.markdown("---")

# --- GRÁFICOS INTERACTIVOS (FILA 1) ---
col1, col2 = st.columns(2)

color_discrete_map = {
    "Muy Alta": "#d9534f",
    "Alta": "#f0ad4e",
    "Media-Alta": "#f0e68c",
    "Media": "#5cb85c",
}

with col1:
    st.subheader("1. Distribución por Categoría de Fragilidad")
    fig1 = px.bar(
        df_filtered["Categoria_Fragilidad"]
        .value_counts()
        .reset_index(name="Cantidad"),
        x="Categoria_Fragilidad",
        y="Cantidad",
        color="Categoria_Fragilidad",
        color_discrete_map=color_discrete_map,
        labels={
            "Categoria_Fragilidad": "Fragilidad",
            "Cantidad": "N° de Predios",
        },
        text_auto=True,
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("2. Estado de la Construcción")
    fig2 = px.pie(
        df_filtered,
        names="Estado_Construccion",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- GRÁFICOS INTERACTIVOS (FILA 2) ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Dispersión del Índice SE por Categoría")
    fig3 = px.box(
        df_filtered,
        x="Categoria_Fragilidad",
        y="SE",
        color="Categoria_Fragilidad",
        color_discrete_map=color_discrete_map,
        points="all",
        labels={"SE": "Índice SE", "Categoria_Fragilidad": "Categoría"},
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("4. Número de Pisos por Predio")
    fig4 = px.histogram(
        df_filtered,
        x="Num_Pisos",
        color="Categoria_Fragilidad",
        color_discrete_map=color_discrete_map,
        barmode="group",
        labels={"Num_Pisos": "Número de Pisos"},
    )
    st.plotly_chart(fig4, use_container_width=True)

# --- TABLA DETALLADA ---
st.markdown("---")
st.subheader("📋 Detalle de la Base de Datos")
st.dataframe(
    df_filtered[
        [
            "ID",
            "Direccion",
            "Num_Pisos",
            "Estado_Construccion",
            "Sistema_Estructural",
            "Categoria_Fragilidad",
            "SE",
            "Num_Habitantes",
        ]
    ],
    use_container_width=True,
)
