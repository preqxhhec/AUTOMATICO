import requests
import random
import time
from bs4 import BeautifulSoup

URL_VIEW = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/viewform"
URL_ENVIO = "https://docs.google.com/forms/d/e/1FAIpQLSfzCBr1UGj460ZxhOYcqglrgfgzKfufqCCYXVQbN3lLsEPKag/formResponse"

# Lista completa de 250 opciones (puedes cambiarla luego si quieres)
TEXTOS_LARGOS = [
    "Implementar un código de ética institucional claro y difundido",
    "Capacitar periódicamente a todo el personal en probidad y ética pública",
    "Crear un canal de denuncias confidencial y accesible"
]

def enviar_una(session, token_fbzx):
    # Mapeo exacto extraído del HTML
    s1 = random.choice(["PABELLON", "Subdirección de Gestión y Desarrollo de las Personas"])
    s2 = random.choice(["Si", "No"])
    s3 = random.choice(["Si", "No"])
    s4 = random.choice(["Si", "No"])
    s5 = random.choice(["Si", "No"])
    s6 = random.choice(["Si", "No"])
    
    medios_posibles = ["Correo institucional", "WhatsApp", "Charlas presenciales", "Intranet"]
    medios_elegidos = random.sample(medios_posibles, random.randint(1, 2))
    texto_libre = random.choice(TEXTOS_LARGOS)

    payload = (
        f"entry.1053311210={s1}&"
        f"entry.847966595={s2}&"
        f"entry.341909465={s3}&"
        f"entry.1591633300={s4}&"
        f"entry.718660351={s5}&"
        f"entry.793231334={s6}&"
    )
    
    for medio in medios_elegidos:
        payload += f"entry.83856868={medio}&"
        
    payload += (
        f"entry.1245173661={texto_libre}&"
        f"fvv=1&pageHistory=0&fbzx={token_fbzx}"
    )

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = session.post(URL_ENVIO, data=payload, headers=headers)
    return r.status_code == 200

if __name__ == "__main__":
    print("Iniciando bot desde GitHub...")
    # Aquí definimos cuántas respuestas enviar por cada clic en GitHub
    cant = 5 
    
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    page = session.get(URL_VIEW, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    token_fbzx = soup.find('input', {'name': 'fbzx'})['value']

    exitos = 0
    for i in range(cant):
        if enviar_una(session, token_fbzx):
            exitos += 1
            print(f"✅ Respuesta {i+1} enviada.")
        else:
            print(f"❌ Falló la respuesta {i+1}.")
        time.sleep(1)
        
    print(f"Terminado: {exitos} de {cant} enviadas.")