import os
from flask import Flask
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

def get_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # En Docker, Chrome se instala en esta ruta por defecto
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    # Ya no necesitamos webdriver-manager, Selenium 4 detecta el driver solo en Linux
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://cw-simulador1.vercel.app/")
        # Espera de seguridad para que React cargue
        driver.implicitly_wait(15)
        
        tables = pd.read_html(driver.page_source)
        if tables:
            return tables[0]
        return pd.DataFrame({"Error": ["Tabla no encontrada"]})
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})
    finally:
        driver.quit()

@app.route('/')
def home():
    df = get_data()
    return df.to_html(index=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
