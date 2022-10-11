from src.config.mysqlconnection import conectarMySQL
from flask import flash
import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CONTRASENA_REGEX = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$")


class Usuarios:
    def __init__(self, data):  
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.update_at = data["update_at"]

    @classmethod 
    def obtener_todo(cls):
        query = "SELECT * FROM usuarios;" 
        results = conectarMySQL('examen_schema').query_db(query) 
        
        usuarios_registro_instancias = []   
        for usuario_variable in results: 
            usuarios_registro_instancias.append(cls(usuario_variable)) 
        return usuarios_registro_instancias 

    @classmethod
    def registro_usuario(cls, data): 
        query = """INSERT INTO usuarios (first_name, last_name, email, password) 
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);""" 
        return conectarMySQL('examen_schema').query_db(query, data)

    @classmethod  
    def obtener_un_usuario(cls, data):
        query = "SELECT * FROM usuarios WHERE id=%(id_usuario)s;" 
        results =  conectarMySQL('examen_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0]) 

    @classmethod
    def obtener_por_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email=%(email)s;" 
        result = conectarMySQL('examen_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validar_formulario(usuario):
        datos_email = {
            "email":usuario['email']
        }
        validar = True 
        if len(usuario['first_name']) < 2:
            flash("ATENCIÓN ¡NOMBRE debe tener al menos 2 caracteres!")
            validar = False
        if len(usuario['last_name']) < 2:
            flash("ATENCIÓN ¡APELLIDO debe tener al menos 2 caracteres!") 
            validar = False
        if not CONTRASENA_REGEX.match(usuario['password']): #contraseña debe tener minimo 6 caracteres, mayuscula, minuscula y caracter especial
            flash("ATENCIÓN CONTRASEÑA no cumple con los requisitos!") 
            validar = False
        if usuario['password'] != usuario['confirmar']:
            flash("ATENCIÓN ¡CONTRASEÑAS no coinciden!") 
            validar = False
        if not EMAIL_REGEX.match(datos_email['email']): 
            flash("ATENCIÓN ¡Direccion de EMAIL no es valido!")  
            validar = False
        elif Usuarios.obtener_por_email(datos_email): 
            flash("ATENCIÓN ¡La direccion de EMAIL ya existe!") 
        return validar
