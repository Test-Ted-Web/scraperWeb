import os
from flask import Flask
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

app = Flask(__name__)

def get_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Instalación automática del driver compatible
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get("https://cw-simulador1.vercel.app/")
        # Reducimos un poco el tiempo para evitar timeouts de Render (máx 30s)
        driver.implicitly_wait(15) 
        
        tables = pd.read_html(driver.page_source)
        if tables:
            return tables[0]
        return pd.DataFrame({"Error": ["No se encontró la tabla"]})
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
