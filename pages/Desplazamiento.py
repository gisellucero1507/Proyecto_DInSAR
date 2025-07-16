import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Desplazamiento",
    layout="wide"
)

st.title("Visualización de Desplazamiento por Sensor 📊")

# 1) Carga de datos 
disp_paths = [
    './data/data_estructurada_corrida1.csv',
    './data/data_estructurada_corrida2.csv',
    './data/data_estructurada_corrida3.csv'
]

# 2) Carga, fusión y transformación de los datos
parts = []
for path in disp_paths:
    df_temp = pd.read_csv(path, delimiter=';')
    df_temp.columns = df_temp.columns.str.lower()

    # Asegurar que todos los nombres de columna sean strings limpios
    df_temp.columns = [str(col).lower().strip() for col in df_temp.columns]

    # Eliminar columnas vacías
    df_temp = df_temp.loc[:, ~df_temp.columns.str.contains('^unnamed')]
    df_temp = df_temp.dropna(axis=1, how='all')

    # Procesar fecha
    df_temp['fecha'] = pd.to_datetime(df_temp['fecha'], dayfirst=True, errors='coerce')

    # Mostrar filas con fecha inválida justo después de procesar este archivo
    invalid_fechas = df_temp[df_temp['fecha'].isna()]
    if not invalid_fechas.empty:
        st.warning(f"Hay {len(invalid_fechas)} filas con fechas inválidas o no convertibles en {path}:")
        st.dataframe(invalid_fechas)

    # Eliminar filas sin fecha válida
    df_temp = df_temp[df_temp['fecha'].notna()]

    # Detectar columnas de sensores
    sensor_cols = [c for c in df_temp.columns if c not in ('punto', 'fecha', 'corrida')]

    # Melt para pasar a formato largo
    df_long = df_temp.melt(
        id_vars=['fecha', 'corrida', 'punto'],
        value_vars=sensor_cols,
        var_name='sensor',
        value_name='Desplazamiento'
    )

    # Reemplazar coma decimal por punto antes de convertir a número
    df_long['Desplazamiento'] = (
        df_long['Desplazamiento']
        .astype(str)
        .str.replace(',', '.', regex=False)
    )

    df_long['Desplazamiento'] = pd.to_numeric(df_long['Desplazamiento'], errors='coerce')

    parts.append(df_long)

# Concatenar todos los datos
if not parts:
    st.error("No se cargaron datos válidos.")
    st.stop()

df_disp = pd.concat(parts, ignore_index=True)
df_disp['punto'] = df_disp['punto'].astype(str).str.strip()
df_disp['sensor'] = df_disp['sensor'].astype(str)

# Eliminar sensores sin ningún valor válido 
valid_sensores = df_disp.groupby('sensor')['Desplazamiento'].apply(lambda x: x.notna().any())
df_disp = df_disp[df_disp['sensor'].isin(valid_sensores[valid_sensores].index)]

#3)Sidebar de filtros
with st.sidebar:
    st.header("Filtros")

    corridas = sorted(df_disp['corrida'].unique())
    corrida_sel = st.selectbox("Selecciona la corrida", corridas)

    df_corrida = df_disp[df_disp['corrida'] == corrida_sel]

    sensores = sorted(df_corrida['sensor'].unique())
    sensores_sel = st.multiselect("Selecciona sensores", sensores, default=sensores)

# Filtro principal 
df_filtrado = df_disp[
    (df_disp['corrida'] == corrida_sel) &
    (df_disp['sensor'].isin(sensores_sel)) &
    (df_disp['Desplazamiento'].notna())
]

#4) Visualización 
if df_filtrado.empty:
    st.warning("No hay datos válidos para graficar.")
else:
    fig = px.scatter(
        df_filtrado,
        x='fecha',
        y='Desplazamiento',
        color='sensor',
        labels={
            'fecha': 'Fecha',
            'Desplazamiento': 'Desplazamiento (mm)',
            'sensor': 'Sensor'
        },
        title=f"Desplazamiento - Corrida {corrida_sel}"
    )
    
    # Calcular promedio por fecha
    promedio_por_fecha = df_filtrado.groupby('fecha')['Desplazamiento'].mean().reset_index()

    # Añadir línea de promedio  
    fig.add_trace(
        go.Scatter(
            x=promedio_por_fecha['fecha'],
            y=promedio_por_fecha['Desplazamiento'],
            mode='lines',
            name='Promedio',
            line=dict(color='#56ff68', width=3)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calcular la fecha con mayor desplazamiento promedio
    max_fecha = promedio_por_fecha.loc[promedio_por_fecha['Desplazamiento'].idxmax()]
    max_fecha_str = max_fecha['fecha'].strftime('%Y-%m-%d')
    max_valor = round(max_fecha['Desplazamiento'], 4)

    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        color: #000;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 1.5rem;
        font-family: "Segoe UI", sans-serif;
    '>
        <div style='font-size:1.4rem; font-weight:600; margin-bottom:0.5rem;'>
            Fecha con mayor desplazamiento promedio
        </div>
        <div style='font-size:1.1rem;'>
            <strong style='color:#3b0a75'>{max_fecha_str}</strong> 
            registró un promedio de 
            <strong style='color:#3b0a75'>{max_valor:.3f} mm</strong> de desplazamiento.
        </div>
    </div>
    <hr/>
""", unsafe_allow_html=True)

    
    # Detectar eventos con mayor cambio de desplazamiento 
df_eventos = df_filtrado.sort_values(by=['sensor', 'fecha']).copy()

#4) Calcular deltas
df_eventos['Desplazamiento_Previo'] = df_eventos.groupby('sensor')['Desplazamiento'].shift(1)
df_eventos['Fecha_Previo'] = df_eventos.groupby('sensor')['fecha'].shift(1)
df_eventos['Delta'] = df_eventos['Desplazamiento'] - df_eventos['Desplazamiento_Previo']
df_eventos['Dias'] = (df_eventos['fecha'] - df_eventos['Fecha_Previo']).dt.days
df_eventos['Velocidad'] = df_eventos['Delta'] / df_eventos['Dias']

#5) Detectar el mayor cambio por sensor
df_picos = df_eventos.loc[
    df_eventos.groupby('sensor')['Delta'].apply(lambda x: x.abs().idxmax())
]

df_picos = df_picos[['sensor', 'Fecha_Previo', 'fecha', 'Delta', 'Velocidad']]
df_picos = df_picos.sort_values(by='Velocidad', ascending=False).reset_index(drop=True)

st.subheader("Eventos con Mayor Cambio de Desplazamiento 📋")
st.dataframe(df_picos.head(10))

st.markdown(f"""
    <hr/>
    """, unsafe_allow_html=True)

# Tabla de datos 
with st.expander("📄 Ver datos tabulares"):
    st.dataframe(df_filtrado)
    
# Pie de página
st.markdown("---")
st.caption("📍 Proyecto desarrollado en Streamlit · Datos de desplazamientos graficados para demostración")

#Enviar datos a Cruzado
def cargar_datos_desp():
    return df_disp