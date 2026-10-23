import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL de tu formulario
URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/viewform"

def enviar_una_respuesta():
    print("Iniciando navegador en modo invisible...")
    
    # Configuración para que corra en GitHub (sin interfaz gráfica)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") # Modo invisible
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(URL_FORMULARIO)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='listitem']")))
        time.sleep(2) # Pausa para que cargue todo

        bloques = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
        
        # 1. Servicio (Opción múltiple / texto)
        radios_p1 = bloques[0].find_elements(By.CSS_SELECTOR, "div[role='radio']")
        if radios_p1:
            opciones_validas = [r for r in radios_p1 if r.get_attribute("data-value") != "__other_option__"]
            if opciones_validas:
                random.choice(opciones_validas).click()

        # 2. Preguntas Si/No
        preguntas_si_no = []
        for bloque in bloques[1:-1]: 
            radios = bloque.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            if len(radios) == 2:
                preguntas_si_no.append(radios)
        
        for opciones in preguntas_si_no:
            random.choice(opciones).click()
            time.sleep(0.3)

        # 3. Medios de comunicación (Casillas)
        for bloque in bloques:
            checks = bloque.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
            if checks:
                cantidad = random.randint(1, 2)
                checks_validos = [c for c in checks if c.get_attribute("data-value") != "__other_option__"]
                if checks_validos:
                    seleccionados = random.sample(checks_validos, min(cantidad, len(checks_validos)))
                    for c in seleccionados:
                        c.click()
                break

        # 4. Pregunta de Texto (La última)
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        if textareas:
            respuestas = ["Fomentar charlas.", "Mayor transparencia.", "Capacitaciones.", "Nada.", "Difundir por intranet."]
            textareas[0].send_keys(random.choice(respuestas))

        # 5. Botón Enviar
        time.sleep(1)
        boton_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Enviar']/ancestor::div[@role='button']")))
        boton_enviar.click()
        time.sleep(2)
        
        print("✅ ¡Respuesta enviada con éxito!")
        return True
        
    except Exception as e:
        print(f"❌ Error en el envío: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    # Envía 1 sola respuesta cada vez que se presiona el botón
    enviar_una_respuesta()
