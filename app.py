import streamlit as st
import pandas as pd
from utils.extractor import run_extraction
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')



# Configurar página
st.set_page_config(
    page_title="VALD Data Extraction App",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("🌟 VALD Data Extraction App")
    st.write("Esta aplicación permite extraer datos de la API de VALD Performance y guardarlos en archivos CSV.")
    
    # Información de la aplicación
    with st.expander("ℹ️ Información de la aplicación", expanded=False):
        st.markdown("""
        Esta aplicación extrae datos de la API de VALD Performance incluyendo:
        - Tenants
        - Categorías
        - Grupos
        - Perfiles de usuarios
        - Datos de pruebas NordBord
        - Datos de pruebas ForceFrame
        
        Los datos se guardan en archivos CSV en la carpeta `output_data`.
        """)
    
    # Sección de extracción
    st.header("📥 Extracción de Datos")
    
    # Botón para iniciar extracción
    if st.button("🚀 Iniciar Proceso de Extracción", type="primary"):
        # Crear contenedor para logs
        log_container = st.empty()
        
        # Redirigir salida estándar a Streamlit
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output
        
        # Mostrar spinner durante la extracción
        with st.spinner("Ejecutando el proceso de extracción..."):
            try:
                # Ejecutar extracción
                run_extraction()
                
                # Restaurar salida estándar
                sys.stdout = old_stdout
                
                # Mostrar logs
                log_container.code(redirected_output.getvalue())
                
                # Mostrar mensaje de éxito
                st.success("✅ Proceso de extracción completado con éxito")
                
                # Mostrar datos extraídos si existen
                show_extracted_data()
                
            except Exception as e:
                # Restaurar salida estándar
                sys.stdout = old_stdout
                
                # Mostrar error
                log_container.code(redirected_output.getvalue())
                st.error(f"❌ Error durante la extracción: {str(e)}")

def show_extracted_data():
    """Muestra los datos extraídos si existen"""
    output_dir = "output_data"
    
    if not os.path.exists(output_dir):
        st.warning("No se encontró la carpeta de datos extraídos.")
        return
    
    # Obtener lista de archivos CSV
    csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
    
    if not csv_files:
        st.info("No se encontraron archivos CSV en la carpeta de datos extraídos.")
        return
    
    st.header("📊 Datos Extraídos")
    
    # Mostrar selector de archivos
    selected_file = st.selectbox("Seleccionar archivo para visualizar:", csv_files)
    
    if selected_file:
        file_path = os.path.join(output_dir, selected_file)
        try:
            df = pd.read_csv(file_path)
            st.write(f"**{selected_file}** - {len(df)} filas:")
            st.dataframe(df)
            
            # Opción para descargar
            st.download_button(
                label="⬇️ Descargar archivo CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=selected_file,
                mime='text/csv',
            )
            
        except Exception as e:
            st.error(f"Error al cargar el archivo {selected_file}: {str(e)}")

if __name__ == "__main__":
    main()
