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
    print("Iniciando navegador en modo invisible...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Navegando al formulario...")
        driver.get(URL_FORMULARIO)
        
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='listitem']")))
        time.sleep(3)

        bloques = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
        print(f"Se encontraron {len(bloques)} bloques.")
        
        # 1. Servicio (Pregunta 1)
        radios_p1 = bloques[0].find_elements(By.CSS_SELECTOR, "div[role='radio']")
        if radios_p1:
            opciones_validas = [r for r in radios_p1 if r.get_attribute("data-value") != "__other_option__"]
            if opciones_validas:
                random.choice(opciones_validas).click()
                print("- Pregunta 1 respondida.")

        # 2. EL ARREGLO: Buscar TODOS los botones de radio en todos los bloques
        # y hacer clic en uno al azar. Esto asegura que no quede ninguna en blanco.
        print("- Buscando preguntas de opción única para asegurar que no queden vacías...")
        for i, bloque in enumerate(bloques[1:-1], start=1): 
            radios = bloque.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            if radios:
                # Si hay opciones de "Otro" (other_option), las filtramos para no complicarla
                validas = [r for r in radios if r.get_attribute("data-value") != "__other_option__"]
                if validas:
                    random.choice(validas).click()
                    time.sleep(0.3)
        
        print("- Preguntas de opción única respondidas.")

        # 3. Medios (Casillas)
        for bloque in bloques:
            checks = bloque.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
            if checks:
                cantidad = random.randint(1, 2)
                checks_validos = [c for c in checks if c.get_attribute("data-value") != "__other_option__"]
                if checks_validos:
                    seleccionados = random.sample(checks_validos, min(cantidad, len(checks_validos)))
                    for c in seleccionados:
                        c.click()
                print("- Pregunta de medios respondida.")
                break

        # 4. Texto
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        if textareas:
            respuestas = ["Fomentar charlas.", "Mayor transparencia.", "Capacitaciones.", "Nada.", "Difundir por intranet."]
            textareas[0].send_keys(random.choice(respuestas))
            print("- Pregunta de texto respondida.")

        # 5. Botón Enviar
        time.sleep(1)
        print("Buscando el botón Enviar...")
        boton_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Enviar']/ancestor::div[@role='button']")))
        boton_enviar.click()
        print("¡Clic en Enviar realizado!")
        
        time.sleep(4)
        print("✅ Proceso terminado exitosamente.")
        
    except Exception as e:
        print(f"❌ Error en el envío: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    enviar_una_respuesta()
