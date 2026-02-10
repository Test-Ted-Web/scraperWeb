def get_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Modo headless moderno más eficiente
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # --- OPTIMIZACIONES DE MEMORIA CRÍTICAS ---
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false") # No cargar imágenes
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--single-process") # Reduce uso de hilos (especial para Docker)
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Establecemos un límite de carga de página agresivo
        driver.set_page_load_timeout(30)
        driver.get("https://cw-simulador1.vercel.app/")
        
        # Espera dinámica para que la tabla aparezca
        wait = WebDriverWait(driver, 25)
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        return table.get_attribute('outerHTML')
    except Exception as e:
        return f"<table><tr><td>Error de memoria o tiempo: {str(e)}</td></tr></table>"
    finally:
        driver.quit() # Es vital para liberar la RAM
