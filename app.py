import streamlit as st
import pandas as pd
import plotly.express as px
from funciones import cargar_datos, modelo_regresion, modelo_clasificacion, convertir_rango_ingreso
from fpdf import FPDF
import os
import tempfile

# --- Configuración de página ---
st.set_page_config(page_title="Empleo y Desempleo en el Estado de México", layout="wide")

# --- CSS para diseño con líneas doradas y botones dinámicos ---
st.markdown("""
    <style>
    body { background-color: #ffffff; }
    .main { font-family: Arial, sans-serif; color: #333333; }

    .title-box {
        background: #800020;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
        border: 5px solid #FFD700;
    }
    .title-box h1 {
        color: white;
        font-size: 3em;
        margin: 0;
    }
    hr {
        border: none;
        border-top: 3px solid #FFD700;
        margin: 20px 0;
    }
    .intro-text {
        font-size: 1.3em;
        margin-bottom: 20px;
        text-align: justify;
    }
    .nav-button {
        display: inline-block;
        background-color: #800020;
        color: #fff;
        border: 2px solid #FFD700;
        border-radius: 50px;
        padding: 10px 25px;
        margin: 5px;
        text-decoration: none;
        font-size: 1em;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        background-color: #990033;
        transform: scale(1.05);
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Título ---
st.markdown("""
    <div class='title-box'>
        <h1>🇲🇽 EMPLEO Y DESEMPLEO EN EL ESTADO DE MÉXICO</h1>
    </div>
""", unsafe_allow_html=True)

# --- Botones de navegación ---
nav_items = ["Inicio", "2020", "2021", "2022", "2023", "2024", "Realizar Predicción", "Descargas"]
nav_query = st.query_params.get("page")

if nav_query in nav_items:
    seccion = nav_query
else:
    seccion = "Inicio"

nav_html = "".join(
    [f"<a class='nav-button' href='?page={item}'>{item}</a>" for item in nav_items]
)
st.markdown(f"<div style='text-align: center;'>{nav_html}</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- Cargar datos ---
df = cargar_datos("data/empleodesempleo.csv")

# --- Funciones de introducción ---
def mostrar_intro_general():
    st.markdown("""
    <div class="intro-text" style="text-align: justify;">
    El Estado de México es uno de los motores económicos más relevantes del país, siendo el área con mayor población y actividad industrial cercana a la Ciudad de México. Su dinámica laboral refleja tendencias complejas y variadas que impactan directamente en la calidad de vida de sus habitantes.
    <br><br>
    Características destacadas del mercado laboral en el Estado de México incluyen una fuerte predominancia del empleo informal, especialmente en zonas urbanas y rurales marginadas, donde muchas personas se emplean en actividades sin contratos ni prestaciones sociales. Sin embargo, la formalidad laboral ha mostrado una recuperación paulatina tras la crisis sanitaria provocada por la pandemia del COVID-19.
    <br><br>
    Los sectores con mayor generación de empleo son el comercio, servicios y manufactura, que concentran la mayor parte de las oportunidades laborales. A pesar de ello, la tasa de desempleo ha tenido altibajos debido a factores externos como cambios en la economía nacional, políticas públicas y fluctuaciones en la demanda de mano de obra.
    <br><br>
    En términos demográficos, los hombres continúan siendo quienes presentan mayor participación laboral, aunque la incorporación femenina ha ido en aumento en los últimos años, diversificando los roles en el mercado de trabajo. La edad promedio de los trabajadores activos oscila entre los 25 y 45 años, siendo este grupo el más productivo y con mayor estabilidad.
    <br><br>
    El Estado de México también presenta diferencias regionales importantes: municipios como Ecatepec, Naucalpan y Tlalnepantla concentran el mayor número de empleos formales debido a su desarrollo industrial y comercial, mientras que otras áreas rurales enfrentan mayores retos para la generación de oportunidades.
    <br><br>
    En este contexto, la presente plataforma interactiva ofrece un análisis detallado de la evolución del empleo y desempleo entre 2020 y 2024, permitiendo observar cómo han cambiado los niveles de ingresos, la distribución por sexo, la formalidad del empleo y las horas trabajadas. A través de gráficas y datos actualizados, se busca facilitar la comprensión y la toma de decisiones para actores sociales, económicos y gubernamentales.
    <br><br>
    Te invitamos a explorar cada sección para profundizar en los indicadores laborales por año, realizar predicciones basadas en modelos estadísticos y descargar reportes que faciliten el estudio de esta importante temática en el Estado de México.
    </div>
    """, unsafe_allow_html=True)

def mostrar_intro_anual(año):
    st.markdown(f"""
    <div class="intro-text" style="text-align: justify;">
    Durante el año {año}, se observaron tendencias particulares en el mercado laboral del Estado de México, afectando variables como ingresos promedio, distribución por sexo y la prevalencia del empleo formal e informal.
    Las gráficas presentadas permiten visualizar de forma clara la situación de ese año específico.
    </div>
    """, unsafe_allow_html=True)

# --- Sección INICIO ---
if seccion == "Inicio":
    st.header("Introducción General")
    mostrar_intro_general()

    img_path = "empleo.jpg"
    if os.path.exists(img_path):
        st.image(img_path, caption="Empleo en el Estado de México", use_container_width=True)
    else:
        st.warning(f"No se encontró la imagen '{img_path}'. Colócala junto a app.py.")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("Base de datos de empleo y desempleo (2020 - 2024)")
    st.write("Esta base de datos muestra información clave para analizar las tendencias del empleo y desempleo en el Estado de México.")
    st.dataframe(df, use_container_width=True)

# --- Apartados por año ---
elif seccion in ["2020", "2021", "2022", "2023", "2024"]:
    año = int(seccion)
    st.header(f"Empleo y Desempleo en {año}")
    mostrar_intro_anual(año)

    df_año = df[df['Año'] == año].copy()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f"Tabla de datos para {año}")
    st.dataframe(df_año, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    fig1 = px.histogram(df_año, x='Sexo', color='Sexo',
                        color_discrete_sequence=['#800020', '#FFD700'],
                        title=f"Distribución por Sexo en {año}")
    st.plotly_chart(fig1, use_container_width=True)

    df_año['Nivel_Ingresos'] = df_año['Nivel_Ingresos'].apply(convertir_rango_ingreso)
    df_año_ingresos = df_año.dropna(subset=['Nivel_Ingresos'])

    fig2 = px.box(df_año_ingresos, x='Sexo', y='Nivel_Ingresos',
                  color='Sexo',
                  color_discrete_sequence=['#800020', '#FFD700'],
                  title=f"Distribución de Ingresos por Sexo en {año}",
                  points="all")
    st.plotly_chart(fig2, use_container_width=True)

    if 'Horas_Trabajo' in df_año.columns:
        horas_sexo = df_año.groupby('Sexo')['Horas_Trabajo'].mean().reset_index()
        fig3 = px.bar(horas_sexo, x='Sexo', y='Horas_Trabajo',
                      color='Sexo',
                      color_discrete_sequence=['#800020', '#FFD700'],
                      title=f"Promedio de Horas Trabajadas por Sexo en {año}")
        st.plotly_chart(fig3, use_container_width=True)

    if 'Tipo_Empleo' in df_año.columns:
        empleo_counts = df_año['Tipo_Empleo'].value_counts().reset_index()
        empleo_counts.columns = ['Tipo_Empleo', 'Count']
        fig4 = px.pie(empleo_counts, names='Tipo_Empleo', values='Count',
                      title=f"Proporción de Empleos Formales e Informales en {año}",
                      color_discrete_sequence=['#800020', '#FFD700'])
        st.plotly_chart(fig4, use_container_width=True)

    if 'Posicion_Ocupacion' in df_año.columns and 'Total_Poblacion' in df_año.columns:
        ocupacion_sum = df_año.groupby('Posicion_Ocupacion')['Total_Poblacion'].sum().reset_index()
        fig5 = px.pie(ocupacion_sum, names='Posicion_Ocupacion', values='Total_Poblacion',
                      title=f"Posición/Ocupación vs Población Total en {año}",
                      color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig5, use_container_width=True)

# --- Predicción ---
elif seccion == "Realizar Predicción":
    st.header("Realizar Predicción")
    edad_input = st.slider("Edad", min_value=18, max_value=100, value=30)
    sexo_input = st.selectbox("Sexo", options=df['Sexo'].unique())

    if st.button("Predecir Ingreso (Regresión)"):
        pred_r = modelo_regresion(df, edad_input, sexo_input)
        st.success(f"Ingreso estimado: ${pred_r:,.2f}")

    if st.button("Predecir Categoría (Clasificación)"):
        pred_c = modelo_clasificacion(df, edad_input, sexo_input)
        st.info(f"Categoría estimada: {pred_c}")

# --- Descargas ---
elif seccion == "Descargas":
    st.header("Descargar Datos y Reportes")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar Base de Datos CSV", csv, "empleodesempleo.csv", "text/csv")

    if st.button("Generar Reporte PDF con Gráficas por Año"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        for año in range(2020, 2025):
            df_año = df[df['Año'] == año].copy()
            df_año['Nivel_Ingresos'] = df_año['Nivel_Ingresos'].apply(convertir_rango_ingreso)
            df_año_ingresos = df_año.dropna(subset=['Nivel_Ingresos'])

            fig1 = px.histogram(df_año, x='Sexo', color='Sexo',
                                color_discrete_sequence=['#800020', '#FFD700'],
                                title=f"Distribución por Sexo en {año}")

            fig2 = px.box(df_año_ingresos, x='Sexo', y='Nivel_Ingresos',
                          color='Sexo',
                          color_discrete_sequence=['#800020', '#FFD700'],
                          title=f"Distribución de Ingresos por Sexo en {año}",
                          points="all")

            img1 = fig1.to_image(format="png", width=600, height=400)
            img2 = fig2.to_image(format="png", width=600, height=400)

            # Guardar imágenes en archivos temporales para fpdf
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile1:
                tmpfile1.write(img1)
                tmpfile1_path = tmpfile1.name

            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f"Distribución por Sexo - {año}", ln=True, align="C")
            pdf.image(tmpfile1_path, x=15, y=30, w=180)
            os.remove(tmpfile1_path)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile2:
                tmpfile2.write(img2)
                tmpfile2_path = tmpfile2.name

            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f"Distribución de Ingresos por Sexo - {año}", ln=True, align="C")
            pdf.image(tmpfile2_path, x=15, y=30, w=180)
            os.remove(tmpfile2_path)

        pdf_bytes = pdf.output(dest='S').encode('latin1')

        st.download_button(
            label="Descargar PDF con Gráficas",
            data=pdf_bytes,
            file_name="reporte_empleo_estado_mexico.pdf",
            mime="application/pdf"
        )
