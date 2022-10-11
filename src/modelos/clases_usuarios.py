from src.config.mysqlconnection import conectarMySQL
from flask import flash
import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CONTRASENA_REGEX = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$")


class Usuarios:
    def __init__(self, data): #en cada uno de los atributos de objetos estamos almacenando el valor de la clave de ese diccionario que obtenemos de la bd de nuestra tabla 
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.contraseña = data["contraseña"]
        self.created_at = data["created_at"]
        self.update_at = data["update_at"]

    @classmethod # ahora usamos métodos de clase para consultar o leer nuestra base de datos. NADA MAS
    def obtener_todo(cls):
        query = "SELECT * FROM usuarios;" #aqui llamamos a la tabla e nuestra base de datos
        results = conectarMySQL('examen_schema').query_db(query) #result serian un diccionario en donde conectamos con el nombre de nuestra base de datos y  vamos a llamar a la función conectarMySQL con el esquema al que te diriges
        
        usuarios_registro_instancias = []   # creamos una lista vacía para agregar nuestras instancias de usuarios
        for usuario_variable in results: # Iterar sobre los resultados de la base de datos y crear instancias de usuarios_instancias con cls
            usuarios_registro_instancias.append(cls(usuario_variable)) #convertimos una lista de diccionarios en una lista de objetos
        return usuarios_registro_instancias #retornamos una lista de objetos, lo transformamos a un objeto para poder usarlo en logica compleja desde html

#METODO CREATE con INSERT
    @classmethod
    def registro_usuario(cls, data): #(nombre de las columnas en nuestra tabla y en VALUES nombre de las claves de nuestro diccionario del controlador de forma sanitizada)
        query = """INSERT INTO usuarios (nombre, apellido, email, contraseña) 
        VALUES(%(nombre)s, %(apellido)s, %(email)s, %(contraseña)s);""" #se coloca al final NOW(), NOW()), solo si por defecto nuesrta tabla no lo tiene predeterminado y arriba created_at y update_at
        return conectarMySQL('examen_schema').query_db(query, data)
#no es necesario transformsarlo en objeto ya que solo estamos guardando informacion

#para obtener un usuario a traves de su id
    @classmethod  # ahora usamos métodos de clase para consultar nuestra base de datos de forma sanitizada
    def obtener_un_usuario(cls, data):
        query = "SELECT * FROM usuarios WHERE id=%(id_usuario)s;" #aca la variable que queremos es el WHERE id=1 (2 o 3, etc), debemos sanitizarla con % y s
        results =  conectarMySQL('examen_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0]) #aca retorna solo el diccionario, no objetos

#a traves del email estamos obteniendo un usuario
    @classmethod
    def obtener_por_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email=%(email)s;" #queremos la variable de email
        result = conectarMySQL('examen_schema').query_db(query, data)
        #no se encontro un usuario que coincida
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validar_formulario(usuario):
        datos_email = {
            "email":usuario['email']
        }
        validar = True # asumimos que esto es true
        if len(usuario['nombre']) < 2:
            flash("ATENCIÓN ¡NOMBRE debe tener al menos 2 caracteres!")
            validar = False
        if len(usuario['apellido']) < 2:
            flash("ATENCIÓN ¡APELLIDO debe tener al menos 2 caracteres!") 
            validar = False
        if (usuario['fnacimiento']) == "":
            flash("ATENCIÓN ¡Debe seleccionar una FECHA DE NACIMIENTO!") 
            validar = False
        if not CONTRASENA_REGEX.match(usuario['contraseña']): #contraseña debe tener minimo 6 caracteres, mayuscula, minuscula y caracter especial
            flash("ATENCIÓN CONTRASEÑA no cumple con los requisitos!") 
            validar = False
        if usuario['contraseña'] != usuario['confirmar']:
            flash("ATENCIÓN ¡CONTRASEÑAS no coinciden!") 
            validar = False
        if not EMAIL_REGEX.match(datos_email['email']): 
            flash("ATENCIÓN ¡Direccion de EMAIL no es valido!")  
            validar = False
        elif Usuarios.obtener_por_email(datos_email): 
            flash("ATENCIÓN ¡La direccion de EMAIL ya existe!") 
        return validar
