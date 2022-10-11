from src import app
from flask import render_template, redirect, session, request 
from src.modelos.clases_otros import Recetas

@app.route("/crear_receta") #ruta que se redigire action del formulario
def formulario_receta():
    if "id_usuario" not in session:
        return redirect("/")
    return render_template("crear_receta.html")
#tenemos que concatenar, con formart y comillas simples


@app.route("/crear_receta", methods=["POST"]) #ruta que se redigire action del formulario
def crear_receta():
    if "id_usuario" not in session:
        return redirect("/")
    if not Recetas.validar_recetas(request.form): #validacion
        print(request.form)
        # redirigir a la ruta donde se renderiza el formulario 
        return redirect("/crear_receta")
    print(request.form)
    id_receta = Recetas.ingresar_receta(request.form) #le agregamos una variable para poder retornar un numero y asi traquear al usuario para darle seguimiento con session. se llama al metodo para guardar la informacion en la base de datos
    print(id_receta)
    session["id_receta"] = id_receta #estamos almacenando la variable en una clave llamada id_usuario. esta llave va a contener el numero del usuario creado
    return redirect((f"/usuario/{session['id_usuario']}")) #se redirige a la pagina donde se muestra la informacion del usuario con su id a traves de id_usuario
#tenemos que concatenar, con formart y comillas simples



#ruta MIXTA para modificar los datos de la receta (se puede realizar en 2 rutas distintas)
@app.route("/editar/<int:id_receta>", methods=["GET","POST"]) #va a recibir 2 metodos
def editar_receta(id_receta):
    if "id_usuario" not in session:
        return redirect("/")
    if request.method == "GET": #si entra un metodo get, se entra a esta linea y se obtienen los datos del usuario para modificarlos
        datos = {
        "id_receta": id_receta
        }
        ver_una_receta = Recetas.obtener_una_receta(datos)
        return render_template("editar_receta.html", ver_receta=ver_una_receta)

    if not Recetas.validar_editar(request.form): #validacion
        print(request.form)
        # redirigir a la ruta donde se renderiza el formulario 
        return redirect((f"/editar/{id_receta}"))

    datos = {
        "nombre":request.form["nombre"], #["nombre"] es el name que se coloco en el imput del formulario
        "descripcion":request.form["descripcion"],
        "instrucciones":request.form["instrucciones"],
        "fecha_creacion":request.form["fecha_creacion"],
        "tiempo_preparacion":request.form["tiempo_preparacion"],
        "id":id_receta
    }
    Recetas.editar_receta(datos) #una vez modificado entrara a la tabla y se mostrara en la pagina
    return redirect((f"/usuario/{session['id_usuario']}"))



@app.route("/ver/<int:id_receta>")
def ver_receta(id_receta):
    if "id_usuario" not in session:
        return redirect("/")
    datos = {
    "id_receta": id_receta
    }
    ver_una_receta = Recetas.obtener_una_receta(datos)
    return render_template("ver_receta.html", ver_receta=ver_una_receta)



#ruta para eliminar una receta
@app.route("/eliminar/<int:id_receta>")
def borrar_receta(id_receta):
    if "id_usuario" not in session:
        return redirect("/")
    datos={
        "id_receta": id_receta
    }
    Recetas.eliminar_receta(datos)
    return redirect((f"/usuario/{session['id_usuario']}"))

""" colocar en TODAS las rutas GET
    if "id_usuario" not in session:
        return redirect("/")
"""