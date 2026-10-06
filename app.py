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
    # Leer el archivo de Excel cargado en el repositorio
    df_temp = pd.read_excel("Base de Datos.xlsx")
    
    # Limpiar espacios en los nombres de las columnas
    df_temp.columns = [str(col).strip() for col in df_temp.columns]
    return df_temp

df = cargar_datos()

# Mostrar columnas detectadas en el sidebar para fácil verificación
st.sidebar.markdown("### 🔍 Columnas Detectadas")
st.sidebar.json(list(df.columns))

# 2. Función para convertir coordenadas sexagesimales a decimales (WGS84)
def dms_a_decimal(coord_str, es_longitud=False):
    if not isinstance(coord_str, str) or not coord_str.strip() or coord_str in ['N/A', 'nan', 'None']:
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
    
    # Si ya viene en formato numérico/decimal
    try:
        val = float(coord_str)
        if es_longitud:
            val = -abs(val)
        return val
    except ValueError:
        return None

# Identificar columnas de Latitud y Longitud
col_lat = None
col_lon = None

for col in df.columns:
    c_upper = str(col).upper()
    if 'LAT' in c_upper or 'NORTE' in c_upper or c_upper == 'Y':
        col_lat = col
    elif 'LON' in c_upper or 'ESTE' in c_upper or 'OESTE' in c_upper or c_upper == 'X':
        col_lon = col

# Aplicar conversión de coordenadas
if col_lat and col_lon:
    df['lat_dec'] = df[col_lat].apply(lambda x: dms_a_decimal(str(x), es_longitud=False))
    df['lon_dec'] = df[col_lon].apply(lambda x: dms_a_decimal(str(x), es_longitud=True))
else:
    df['lat_dec'] = None
    df['lon_dec'] = None

# 3. Sidebar y Cálculos
costo_unitario = st.sidebar.number_input("Costo Unitario (COP/m²):", value=1650000, step=50000)

# Buscar columnas de área, P(Hi) y Vulnerabilidad
col_area = [c for c in df.columns if 'AREA' in str(c).upper() or 'M2' in str(c).upper()]
col_phi = [c for c in df.columns if 'P(HI)' in str(c).upper() or 'AMENAZA' in str(c).upper() or 'P_HI' in str(c).upper()]
col_v = [c for c in df.columns if 'VULNERABILIDAD' in str(c).upper() or str(c).strip().upper() == 'V']

c_area = col_area[0] if col_area else df.columns[0]
c_phi = col_phi[0] if col_phi else df.columns[0]
c_v = col_v[0] if col_v else df.columns[0]

# Convertir a valores numéricos de forma segura
df['AREA_NUM'] = pd.to_numeric(df[c_area], errors='coerce')
df['PHI_NUM'] = pd.to_numeric(df[c_phi], errors='coerce')
df['V_NUM'] = pd.to_numeric(df[c_v], errors='coerce')

df['Exposicion_E'] = df['AREA_NUM'] * costo_unitario
df['Perdida_Economica'] = df['PHI_NUM'] * df['V_NUM'] * df['Exposicion_E']

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

    # Buscar columna de dirección
    col_dir = [c for c in df.columns if 'DIR' in str(c).upper() or 'PREDIO' in str(c).upper()]
    c_dir = col_dir[0] if col_dir else df.columns[0]

    for _, fila in df_mapa.iterrows():
        popup_html = f"""
        <b>Predio:</b> {fila[c_dir]}<br>
        <b>Vulnerabilidad (V):</b> {fila['V_NUM']:.4f}<br>
        <b>Amenaza P(Hi):</b> {fila['PHI_NUM']:.5f}<br>
        <b>Pérdida Económica:</b> ${fila['Perdida_Economica']:,.2f} COP
        """
        folium.CircleMarker(
            location=[fila['lat_dec'], fila['lon_dec']],
            radius=7,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Predio {fila[c_dir]}",
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
