import streamlit as st
import pandas as pd
import re
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Dashboard AVR - Riesgo Predial", layout="wide")

st.title("📊 Evaluación de Riesgo por Pérdidas Económicas Directas")
st.markdown("Sector Calucaima - Análisis Dinámico, Georreferenciado y Descriptivo")

# 1. Cargar base de datos y renombrar columnas duplicadas
@st.cache_data
def cargar_datos():
    df_raw = pd.read_excel("Base de Datos.xlsx")
    
    # Buscar la fila que contiene las palabras claves 'LONGITUD' o 'LATITUD' o 'PREDIO'
    fila_encabezado = None
    for idx, row in df_raw.iterrows():
        valores_fila = [str(val).upper().strip() for val in row.values]
        if any('LONGITUD' in v for v in valores_fila) or any('LATITUD' in v for v in valores_fila):
            fila_encabezado = idx
            break
            
    if fila_encabezado is not None:
        nuevos_encabezados = []
        for i, val in enumerate(df_raw.iloc[fila_encabezado].values):
            if pd.notna(val) and str(val).strip() != '' and not str(val).startswith('Unnamed'):
                nuevos_encabezados.append(str(val).strip())
            else:
                val_sup = df_raw.columns[i]
                if pd.notna(val_sup) and not str(val_sup).startswith('Unnamed'):
                    nuevos_encabezados.append(str(val_sup).strip())
                else:
                    nuevos_encabezados.append(f"Columna_{i+1}")
                    
        df_clean = df_raw.iloc[fila_encabezado + 1:].copy().reset_index(drop=True)
        df_clean.columns = nuevos_encabezados
    else:
        df_clean = df_raw.copy()
        df_clean.columns = [str(c).strip() for c in df_clean.columns]
        
    # Eliminar columnas sin nombre / Unnamed residuales
    df_clean = df_clean.loc[:, ~df_clean.columns.str.startswith('Unnamed')]
    
    # RESOLVER COLUMNAS DUPLICADAS: Asigna subíndices únicos (ej: Col, Col.1, Col.2)
    cols = pd.Series(df_clean.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols == dup] = [f"{dup}.{i}" if i != 0 else dup for i in range(sum(cols == dup))]
    df_clean.columns = cols
    
    return df_clean

df = cargar_datos()

# 2. Función para convertir coordenadas sexagesimales (DMS) a decimales (WGS84)
def dms_a_decimal(coord_str, es_longitud=False):
    if not isinstance(coord_str, str) or not coord_str.strip() or coord_str in ['N/A', 'nan', 'None']:
        return None
    
    c = coord_str.strip().replace(',', '.')
    patron = r"(\d+)°\s*(\d+)'\s*([\d.]+)\"\s*([ONSEONSE])"
    coincidencia = re.search(patron, c)
    
    if coincidencia:
        grados = float(coincidencia.group(1))
        minutos = float(coincidencia.group(2))
        segundos = float(coincidencia.group(3))
        orientacion = coincidencia.group(4).upper()
        
        decimal = grados + (minutos / 60.0) + (segundos / 3600.0)
        
        if orientacion in ['O', 'W', 'S'] or es_longitud:
            decimal = -abs(decimal)
            
        return decimal
        
    try:
        val = float(c)
        if es_longitud:
            val = -abs(val)
        return val
    except ValueError:
        return None

# Identificar dinámicamente las columnas de Latitud y Longitud
col_lat = [c for c in df.columns if 'LATITUD' in str(c).upper()]
col_lon = [c for c in df.columns if 'LONGITUD' in str(c).upper()]

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

# 4. MAPA INTERACTIVO CON LOCALIZACIONES
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
        <b>Latitud:</b> {fila['lat_dec']:.6f}<br>
        <b>Longitud:</b> {fila['lon_dec']:.6f}<br>
        <b>Vulnerabilidad (V):</b> {fila['V_NUM'] if pd.notna(fila['V_NUM']) else 'N/A'}<br>
        <b>Pérdida Económica:</b> ${fila['Perdida_Economica']:,.2f} COP
        """
        folium.CircleMarker(
            location=[fila['lat_dec'], fila['lon_dec']],
            radius=8,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Predio: {fila[c_dir]}",
            color=obtener_color(fila['Perdida_Economica']),
            fill=True,
            fill_color=obtener_color(fila['Perdida_Economica']),
            fill_opacity=0.8
        ).add_to(m)

    st_folium(m, use_container_width=True, height=480)
else:
    st.warning("No se encontraron coordenadas válidas para desplegar el mapa.")

st.markdown("---")

# 5. ANÁLISIS EXPLORATORIO POR COLUMNA
st.subheader("📈 Análisis Exploratorio por Columna")

columnas_visibles = [c for c in df.columns if c not in ['lat_dec', 'lon_dec', 'AREA_NUM', 'PHI_NUM', 'V_NUM', 'Exposicion_E', 'Perdida_Economica']]

col_seleccionada = st.selectbox("Selecciona una columna para analizar sus datos:", columnas_visibles)

if col_seleccionada:
    serie_datos = df[col_seleccionada].dropna()
    serie_numerica = pd.to_numeric(serie_datos, errors='coerce').dropna()
    
    if len(serie_numerica) > len(serie_datos) * 0.5 and len(serie_numerica) > 0:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Promedio", f"{serie_numerica.mean():,.2f}")
        c2.metric("Mínimo", f"{serie_numerica.min():,.2f}")
        c3.metric("Máximo", f"{serie_numerica.max():,.2f}")
        c4.metric("Suma Total", f"{serie_numerica.sum():,.2f}")
        
        st.markdown(f"**Distribución de valores para:** `{col_seleccionada}`")
        df_chart = serie_numerica.value_counts().reset_index()
        df_chart.columns = ['Valor', 'Cantidad']
        st.bar_chart(df_chart.set_index('Valor'))
    else:
        conteo = serie_datos.value_counts().reset_index()
        conteo.columns = [col_seleccionada, 'Cantidad de Predios']
        
        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            st.dataframe(conteo, use_container_width=True)
        with col_t2:
            st.markdown(f"**Frecuencia por categoría en:** `{col_seleccionada}`")
            st.bar_chart(conteo.set_index(col_seleccionada))

st.markdown("---")

# 6. MATRIZ DE DATOS COMPLETA
st.subheader("📋 Matriz de Datos Consolidada")
st.dataframe(df[columnas_visibles], use_container_width=True)
