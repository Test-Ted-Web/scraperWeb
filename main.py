import os
from flask import Flask, render_template_string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def get_data():
    chrome_options = Options()
    # Usamos el nuevo modo headless que es más eficiente en memoria
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # No cargar imágenes ni extensiones para ahorrar RAM
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Tiempo límite de carga de la web
        driver.set_page_load_timeout(25)
        driver.get("https://cw-simulador1.vercel.app/")
        
        # Esperamos solo a que el primer ID de vehículo aparezca (sabemos que es React)
        # Esto es más rápido que esperar a que toda la página termine de procesar
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # IMPORTANTE: Extraemos solo el texto de la tabla, no todo el HTML pesado
        # Esto consume mucho menos procesamiento para Flask
        tabla_html = driver.find_element(By.TAG_NAME, "table").get_attribute('outerHTML')
        return tabla_html
    except Exception as e:
        return f"<p>Error de carga (RAM agotada o Timeout): {str(e)}</p>"
    finally:
        # Liberación inmediata de memoria
        driver.quit()

@app.route('/')
def home():
    table_content = get_data()
    # Estructura mínima para que Excel reconozca la tabla
    return render_template_string(f"""
        <html>
            <body>
                {table_content}
            </body>
        </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
