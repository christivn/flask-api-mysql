from flask import request, jsonify
from server import app, mysql
from datetime import datetime


# Comprobar login, y generar token
@app.route('/auth/login', methods=['POST'])
def login():
    # Dos metodos de inicio por nick y por email
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y/%m/%d %H:%M:%S")

        nick = request.form.get('nick')
        email = request.form.get('email')
        password = request.form.get('password')
        fultimaconex = timestamp

        if nick is not None:
            tipoLogin="nick"
        else:
            tipoLogin="email"

    except Exception as e:
        return jsonify({ 'msg': 'Error with params'}), 400

    try:
        # Login usando nick
        if(tipoLogin=="nick"):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE nick='"+nick+"' and password='"+password+"'")
            num_rows = cur.fetchall()
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO userinfo (fecha_ultima_conexion) VALUES ('"+fultimaconex+"')")
            mysql.connection.commit()
            cur.close()

            if num_rows:
                date_time = now.strftime("%d/%m/%Y, %H:%M")
                print("\033[37m[\033[32m\033[01m+\033[0m\033[37m]\033[37m Login de usuario \033[35m{"+nick+"} \033[37m("+date_time+")\033[0m")
                return jsonify({ 'msg': 'Successful log-in'}), 200
            else:
                return jsonify({ 'msg': 'Account does not exist'}), 400
        
        # Login usando email
        if(tipoLogin=="email"):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE email='"+email+"' and password='"+password+"'")
            num_rows = cur.fetchall()
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO userinfo (fecha_ultima_conexion) VALUES ('"+fultimaconex+"')")
            mysql.connection.commit()
            cur.close()

            if num_rows:
                date_time = now.strftime("%d/%m/%Y, %H:%M")
                print("\033[37m[\033[32m\033[01m+\033[0m\033[37m]\033[37m Login de usuario \033[35m{"+email+"} \033[37m("+date_time+")\033[0m")
                return jsonify({ 'msg': 'Successful log-in'}), 200
            else:
                return jsonify({ 'msg': 'Account does not exist'}), 400

    except Exception as e:
        print(e)
        return jsonify({ 'msg': 'Error log-in'}), 200



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
    except Exception as e:
        return jsonify({ 'msg': 'Error with params'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE nick='"+nick+"'")
        num_rows = cur.fetchall()
        if num_rows:
            return jsonify({ 'msg': 'Error signing up due to duplicates' }), 400

        cur.execute("INSERT INTO usuarios (nick, email, password) VALUES (%s,%s,%s)", (nick, email, password))
        mysql.connection.commit()
        cur.execute("INSERT INTO userinfo (ip, fecha_registro, fecha_ultima_conexion) VALUES (%s,%s,%s)", (ip,fregistro,fultimaconex))
        mysql.connection.commit()
        cur.close()

        date_time = now.strftime("%d/%m/%Y, %H:%M")
        print("\033[37m[\033[32m\033[01m+\033[0m\033[37m]\033[37m Nuevo usuario registrado \033[35m{"+nick+"} \033[37m("+date_time+")\033[0m")
        return jsonify({ 'msg': 'Successful sign up'}), 200
    except Exception as e:
        return jsonify({ 'msg': 'Error signing up' }), 400

