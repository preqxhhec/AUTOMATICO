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
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(URL_FORMULARIO)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        time.sleep(3) # Dar tiempo a que cargue todo

        print("Buscando botones de opción (radios)...")
        # Buscar TODOS los botones de opción en toda la página
        todos_los_radios = driver.find_elements(By.XPATH, "//div[@role='radio']")
        
        # Agruparlos por si hay varios en la misma pregunta (evitar hacer doble clic en la misma)
        opciones_por_pregunta = {}
        for radio in todos_los_radios:
            try:
                # Obtenemos el ID del grupo o usamos el nombre de la pregunta
                pregunta_padre = radio.find_element(By.XPATH, "./ancestor::div[@role='listitem']")
                id_pregunta = pregunta_padre.id
                
                if id_pregunta not in opciones_por_pregunta:
                    opciones_por_pregunta[id_pregunta] = []
                opciones_por_pregunta[id_pregunta].append(radio)
            except:
                pass

        print(f"Se encontraron {len(opciones_por_pregunta)} preguntas de opción única.")
        
        # Hacer clic en una opción al azar por cada pregunta
        for id_pregunta, opciones in opciones_por_pregunta.items():
            random.choice(opciones).click()
            time.sleep(0.3)
            
        print("Buscando casillas de verificación (medios)...")
        # Buscar TODAS las casillas de verificación
        todos_los_checks = driver.find_elements(By.XPATH, "//div[@role='checkbox']")
        if todos_los_checks:
            # Elegir 1 o 2 al azar
            cantidad = random.randint(1, min(2, len(todos_los_checks)))
            seleccionados = random.sample(todos_los_checks, cantidad)
            for check in seleccionados:
                check.click()
                time.sleep(0.2)
                
        print("Buscando campo de texto...")
        # Buscar campo de texto
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        if textareas:
            respuestas = ["Fomentar charlas.", "Mayor transparencia.", "Capacitaciones.", "Nada.", "Difundir por intranet."]
            textareas[0].send_keys(random.choice(respuestas))

        print("Buscando botón Enviar...")
        # Buscar el botón de enviar de varias formas posibles
        boton_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][.//span[contains(text(), 'Enviar') or contains(text(), 'Submit')]]")))
        
        print("Haciendo clic en Enviar...")
        boton_enviar.click()
        
        time.sleep(3) # Esperar a que procese
        print("✅ ¡Proceso terminado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error exacto: {e}")
        # Intento desesperado: buscar si hay un mensaje de error visible en pantalla
        try:
            errores = driver.find_elements(By.XPATH, "//*[contains(text(), 'obligatoria') or contains(text(), 'obligatorio') or contains(text(), 'required')]")
            for err in errores:
                if err.is_displayed():
                    print(f"⚠️ Google dice: {err.text}")
        except:
            pass
    finally:
        driver.quit()

if __name__ == "__main__":
    enviar_una_respuesta()
