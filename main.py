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
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Punto clave para Render: localizar el binario de Chrome
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://cw-simulador1.vercel.app/")
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        tables = pd.read_html(driver.page_source)
        if tables:
            return tables[0]
        return pd.DataFrame({"Error": ["No se encontró la tabla"]})
    finally:
        driver.quit()

@app.route('/')
def home():
    df = get_data()
    # Convertimos el DataFrame a HTML plano
    return df.to_html(index=False)

if __name__ == "__main__":
    # Render asigna un puerto dinámico mediante la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
