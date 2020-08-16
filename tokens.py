from flask import request

secret="123456"

# Genera el token y lo guarda en las cookies del cliente
def generateToken():
    token=""
    request.cookies.set('token', value=token)


# Recoge el token del cliente
def getToken():
    return request.cookies.get('token')


# Comprueba que el token sea válido, y que no haya caducado
def checkToken():
    token=""
    return token