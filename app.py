import streamlit as st
import pandas as pd
import re
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Dashboard AVR - Riesgo Predial", layout="wide")

st.title("📊 Evaluación de Riesgo por Pérdidas Económicas Directas")
st.markdown("Sector Calucaima - Análisis Dinámico y Georreferenciado")

# 1. Cargar base de datos
@st.cache_data
def cargar_datos():
    return pd.read_excel("Base de Datos.xlsx")

df = cargar_datos()

# 2. Función para convertir coordenadas sexagesimales a decimales (WGS84)
def dms_a_decimal(coord_str, es_longitud=False):
    if not isinstance(coord_str, str) or not coord_str.strip() or coord_str == 'N/A':
        return None
    
    patron = r"(\d+)°\s*(\d+)'\s*([\d.]+)\"\s*([ONSEONSE])"
    coincidencia = re.search(patron, coord_str.strip())
    
    if coincidencia:
        grados = float(coincidencia.group(1))
        minutos = float(coincidencia.group(2))
        segundos = float(coincidencia.group(3))
        orientacion = coincidencia.group(4).upper()
        
        decimal = grados + (minutos / 60.0) + (segundos / 3600.0)
        
        if orientacion in ['O', 'W', 'S'] or es_longitud:
            decimal = -abs(decimal)
            
        return decimal
    return None

# Normalizar los nombres de las columnas para evitar errores de espacios o mayúsculas/minúsculas
df.columns = df.columns.str.strip().str.upper()

# Buscar la columna de latitud y longitud sin importar variaciones leves de nombre
col_lat = [c for c in df.columns if 'LAT' in c][0]
col_lon = [c for c in df.columns if 'LON' in c][0]

# Convertir coordenadas
df['lat_dec'] = df[col_lat].apply(lambda x: dms_a_decimal(str(x), es_longitud=False))
df['lon_dec'] = df[col_lon].apply(lambda x: dms_a_decimal(str(x), es_longitud=True))

# 3. Sidebar y Cálculos
costo_unitario = st.sidebar.number_input("Costo Unitario (COP/m²):", value=1650000, step=50000)

df['Exposicion_E'] = df['AREA (m2)'] * costo_unitario
df['Perdida_Economica'] = df['P(Hi)'] * df['V'] * df['Exposicion_E']

# 4. Sección de Mapa Interactivo
st.subheader("🗺️ Ubicación Espacial de Predios y Niveles de Riesgo")

df_mapa = df.dropna(subset=['lat_dec', 'lon_dec'])

if not df_mapa.empty:
    lat_centro = df_mapa['lat_dec'].mean()
    lon_centro = df_mapa['lon_dec'].mean()

    m = folium.Map(location=[lat_centro, lon_centro], zoom_start=18, tiles="OpenStreetMap")

    def obtener_color(perdida):
        if pd.isna(perdida):
            return 'gray'
        elif perdida > 80000:
            return 'red'
        elif perdida > 40000:
            return 'orange'
        else:
            return 'green'

    for _, fila in df_mapa.iterrows():
        popup_html = f"""
        <b>Predio:</b> {fila['DIRECCION PREDIO']}<br>
        <b>Pisos:</b> {fila['NUMERO DE PISOS']}<br>
        <b>Vulnerabilidad (V):</b> {fila['V']:.4f}<br>
        <b>Amenaza P(Hi):</b> {fila['P(Hi)']:.5f}<br>
        <b>Pérdida Económica:</b> ${fila['Perdida_Economica']:,.2f} COP
        """
        folium.CircleMarker(
            location=[fila['lat_dec'], fila['lon_dec']],
            radius=7,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Predio {fila['DIRECCION PREDIO']}",
            color=obtener_color(fila['Perdida_Economica']),
            fill=True,
            fill_opacity=0.8
        ).add_to(m)

    st_folium(m, use_container_width=True, height=500)
else:
    st.warning("No se encontraron coordenadas válidas para desplegar el mapa.")

# 5. Tabla Consolidada
st.subheader("📋 Matriz de Datos")
st.dataframe(df, use_container_width=True)
