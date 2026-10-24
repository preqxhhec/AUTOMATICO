import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/viewform"

def enviar_una_respuesta():
    print("Iniciando navegador...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--window-size=1280,1024")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(URL_FORMULARIO)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        time.sleep(3)

        # 1. Llenar TODAS las preguntas de opción única
        print("Llenando opciones únicas...")
        # Buscamos todos los contenedores de preguntas reales (role='listitem')
        bloques = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
        
        for bloque in bloques:
            # Buscar si este bloque tiene botones de opción (radios)
            radios = bloque.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            if radios:
                # Elegir uno al azar (ignorando "Otro" si existe)
                validos = [r for r in radios if r.get_attribute("data-value") != "__other_option__"]
                if validos:
                    random.choice(validos).click()
                    time.sleep(0.3) # Pequeña pausa entre preguntas

        # 2. Llenar las casillas de verificación (Medios)
        print("Llenando casillas...")
        for bloque in bloques:
            checks = bloque.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
            if checks:
                cantidad = random.randint(1, 2)
                validos = [c for c in checks if c.get_attribute("data-value") != "__other_option__"]
                if validos:
                    seleccionados = random.sample(validos, min(cantidad, len(validos)))
                    for c in seleccionados:
                        c.click()
                break # Solo hay una pregunta de este tipo

        # 3. Llenar el texto
        print("Llenando texto...")
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        if textareas:
            respuestas = ["Fomentar charlas.", "Mayor transparencia.", "Capacitaciones.", "Nada.", "Difundir por intranet."]
            textareas[0].send_keys(random.choice(respuestas))

        # 4. Hacer clic en Enviar
        print("Haciendo clic en Enviar...")
        boton_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][.//span[contains(text(), 'Enviar') or contains(text(), 'Submit')]]")))
        boton_enviar.click()
        
        time.sleep(4) # Esperar a que procese
        
        # Verificar si hubo errores de Google (por si acaso)
        errores = driver.find_elements(By.XPATH, "//*[contains(text(), 'obligatoria') or contains(text(), 'required')]")
        if len(errores) > 0:
            print(f"❌ Google sigue diciendo que faltan preguntas: {len(errores)} errores.")
        else:
            print("✅ ¡Proceso terminado exitosamente! (Sin errores)")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    enviar_una_respuesta()
