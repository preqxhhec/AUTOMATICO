import requests
import random
import time
import re

URL_VIEW = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/viewform"
URL_ENVIO = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/formResponse"

def enviar_una(session):
    # 1. Obtenemos el token y la página
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    page = session.get(URL_VIEW, headers=headers)
    
    # Buscamos el token con una expresión regular (más seguro en GitHub)
    match = re.search(r'name="fbzx" value="([^"]+)"', page.text)
    if not match:
        print("❌ No se encontró el token en la página.")
        return False
    token_fbzx = match.group(1)

    # 2. Preparamos los datos
    s1 = random.choice(["PABELLON", "Subdirección de Gestión y Desarrollo de las Personas"])
    s2 = random.choice(["Si", "No"])
    s3 = random.choice(["Si", "No"])
    s4 = random.choice(["Si", "No"])
    s5 = random.choice(["Si", "No"])
    s6 = random.choice(["Si", "No"])
    
    medios = random.sample(["Correo institucional", "WhatsApp", "Charlas presenciales", "Intranet"], 1)
    texto = random.choice([
        "Implementar un código de ética institucional claro y difundido",
        "Capacitar periódicamente a todo el personal en probidad y ética pública",
        "Crear un canal de denuncias confidencial y accesible"
    ])

    payload = (
        f"entry.1053311210={s1}&"
        f"entry.847966595={s2}&"
        f"entry.341909465={s3}&"
        f"entry.1591633300={s4}&"
        f"entry.718660351={s5}&"
        f"entry.793231334={s6}&"
        f"entry.83856868={medios[0]}&"
        f"entry.1245173661={texto}&"
        f"fvv=1&pageHistory=0&fbzx={token_fbzx}"
    )

    # 3. Enviamos
    r = session.post(URL_ENVIO, data=payload, headers=headers)
    if r.status_code != 200:
        print(f"Error {r.status_code}") # Imprimimos el error para depurar
    return r.status_code == 200

if __name__ == "__main__":
    print("Iniciando bot...")
    session = requests.Session()
    exitos = 0
    for i in range(5): # Envía 5 respuestas
        if enviar_una(session):
            exitos += 1
            print(f"✅ Respuesta {i+1} enviada.")
        else:
            print(f"❌ Falló la respuesta {i+1}.")
        time.sleep(1)
    print(f"Terminado: {exitos} de 5 enviadas.")