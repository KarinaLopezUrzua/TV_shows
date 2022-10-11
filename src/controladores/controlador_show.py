from src import app
from flask import render_template, redirect, session, request 
from src.modelos.clases_show import Show

@app.route("/crear_show") 
def formulario_show():
    if "id_usuario" not in session:
        return redirect("/")
    return render_template("crear.html")

@app.route("/crear_show", methods=["POST"]) 
def crear_show():
    if "id_usuario" not in session:
        return redirect("/")
    if not Show.validar_show(request.form, "crear"): 
        print(request.form)
        return redirect("/crear_show")
    print(request.form)
    id_show = Show.ingresar_show(request.form) 
    print(id_show)
    session["id_show"] = id_show 
    return redirect((f"/usuario/{session['id_usuario']}")) 

@app.route("/editar/<int:id_show>", methods=["GET","POST"]) 
def editar_show(id_show):
    if "id_usuario" not in session:
        return redirect("/")
    if request.method == "GET": 
        datos = {
        "id_show": id_show
        }
        ver_un_show = Show.obtener_un_show(datos)
        return render_template("editar.html", ver_show=ver_un_show)

    if not Show.validar_show(request.form, "editar"): 
        print(request.form) 
        return redirect((f"/editar/{id_show}"))

    datos = {
        "title":request.form["title"], 
        "network":request.form["network"],
        "release_date":request.form["release_date"],
        "description":request.form["description"],
        "id":id_show
    }
    Show.editar_show(datos) 
    return redirect((f"/usuario/{session['id_usuario']}"))

@app.route("/ver/<int:id_show>")
def ver_show(id_show):
    if "id_usuario" not in session:
        return redirect("/")
    datos = {
    "id_show": id_show
    }
    ver_un_show = Show.obtener_un_show(datos)
    return render_template("ver.html", ver_show=ver_un_show)

@app.route("/like/<int:id_show>")
def like_show(id_show):
    if "id_usuario" not in session:
        return redirect("/")
    datos = {
    "id_programa": id_show,
    "id_usuario": session["id_usuario"],
    }
    Show.dar_like_un_show(datos)
    return redirect((f"/usuario/{session['id_usuario']}"))

@app.route("/unlike/<int:id_show>")
def unlike_show(id_show):
    if "id_usuario" not in session:
        return redirect("/")
    datos = {
    "id_programa": id_show,
    "id_usuario": session["id_usuario"],
    }
    Show.dar_unlike_un_show(datos)
    return redirect((f"/usuario/{session['id_usuario']}"))

@app.route("/eliminar/<int:id_show>")
def borrar_show(id_show):
    if "id_usuario" not in session:
        return redirect("/")
    datos={
        "id_show": id_show
    }
    Show.eliminar_show(datos)
    return redirect((f"/usuario/{session['id_usuario']}"))
