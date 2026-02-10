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
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # Estas opciones ayudan a consumir menos RAM
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Reducimos el tiempo de carga de página a 20 segundos
        driver.set_page_load_timeout(20)
        driver.get("https://cw-simulador1.vercel.app/")
        
        # Espera máxima de 10 segundos para que aparezca la tabla
        wait = WebDriverWait(driver, 10)
        
        # Intentamos localizar la tabla. Si falla, tomamos lo que haya.
        try:
            element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            tabla_html = element.get_attribute('outerHTML')
        except:
            # Si no encuentra <table>, intenta leer todo el body como último recurso
            tabla_html = driver.page_source
        
        df_list = pd.read_html(tabla_html)
        
        if df_list:
            df = df_list[0]
            return df.dropna(how='all', axis=0)
        
        return pd.DataFrame({"Estado": ["Esperando datos... recarga en unos segundos"]})
    
    except Exception as e:
        return pd.DataFrame({"Error": [f"Reintenta en un momento: {str(e)}"]})
    finally:
        driver.quit()

@app.route('/')
def home():
    df = get_data()
    # Generamos HTML puro sin CSS pesado
    return df.to_html(index=False, border=1)

if __name__ == "__main__":
    # Render usa el puerto 10000 por defecto en muchos casos, os.environ lo detecta
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
