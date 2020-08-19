from flask import request, jsonify
from server import app, mysql
from tokens import getToken, generateToken, checkToken
from datetime import datetime


# Comprobar login, y generar token
@app.route('/auth/login', methods=['POST'])
def login():
    try:
        tipoLogin="nick"
        nick = request.args['nick']
        password = request.args['password']
    except:
        try:
            tipoLogin="email"
            email = request.args['email']
            password = request.args['password']
        except:
            return jsonify({ 'msg': 'Error en los parametros', 'code':400 })

    ##################
    #   Consultas SQL
    ##################

    return jsonify({ 'token': '1234567890', 'code':200 })



# Registro, check de disponibilidad de usuario, y generar token
@app.route('/auth/register', methods=['POST'])
def register():
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y/%m/%d %H:%M:%S")

        nick = request.form.get('nick')
        email = request.form.get('email')
        password = request.form.get('password')
        ip = request.remote_addr
        fregistro = timestamp
        fultimaconex = timestamp
    except:
        return jsonify({ 'msg': 'Error en los parametros', 'code':400 }), 400

    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM usuarios WHERE nick='"+nick+"'")
        num_rows = cur.fetchall()
        if num_rows:
            return jsonify({ 'msg': 'Error signing up due to duplicates', 'code':400 }), 400

        cur.execute("INSERT INTO usuarios (nick, email, password) VALUES (%s,%s,%s)", (nick, email, password))
        mysql.connection.commit()
        cur.execute("INSERT INTO userinfo (ip, fecha_registro, fecha_ultima_conexion) VALUES (%s,%s,%s)", (ip,fregistro,fultimaconex))
        mysql.connection.commit()
        cur.close()

        date_time = now.strftime("%d/%m/%Y, %H:%M")
        print("\033[37m[\033[32m\033[01m+\033[0m\033[37m]\033[37m Nuevo usuario registrado \033[35m{"+nick+"} \033[37m("+date_time+")\033[0m")
        return jsonify({ 'msg': 'Successful sign up', 'token':'1234567890', 'code':200 })
    except:
        return jsonify({ 'msg': 'Error signing up', 'code':400 }), 400

