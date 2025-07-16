# 🌍 Proyecto DInSAR - Análisis de Desplazamientos en Ciudad Victoria

Este proyecto corresponde al desarrollo de una **aplicación interactiva** que analiza desplazamientos del terreno en **Ciudad Victoria (Loja, Ecuador)** mediante la técnica **DInSAR** y registros de **precipitación promedio**, utilizando herramientas de visualización y procesamiento de datos en **Python con Streamlit**.

## 👥 Autores

- Jonathan Paul Abad Castillo  
- Mario David Castillo Castillo  
- Gisel Madelen Lucero Sánchez  
- Josué Nicolás Torres Tinoco  
- Danny Alejandro Alulima Bao  

Facultad de Ingeniería y Arquitectura – Carrera de Geología  
Universidad Técnica Particular de Loja

---

## 🎯 Objetivo

Desarrollar una aplicación web que permita visualizar los **desplazamientos del terreno a lo largo del tiempo** e integrarlos con datos de **precipitación**, para comprender mejor los **posibles riesgos naturales** en la zona, como deslizamientos o hundimientos, desde una perspectiva académica y técnica.

---

## 🧠 Tecnologías y Librerías Utilizadas

- [Streamlit](https://streamlit.io/) – Interfaz web interactiva
- [Pandas](https://pandas.pydata.org/) – Procesamiento de datos
- [Plotly Express / Graph Objects](https://plotly.com/python/) – Visualización interactiva

---

## 🗂️ Estructura de Datos

### 📁 Carpeta `data/`
- Archivos CSV con los **desplazamientos del terreno**, divididos por corridas.
- Archivo CSV con los **registros de precipitación**: fecha, valor de lluvia, y corrida correspondiente.

### 📊 Procesamiento de Datos
- **Desplazamientos**: unificación, limpieza, transformación, y filtrado por sensores válidos.
- **Precipitaciones**: corrección de formato, conversión de tipos de datos, limpieza.

---

## 📈 Funcionalidades de la Aplicación

### 1. Página de **Desplazamientos**
- Gráficos por sensor y promedio diario.
- Identificación del día con **mayor desplazamiento promedio**.
- **Tabla de eventos críticos**: sensores con mayores cambios de desplazamiento.

### 2. Página de **Precipitaciones**
- Línea temporal por corrida.
- Visualización individual por corrida.
- **Histograma de precipitaciones mensuales** agrupadas por año.

### 3. Página de **Datos Cruzados**
- Visualización conjunta de desplazamientos y precipitaciones.
- Filtros por corrida y sensores.
- Análisis visual de posibles correlaciones.

### 4. Página de **Inicio**
- Presentación general del proyecto, institución, integrantes y enlaces relevantes.

---

## 🌐 Enlaces Importantes

- 🔗 Repositorio GitHub: [https://github.com/gisellucero1507/Proyecto_DInSAR](https://github.com/gisellucero1507/Proyecto_DInSAR)
- 🚀 Aplicación Web: [https://dinsar-proyecto.streamlit.app/](https://dinsar-proyecto.streamlit.app/)

---

## 📊 Ejemplos de Resultados

- Eventos de desplazamiento significativos en **2016, 2017 y 2018**.
- Eventos de lluvia intensa correlacionados con cambios en la estabilidad del terreno (**2019 y 2021**).
- Análisis por sensor para identificar zonas más vulnerables.

---

## 🔍 Conclusiones y Futuro

La aplicación representa una herramienta útil para el **análisis visual y exploratorio** de datos espaciales y climáticos. En el futuro, podría ampliarse con:

- Sistemas de **alerta temprana** basados en umbrales críticos.
- Incorporación de datos geotécnicos y topográficos.
- Modelos predictivos de riesgo por IA o machine learning.

---

## 🏁 Cómo Ejecutar el Proyecto Localmente

1. Clona el repositorio:
   ```bash
   git clone https://github.com/gisellucero1507/Proyecto_DInSAR.git
   cd Proyecto_DInSAR
