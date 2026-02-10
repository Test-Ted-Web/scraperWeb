import os
from flask import Flask
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def get_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://cw-simulador1.vercel.app/")
        
        # Esperar a que la tabla sea visible (ajustamos el selector)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # Obtenemos el HTML de la tabla específicamente
        tabla_html = driver.find_element(By.TAG_NAME, "table").get_attribute('outerHTML')
        
        # Convertimos a DataFrame
        df_list = pd.read_html(tabla_html)
        if df_list:
            df = df_list[0]
            # Limpieza: Eliminamos columnas o filas completamente vacías
            df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            return df
        
        return pd.DataFrame({"Mensaje": ["No se encontró estructura de tabla"]})
    
    except Exception as e:
        return pd.DataFrame({"Error": [f"Error en el scraping: {str(e)}"]})
    finally:
        driver.quit()

@app.route('/')
def home():
    df = get_data()
    
    # Generamos un HTML muy simple y limpio para Excel
    # 'border=1' ayuda a Excel a identificar las celdas
    html_output = df.to_html(index=False, border=1, justify='center')
    
    # Envolvemos en etiquetas HTML básicas para que sea una página "plana"
    return f"""
    <html>
        <head><title>Datos para Excel</title></head>
        <body>
            {html_output}
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
