import streamlit as st
import pandas as pd
import re
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Dashboard AVR - Riesgo Predial", layout="wide")

st.title("📊 Evaluación de Riesgo por Pérdidas Económicas Directas")
st.markdown("Sector Calucaima - Análisis Dinámico, Georreferenciado y Descriptivo")

# 1. Cargar y estructurar base de datos ajustando la fila de encabezados
@st.cache_data
def cargar_datos():
    df_clean = pd.read_excel("Base de Datos.xlsx", header=1)
    df_clean = df_clean.dropna(how='all').reset_index(drop=True)
    df_clean.columns = [str(c).strip() for c in df_clean.columns]
    return df_clean

df = cargar_datos()

# 2. Función de conversión sexagesimal a decimal (WGS84)
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
    return None

# Buscar columnas de latitud y longitud
col_lat = [c for c in df.columns if 'LATITUD' in c.upper()]
col_lon = [c for c in df.columns if 'LONGITUD' in c.upper()]

if col_lat and col_lon:
    df['lat_dec'] = df[col_lat[0]].apply(lambda x: dms_a_decimal(str(x), es_longitud=False))
    df['lon_dec'] = df[col_lon[0]].apply(lambda x: dms_a_decimal(str(x), es_longitud=True))
else:
    df['lat_dec'] = None
    df['lon_dec'] = None

# 3. Sidebar y Cálculos de Riesgo
st.sidebar.header("⚙️ Configuración del Modelo")
costo_unitario = st.sidebar.number_input("Costo Unitario (COP/m²):", value=1650000, step=50000)

col_area = [c for c in df.columns if 'AREA' in str(c).upper()]
col_phi = [c for c in df.columns if 'P(HI)' in str(c).upper() or 'AMENAZA' in str(c).upper()]
col_v = [c for c in df.columns if 'VULNERABILIDAD' in str(c).upper() or str(c).strip().upper() == 'V']

c_area = col_area[0] if col_area else df.columns[0]
c_phi = col_phi[0] if col_phi else df.columns[0]
c_v = col_v[0] if col_v else df.columns[0]

df['AREA_NUM'] = pd.to_numeric(df[c_area], errors='coerce')
df['PHI_NUM'] = pd.to_numeric(df[c_phi], errors='coerce')
df['V_NUM'] = pd.to_numeric(df[c_v], errors='coerce')

df['Exposicion_E'] = df['AREA_NUM'] * costo_unitario
df['Perdida_Economica'] = df['PHI_NUM'] * df['V_NUM'] * df['Exposicion_E']

# 4. Sección del Mapa Interactivo
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

    col_dir = [c for c in df.columns if 'DIR' in str(c).upper() or 'PREDIO' in str(c).upper()]
    c_dir = col_dir[0] if col_dir else df.columns[0]

    for _, fila in df_mapa.iterrows():
        popup_html = f"""
        <b>Predio:</b> {fila[c_dir]}<br>
        <b>Vulnerabilidad (V):</b> {fila['V_NUM']}<br>
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

    st_folium(m, use_container_width=True, height=450)
else:
    st.warning("No se encontraron coordenadas válidas para desplegar el mapa.")

st.markdown("---")

# 5. NUEVA SECCIÓN: Análisis Descriptivo por Columna
st.subheader("📈 Análisis Exploratorio por Columna")

# Filtrar columnas internas auxiliares
columnas_visibles = [c for c in df.columns if c not in ['lat_dec', 'lon_dec', 'AREA_NUM', 'PHI_NUM', 'V_NUM']]

col_seleccionada = st.selectbox("Selecciona una columna para analizar sus datos:", columnas_visibles)

if col_seleccionada:
    serie_datos = df[col_seleccionada].dropna()
    
    # Intentar convertir a numérico para análisis cuantitativo
    serie_numerica = pd.to_numeric(serie_datos, errors='coerce').dropna()
    
    # Si la mayoría de los datos son numéricos
    if len(serie_numerica) > len(serie_datos) * 0.5 and len(serie_numerica) > 0:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Promedio", f"{serie_numerica.mean():,.2f}")
        c2.metric("Mínimo", f"{serie_numerica.min():,.2f}")
        c3.metric("Máximo", f"{serie_numerica.max():,.2f}")
        c4.metric("Suma Total", f"{serie_numerica.sum():,.2f}")
        
        st.markdown(f"**Distribución de valores para:** `{col_seleccionada}`")
        st.bar_chart(serie_numerica.value_counts().sort_index())
        
    else:
        # Si es una variable cualitativa/texto
        conteo = serie_datos.value_counts().reset_index()
        conteo.columns = [col_seleccionada, 'Cantidad de Predios']
        
        col_t1, col_t2 = st.columns([1, 2])
        
        with col_t1:
            st.dataframe(conteo, use_container_width=True)
            
        with col_t2:
            st.markdown(f"**Frecuencia por categoría en:** `{col_seleccionada}`")
            st.bar_chart(conteo.set_index(col_seleccionada))

st.markdown("---")

# 6. Matriz de Datos Limpia
st.subheader("📋 Matriz de Datos Consolidada")
st.dataframe(df[columnas_visibles], use_container_width=True)
