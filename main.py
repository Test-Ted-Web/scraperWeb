import os
from flask import Flask, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def get_latest_row():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://cw-simulador1.vercel.app/")
        
        # Esperar a que la tabla aparezca
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # SELECTOR ESPECÍFICO: Obtenemos solo la primera fila del cuerpo de la tabla
        # Esto reduce drásticamente el tamaño del objeto en memoria
        first_row = driver.find_element(By.CSS_SELECTOR, "table tbody tr:first-child")
        row_html = first_row.get_attribute('outerHTML')
        
        # También capturamos los encabezados para que Excel sepa qué es cada cosa
        header = driver.find_element(By.TAG_NAME, "thead").get_attribute('outerHTML')
        
        return f"<table>{header}<tbody>{row_html}</tbody></table>"
    
    except Exception as e:
        return f"<p>Error: {str(e)}</p>"
    finally:
        driver.quit()

@app.route('/')
def home():
    data_html = get_latest_row()
    return render_template_string(f"""
        <html>
            <head><meta charset="UTF-8"></head>
            <body>
                <h2>Último Registro Lavacar</h2>
                {data_html}
            </body>
        </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
