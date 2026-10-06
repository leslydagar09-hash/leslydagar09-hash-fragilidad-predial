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
