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
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://cw-simulador1.vercel.app/")
        # Esperamos a que la tabla cargue
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # Extraemos el HTML de la tabla directamente
        table_element = driver.find_element(By.TAG_NAME, "table")
        return table_element.get_attribute('outerHTML')
    except Exception as e:
        return f"<table><tr><td>Error: {str(e)}</td></tr></table>"
    finally:
        driver.quit()

@app.route('/')
def home():
    table_html = get_data()
    # Enviamos solo la tabla dentro de una estructura HTML básica
    return render_template_string(f"""
        <html>
            <head><meta charset="UTF-8"></head>
            <body>
                {table_html}
            </body>
        </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
