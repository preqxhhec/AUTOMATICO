import random
import asyncio
from playwright.async_api import async_playwright

URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/viewform"

async def main():
    print("Iniciando navegador con Playwright...")
    
    async with async_playwright() as p:
        # Lanzamos Chromium (el motor de Chrome) en modo invisible
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navegando al formulario...")
        await page.goto(URL_FORMULARIO)
        
        # Playwright espera automáticamente a que la página cargue
        await page.wait_for_selector("div[role='listitem']", timeout=15000)
        
        print("Llenando opciones únicas...")
        # Buscar todos los bloques de preguntas
        bloques = await page.locator("div[role='listitem']").all()
        
        for bloque in bloques:
            # Si el bloque tiene botones de opción (radio)
            radios = await bloque.locator("div[role='radio']").all()
            if radios:
                # Filtramos el "Otro" para que no falle
                validos = []
                for r in radios:
                    val = await r.get_attribute("data-value")
                    if val != "__other_option__":
                        validos.append(r)
                if validos:
                    # Hacer clic en uno al azar
                    await random.choice(validos).click()
                    await page.wait_for_timeout(200) # Pausa para que Google lo registre

        print("Llenando casillas (medios)...")
        # Buscar casillas de verificación
        for bloque in bloques:
            checks = await bloque.locator("div[role='checkbox']").all()
            if checks:
                validos = []
                for c in checks:
                    val = await c.get_attribute("data-value")
                    if val != "__other_option__":
                        validos.append(c)
                if validos:
                    # Elegir 1 o 2
                    cantidad = random.randint(1, min(2, len(validos)))
                    seleccionados = random.sample(validos, cantidad)
                    for c in seleccionados:
                        await c.click()
                break # Solo hay una pregunta de este tipo

        print("Llenando texto...")
        textareas = await page.locator("textarea").all()
        if textareas:
            respuestas = ["Fomentar charlas.", "Mayor transparencia.", "Capacitaciones.", "Nada.", "Difundir por intranet."]
            await textareas[0].fill(random.choice(respuestas))

        print("Haciendo clic en Enviar...")
        # Buscar el botón de enviar
        boton = page.locator("div[role='button']").filter(has_text="Enviar")
        await boton.click()
        
        # Esperar a que la página de confirmación cargue
        await page.wait_for_timeout(3000)
        
        # Verificar si hay errores
        errores = await page.locator("text='obligatoria'").count()
        if errores > 0:
            print(f"❌ Falló: Aún faltan preguntas obligatorias.")
        else:
            print("✅ ¡Proceso terminado exitosamente! (Respuesta enviada)")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
