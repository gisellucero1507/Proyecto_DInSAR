import streamlit as st
import pandas as pd
import plotly.express as px

# 1) Configuración de la página
st.set_page_config(
    page_title="Eventos de Precipitación Promedio",
    layout="wide"
)

# 2) Título y descripción
st.title("Eventos de Precipitación Promedio 🌧️")
st.markdown("""
Este panel visualiza los eventos de **precipitación promedio** registrados en diferentes fechas.  
Solo se grafican los días en que hubo lluvia registrada, diferenciando por corrida.
""")

# 3) Cargar el CSV con delimitador ;
df = pd.read_csv("./data/data_estructurada_precipitaciones.csv", delimiter=";")

# 4) Limpiar y convertir tipos
# Pasar todos los encabezados a minúsculas para evitar problemas
df.columns = df.columns.str.lower()

# Reparar columna rainfall: se reemplaza comas por puntos para decimales correctos y se convierten a float
df["rainfall"] = df["rainfall"].astype(str).str.replace(",", ".", regex=False)
df["rainfall"] = pd.to_numeric(df["rainfall"], errors="coerce")  # NaN si falla la conversión

# Convierte fechas sin format rígido para no perder datos, que Plotly requiere datetime
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")  

# Convertir 'corrida' a string para facilitar color y leyenda
df["corrida"] = df["corrida"].astype(str)

# 5) Filtrar filas que tienen lluvia registrada y fecha válida
df_lluvia = df.dropna(subset=["rainfall", "fecha"])

# 6) Crear figura general
fig = px.line(
    df_lluvia,
    x="fecha",
    y="rainfall",
    color="corrida",
    markers=True,
    title="Eventos de Precipitación Promedio (por Corrida)",
    labels={"fecha": "Fecha", "rainfall": "Precipitación (mm)", "corrida": "Corrida"},
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_traces(line_shape='spline')

# Forzar rango completo en eje x
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Precipitación (mm)",
    hovermode="x unified",
    legend_title_text="Corrida",
    template="plotly_dark",
    margin=dict(l=40, r=40, t=80, b=40),
    xaxis=dict(
        range=[df_lluvia['fecha'].min(), df_lluvia['fecha'].max()]
    )
)

# Mostrar mes y año espaciados cada 3 meses, rotar etiquetas
fig.update_xaxes(
    tickformat="%b %Y",   # Formato mes abreviado y año
    dtick="M3",           # Tick cada 3 meses
    tickangle=45
)

st.plotly_chart(fig, use_container_width=True)

# 7) Gráficas separadas por corridas
corridas = df_lluvia["corrida"].unique()
cols = st.columns(len(corridas))

for i, corrida in enumerate(sorted(corridas)):
    df_corrida = df_lluvia[df_lluvia["corrida"] == corrida]
    fig_corrida = px.line(
        df_corrida,
        x="fecha",
        y="rainfall",
        markers=True,
        title=f"Corrida {corrida}",
        labels={"fecha": "Fecha", "rainfall": "Precipitación (mm)"},
        color_discrete_sequence=[px.colors.qualitative.Pastel[i % len(px.colors.qualitative.Pastel)]]
    )
    fig_corrida.update_traces(line_shape='spline')
    fig_corrida.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Precipitación (mm)",
        hovermode="x unified",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False
    )

    cols[i].plotly_chart(fig_corrida, use_container_width=True)
    
#8) Histograma
# Crear columna con mes-año para agrupar precipitaciones mensuales
df_lluvia['mes_ano'] = df_lluvia['fecha'].dt.to_period('M').dt.to_timestamp()
# Agrupar precipitación total por mes-año
df_mensual = df_lluvia.groupby('mes_ano')['rainfall'].sum().reset_index()
fig_hist = px.bar(
    df_mensual,
    x='mes_ano',
    y='rainfall',
    labels={'mes_ano': 'Mes - Año', 'rainfall': 'Precipitación total (mm)'},
    title='Histograma de Precipitaciones Mensuales',
    template='plotly_dark',
    hover_data={'mes_ano': True, 'rainfall': True}  
)

# Formatear texto del eje x para que solo muestre el año
fig_hist.update_layout(
    xaxis_tickformat='%Y',
    xaxis_tickangle=0,
    margin=dict(l=40, r=40, t=60, b=40),
    hovermode='x unified'
)

# Mejorar formato del hover para que muestre el mes completo al pasar el mouse
fig_hist.data[0].hovertemplate = (
    'Mes y Año: %{x|%b %Y}<br>' 
    'Precipitación: %{y} mm<extra></extra>'
)

st.plotly_chart(fig_hist, use_container_width=True)

#9) Mostrar tabla con vista previa
with st.expander("📄 Ver datos tabulares"):
    st.dataframe(df_lluvia[["fecha", "rainfall", "corrida"]])

#10)st.dataframe(df_lluvia[["fecha", "rainfall", "corrida"]])st.markdown("---")
st.caption("📍 Proyecto desarrollado en Streamlit · Datos de precipitaciones graficados para demostración")

#Enviar datos a Cruzado
def cargar_datos_prec():
    return df_lluvia
