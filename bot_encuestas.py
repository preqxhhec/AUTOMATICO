import random
import asyncio
from playwright.async_api import async_playwright

URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/viewform"

async def main():
    print("Iniciando navegador con Playwright...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Forzar idioma español para que el botón diga "Enviar"
        context = await browser.new_context(locale="es-ES")
        page = await context.new_page()
        
        print("Navegando al formulario...")
        await page.goto(URL_FORMULARIO, wait_until="networkidle")
        
        # Esperar a que aparezca la primera pregunta
        await page.wait_for_selector("div[role='listitem']", timeout=15000)
        await page.wait_for_timeout(2000)
        
        print("Llenando opciones únicas...")
        bloques = await page.locator("div[role='listitem']").all()
        
        for bloque in bloques:
            radios = await bloque.locator("div[role='radio']").all()
            if radios:
                validos = []
                for r in radios:
                    val = await r.get_attribute("data-value")
                    if val != "__other_option__":
                        validos.append(r)
                if validos:
                    await random.choice(validos).click()
                    await page.wait_for_timeout(300)

        print("Llenando casillas (medios)...")
        for bloque in bloques:
            checks = await bloque.locator("div[role='checkbox']").all()
            if checks:
                validos = []
                for c in checks:
                    val = await c.get_attribute("data-value")
                    if val != "__other_option__":
                        validos.append(c)
                if validos:
                    cantidad = random.randint(1, min(2, len(validos)))
                    seleccionados = random.sample(validos, cantidad)
                    for c in seleccionados:
                        await c.click()
                        await page.wait_for_timeout(300)
                break

        print("Llenando texto...")
        textareas = await page.locator("textarea").all()
        if textareas:
            respuestas = ["Fomentar charlas.", "Mayor transparencia.", "Capacitaciones.", "Nada.", "Difundir por intranet."]
            await textareas[0].fill(random.choice(respuestas))

        print("Haciendo clic en Enviar...")
        # Buscamos el botón por su atributo de accesibilidad (funciona en cualquier idioma)
        try:
            # Intentar buscar por texto "Enviar" o "Submit"
            await page.locator("div[role='button']").filter(has_text="Enviar").or_(page.locator("div[role='button']").filter(has_text="Submit")).first.click(timeout=5000)
        except:
            # Si falla, buscar el último botón de la página (que siempre es el de enviar)
            todos_los_botones = await page.locator("div[role='button']").all()
            if todos_los_botones:
                await todos_los_botones[-1].click()
        
        # Esperar a que la página de confirmación cargue
        await page.wait_for_timeout(4000)
        
        # Verificar si hubo errores
        errores = await page.locator("text='obligatoria'").count() + await page.locator("text='required'").count()
        
        if errores > 0:
            print(f"❌ Falló: Aún faltan preguntas obligatorias.")
        else:
            print("✅ ¡Proceso terminado exitosamente! (Respuesta enviada)")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
