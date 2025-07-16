import streamlit as st
from PIL import Image
import io

# Configurar la página
st.set_page_config(
    page_title="DInSAR · Ciudad Victoria",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌋"
)

# Estilos CSS personalizados mejorados
st.markdown("""
    <style>
        :root {
            --primary: #2E86AB;
            --secondary: #F18F01;
            --accent: #C73E1D;
            --light: #F5F5F5;
            --dark: #333333;
        }
        
        .stApp {
            background-color: #0a0a0a;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary), #1B5299);
            color: white;
            padding: 2rem;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .card {
            background: #1e1e1e;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
            border-left: 4px solid var(--primary);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px rgba(0,0,0,0.1);
        }
        
        .card-title {
            color: var(--primary);
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .card-content {
            color: var(--light);
            font-size: 1.05rem;
            line-height: 1.7;
        }
        
        .team-member {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.8rem;
            border-radius: 8px;
            transition: background 0.2s;
        }
        
        .team-member:hover {
            background: rgba(46, 134, 171, 0.1);
        }
        
        .member-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.2rem;
        }
        
        .member-info {
            flex: 1;
        }
        
        .member-name {
            font-weight: 600;
            margin-bottom: 0.2rem;
        }
        
        .divider {
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(0,0,0,0.1), transparent);
            margin: 1.5rem 0;
        }
        
        .feature-icon {
            font-size: 1.8rem;
            margin-right: 0.8rem;
            color: var(--secondary);
        }
        
        .feature-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .feature-text {
            flex: 1;
        }
        
        .tech-badge {
            display: inline-block;
            background: rgba(46, 134, 171, 0.1);
            color: var(--primary);
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        .map-container {
            height: 300px;
            background: #e9ecef;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 1.5rem 0;
            overflow: hidden;
        }
        
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1.5rem;
            color: white;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header con imagen de fondo
st.markdown("""
    <div class="header">
        <h1>🌍 Monitoreo de Desplazamientos con DInSAR</h1>
        <p>Análisis de movimientos de terreno en Ciudad Victoria, Loja - Ecuador</p>
    </div>
""", unsafe_allow_html=True)

# Sección de columnas con tarjetas
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="card">
            <div class="card-title">Integrantes del Equipo 👷</div>
            <div class="card-content">
                <div class="team-member">
                    <div class="member-avatar">JA</div>
                    <div class="member-info">
                        <div class="member-name">Jonhatan Abad</div>
                    </div>
                </div>
                <div class="team-member">
                    <div class="member-avatar">DA</div>
                    <div class="member-info">
                        <div class="member-name">Danny Alulima</div>
                    </div>
                </div>
                <div class="team-member">
                    <div class="member-avatar">MC</div>
                    <div class="member-info">
                        <div class="member-name">Mario Castillo</div>
                    </div>
                </div>
                <div class="team-member">
                    <div class="member-avatar">GL</div>
                    <div class="member-info">
                        <div class="member-name">Gisel Lucero</div>
                    </div>
                </div>
                <div class="team-member">
                    <div class="member-avatar">NT</div>
                    <div class="member-info">
                        <div class="member-name">Nicolás Torres</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card">
            <div class="card-title">Información Académica 📚</div>
            <div class="card-content">
                <p><strong>Materia:</strong> Lenguaje de Programación</p>
                <p><strong>Universidad:</strong> Universidad Técnica Particular de Loja</p>
                <div class="divider"></div>
                <p><strong>Tecnologías utilizadas:</strong></p>
                <div>
                    <span class="tech-badge">Python</span>
                    <span class="tech-badge">Streamlit</span>
                    <span class="tech-badge">DInSAR</span>
                    <span class="tech-badge">Pandas</span>
                    <span class="tech-badge">Matplotlib</span>
                    <span class="tech-badge">GeoPandas</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Sección principal
st.markdown("""
    <div class="card">
        <div class="card-title">🔍 Descripción del Proyecto</div>
        <div class="card-content">
            <p>Esta plataforma interactiva analiza desplazamientos del terreno en Ciudad Victoria, Loja, utilizando datos obtenidos mediante la técnica DInSAR (Interferometría Diferencial de Radar de Apertura Sintética).</p>
            <p>El sistema integra datos de desplazamiento con información meteorológica para identificar correlaciones entre precipitaciones y movimientos del terreno, proporcionando herramientas avanzadas para:</p>
            <div class="feature-item">
                <span class="feature-icon">📊</span>
                <div class="feature-text">
                    <strong>Visualización Desplazamiento</strong> - Gráficas de desplazamiento acumulado en función del tiempo
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-icon">⚠️</span>
                <div class="feature-text">
                    <strong>Detección de anomalías</strong> - Identificación automática de períodos con mayor tasa de desplazamiento
                </div>
            </div>
                    <div class="feature-item">
                <span class="feature-icon">🌧️</span>
                <div class="feature-text">
                    <strong>Visualización Precipitaciones</strong> - Eventos de precipitación promedio marcados en gráficas
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📈</span>
                <div class="feature-text">
                    <strong>Análisis estadístico</strong> - Tablas resumen con métricas descriptivas para evaluación cuantitativa
                </div>
            </div>
            <div class="divider"></div>
            <p><strong>Aplicaciones:</strong> Este sistema es valioso para estudios de riesgo geológico, planificación urbana, monitoreo ambiental y evaluación de amenazas naturales en la región de Loja.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2025 Proyecto de Monitoreo de Desplazamientos - Ciudad Victoria, Loja, Ecuador</p>
        <p>Universidad Técnica Particular de Loja</p>
    </div>
""", unsafe_allow_html=True)