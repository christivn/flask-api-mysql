from flask import request, jsonify, abort
from server import app, mysql

# Devuelve la info del proyecto solicitado
# Returns data of specified project
@app.route('/project/get/<id_proyecto>', methods=['GET'])
def get_project(id_proyecto):
    try:
        cur = mysql.connection.cursor()

        num_rows = cur.execute("SELECT * FROM proyectos WHERE id_proyecto='"+id_proyecto+"'")

        if num_rows:
            record = cur.fetchall()
            cur.close()
            return jsonify({ 'id':record[0][0],'name':record[0][1],'description':record[0][2],'url_photo':record[0][3],'start_date':record[0][4],'end_date':record[0][5]}), 200
        else: return jsonify({ 'msg':"Project doesnt exist" }), 404
    
    except Exception as e:
        abort(404)

# Agrega el proyecto a la base de datos (parametros pasados por el body del post)
# Adds the project to the db (params are passed through the post body)
@app.route('/project/add', methods=['POST'])
def add_project():
    try:
        name = request.form.get('name')
        desc = request.form.get('desc')
        url_photo = request.form.get('url_photo')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
    except Exception as e:
        return jsonify({ 'msg':'Error with params' }), 400

    try:
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO proyectos(nombre,descripcion,url_foto,fecha_inicio,fecha_fin) values(%s,%s,%s,%s,%s)", (name,desc,url_photo,start_date,end_date))
        mysql.connection.commit()
        return jsonify({ 'msg':'Project succesfully created' })
    except Exception as e:
        abort(404)

# Borra el proyecto solicitado
# Deletes specified project from db
@app.route('/project/delete/<id_proyecto>',methods=['DELETE'])
def delete_project(id_proyecto):
    try:
        cur =mysql.connection.cursor()

        num_rows=cur.execute("SELECT * FROM proyectos WHERE id_proyecto='"+id_proyecto+"'")
        if num_rows:
            cur.execute("DELETE FROM proyectos WHERE id_proyecto='"+id_proyecto+"'")
            mysql.connection.commit()
            return jsonify({ 'msg':'Project succesfully deleted' })
        else: return jsonify({ 'msg':'Project doesnt exist' }), 404
    except Exception as e:
        abort(404)
