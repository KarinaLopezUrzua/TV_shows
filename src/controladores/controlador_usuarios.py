from src import app
from flask import render_template, redirect, session, request 
from src.modelos.clases_usuarios import Usuarios
from src.modelos.clases_show import Show 
from flask import jsonify
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

@app.route("/") 
def formulario_raiz():
    return render_template("formulario.html") 


@app.route("/crear", methods=["POST"])
def crear_usuario():
    contrasena_encriptada = bcrypt.generate_password_hash(request.form['password'])
    print(contrasena_encriptada)
    datos = { 
        "first_name":request.form["first_name"], 
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password": contrasena_encriptada, 
    }
    if not Usuarios.validar_formulario(request.form): 
        print(datos)
        return redirect('/')
    print(datos)
    id_usuario = Usuarios.registro_usuario(datos) 
    print(id_usuario)
    session["id_usuario"] = id_usuario 
    return redirect(f"/usuario/{session['id_usuario']}") 

@app.route("/ingresar", methods=["POST"])
def ingreso_usuario():
    datos = {"email":request.form["email"]}
    usuario = Usuarios.obtener_por_email(datos) 
    if not usuario: 
        flash("ATENCIÓN: Email/Contraseña Invalidos") 
        return redirect("/")
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("ATENCIÓN: Email/Contraseña Invalidos")
        return redirect('/')
    session["id_usuario"] = usuario.id 
    return redirect(f"/usuario/{session['id_usuario']}") 

@app.route("/usuario/<int:id_usuario>")
def ver_usuario(id_usuario):
    if "id_usuario" not in session:
        return redirect("/")
    if id_usuario != session["id_usuario"]: 
        return redirect("/")
    datos = {
        "id_usuario": id_usuario
    }
    ver_usuario = Usuarios.obtener_un_usuario(datos)
    session["nombre_usuario"] = ver_usuario.first_name
    todas_los_show_con_usuario = Show.obtener_con_usuario(datos)
    return render_template("info.html", lista_show=todas_los_show_con_usuario, id_usuario=session["id_usuario"])

@app.errorhandler(404)
def invalid_route(e): 
    return jsonify({'errorCode' : 404, 'message' : 'Route not found'}) 

@app.errorhandler(500)
def server_error(e): 
    return jsonify({'errorCode' : 500, 'message' : e}) 

@app.route("/borrar_sesion") 
def eliminar_sesion():
    session.clear()
    return redirect("/")
