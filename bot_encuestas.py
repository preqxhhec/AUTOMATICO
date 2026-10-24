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
    options.add_argument("--window-size=1280,1024") # Tamaño de pantalla para la foto
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(URL_FORMULARIO)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        time.sleep(3)

        print("Llenando opciones únicas...")
        todos_los_radios = driver.find_elements(By.XPATH, "//div[@role='radio']")
        opciones_por_pregunta = {}
        for radio in todos_los_radios:
            try:
                pregunta_padre = radio.find_element(By.XPATH, "./ancestor::div[@role='listitem']")
                id_pregunta = pregunta_padre.id
                if id_pregunta not in opciones_por_pregunta:
                    opciones_por_pregunta[id_pregunta] = []
                opciones_por_pregunta[id_pregunta].append(radio)
            except:
                pass

        for id_pregunta, opciones in opciones_por_pregunta.items():
            random.choice(opciones).click()
            time.sleep(0.2)
            
        print("Llenando casillas...")
        todos_los_checks = driver.find_elements(By.XPATH, "//div[@role='checkbox']")
        if todos_los_checks:
            cantidad = random.randint(1, min(2, len(todos_los_checks)))
            seleccionados = random.sample(todos_los_checks, cantidad)
            for check in seleccionados:
                check.click()
                time.sleep(0.2)
                
        print("Llenando texto...")
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        if textareas:
            respuestas = ["Fomentar charlas.", "Mayor transparencia.", "Capacitaciones.", "Nada.", "Difundir por intranet."]
            textareas[0].send_keys(random.choice(respuestas))

        print("Haciendo clic en Enviar...")
        boton_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][.//span[contains(text(), 'Enviar') or contains(text(), 'Submit')]]")))
        boton_enviar.click()
        
        time.sleep(3) # Esperar a que cargue la pantalla final
        
        # --- LA MAGIA: TOMAR LA FOTO ---
        driver.save_screenshot("resultado_final.png")
        print("📸 Se guardó la foto 'resultado_final.png'.")
        
        # Intentar leer si hay algún mensaje de error en rojo
        try:
            errores = driver.find_elements(By.XPATH, "//*[contains(text(), 'obligatoria') or contains(text(), 'obligatorio') or contains(text(), 'required') or contains(text(), 'Obligatorio')]")
            for err in errores:
                if err.is_displayed():
                    print(f"⚠️ Google dice: {err.text}")
        except:
            pass

        print("✅ Proceso terminado.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("error_pantalla.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    enviar_una_respuesta()
