import random
import asyncio
from playwright.async_api import async_playwright

URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/viewform"

async def main():
    print("Iniciando navegador con Playwright...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="es-ES")
        page = await context.new_page()
        
        print("Navegando al formulario...")
        await page.goto(URL_FORMULARIO, wait_until="networkidle")
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

        print("Llenando texto (escribiendo letra por letra)...")
        textareas = await page.locator("textarea").all()
        if textareas:
            respuestas = ["Fomentar charlas.", "Mayor transparencia.", "Capacitaciones constantes.", "Nada que agregar.", "Difundir por intranet."]
            texto_elegido = random.choice(respuestas)
            # Hacemos clic primero en el campo para que tome el foco
            await textareas[0].click()
            await page.wait_for_timeout(500)
            # Escribimos simulando a un humano (delay de 50 milisegundos por letra)
            await textareas[0].type(texto_elegido, delay=50)
            await page.wait_for_timeout(500) # Pausa para que Google registre el texto
            print(f"-> Texto escrito: '{texto_elegido}'")

        print("Haciendo clic en Enviar...")
        try:
            # Buscar el botón exacto
            boton_enviar = page.locator("div[role='button']").filter(has_text="Enviar").or_(page.locator("div[role='button']").filter(has_text="Submit")).first
            await boton_enviar.click(timeout=5000)
            print("-> Clic en Enviar ejecutado.")
        except Exception as e:
            print(f"-> Error encontrando el botón: {e}")
        
        # Esperar un momento a que procese
        await page.wait_for_timeout(4000)
        
        # --- VERIFICACIÓN REAL ---
        # Si Google aceptó la respuesta, debería mostrar un mensaje de confirmación
        print("Verificando si la respuesta fue aceptada...")
        try:
            # Buscamos si en la pantalla aparece el texto típico de éxito
            exito = page.locator("text='Se ha registrado tu respuesta'").or_(page.locator("text='Your response has been recorded'")).first
            await exito.wait_for(timeout=5000)
            print("🎉 ¡CONFIRMADO! Google dice: 'Se ha registrado tu respuesta'.")
        except:
            # Si no aparece, revisamos si hay errores
            errores = await page.locator("text='obligatoria'").count() + await page.locator("text='required'").count()
            if errores > 0:
                print("❌ Google RECHAZÓ el envío: Hay preguntas obligatorias vacías.")
            else:
                print("⚠️ No se pudo confirmar el mensaje de éxito, pero el botón fue presionado. Revisa tu Google Forms.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
