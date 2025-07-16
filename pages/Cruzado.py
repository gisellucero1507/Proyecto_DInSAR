import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from pages.Desplazamiento import cargar_datos_desp
from pages.Precipitacion import cargar_datos_prec

#Configuración de página
st.set_page_config(
    page_title="Análisis Combinado",
    layout="wide",
)

#Cargar datos
df_desp = cargar_datos_desp()
df_prec = cargar_datos_prec()

# Asegurar tipos consistentes
df_desp['corrida'] = df_desp['corrida'].astype(int)
df_prec['corrida'] = df_prec['corrida'].astype(int)

#Sidebar de filtros
with st.sidebar:
    st.header("Filtros")
    corridas = sorted(df_desp['corrida'].unique())
    corrida_sel = st.selectbox("Selecciona la corrida", corridas)

    df_corrida = df_desp[df_desp['corrida'] == corrida_sel]
    sensores = sorted(df_corrida['sensor'].unique())
    sensores_sel = st.multiselect("Selecciona sensores", sensores, default=sensores)

#Filtrar datos según selección
df_desp_filtrado = df_desp[
    (df_desp['corrida'] == corrida_sel) &
    (df_desp['sensor'].isin(sensores_sel)) &
    (df_desp['Desplazamiento'].notna())
]

df_prec_filtrado = df_prec[
    (df_prec['corrida'] == corrida_sel) &
    (df_prec['rainfall'].notna())
]

#Crear gráfico combinado
fig_combined = go.Figure()

#Añadir puntos de desplazamiento
if not df_desp_filtrado.empty:
    for sensor in df_desp_filtrado['sensor'].unique():
        df_sensor = df_desp_filtrado[df_desp_filtrado['sensor'] == sensor]
        fig_combined.add_trace(
            go.Scatter(
                x=df_sensor['fecha'],
                y=df_sensor['Desplazamiento'],
                mode='markers',
                name=f'Desplazamiento ({sensor})',
                yaxis='y1',
                marker=dict(size=6)
            )
        )
else:
    st.warning(f"No hay datos de desplazamiento válidos para la Corrida {corrida_sel}.")

#Añadir línea de precipitación
if not df_prec_filtrado.empty:
    lluvia_agr = (
        df_prec_filtrado
        .groupby('fecha', as_index=False)['rainfall']
        .sum()
    )
    fig_combined.add_trace(
        go.Scatter(
            x=lluvia_agr['fecha'],
            y=lluvia_agr['rainfall'],
            mode='lines',
            name=f'Precipitación ({corrida_sel})',
            yaxis='y2',
            line=dict(shape='spline', width=3, color='#3398FF')
        )
    )
else:
    st.warning("No hay datos de precipitación para esa corrida.")

#Layout y ejes
fig_combined.update_layout(
    title_text=f"Corrida {corrida_sel}: Desplazamiento y Precipitación",
    xaxis_title="Fecha",
    yaxis=dict(title="Desplazamiento (mm)", side="left"),
    yaxis2=dict(title="Precipitación (mm)", overlaying="y", side="right"),
    hovermode="x unified",
    legend=dict(orientation='v', x=1.10, y=1),
    template="plotly_dark",
    margin=dict(l=40, r=40, t=80, b=40)
)

#Ajustar eje X solo al rango de datos filtrados
if not df_desp_filtrado.empty or not df_prec_filtrado.empty:
    fechas_desp = df_desp_filtrado['fecha'] if not df_desp_filtrado.empty else None
    fechas_prec = df_prec_filtrado['fecha'] if not df_prec_filtrado.empty else None

    fechas_validas = pd.concat([f for f in [fechas_desp, fechas_prec] if f is not None])
    min_fecha = fechas_validas.min()
    max_fecha = fechas_validas.max()

    fig_combined.update_xaxes(
        range=[min_fecha, max_fecha],
        tickformat="%b %Y",
        dtick="M1",
        tickangle=45
    )

#Mostrar gráfico
st.plotly_chart(fig_combined, use_container_width=True)

#Pie de página
st.markdown("---")
st.caption("📍 Proyecto desarrollado en Streamlit · Datos de desplazamientos y precipitaciones graficados para demostración")
