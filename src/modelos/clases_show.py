from src.config.mysqlconnection import conectarMySQL
from flask import flash
from src.modelos.clases_usuarios import Usuarios

class Show:
    def __init__(self, data):  
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data["release_date"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.update_at = data["update_at"]
        self.usuario_id = data["usuario_id"]
        if "user_like" in data: 
            self.user_like = data["user_like"]
        else:
            self.user_like = None
        self.likes = None
        self.usuario = []

    @classmethod
    def ingresar_show(cls, data): 
        query = """INSERT INTO programas (title, network, release_date, description, usuario_id) 
        VALUES(%(title)s, %(network)s, %(release_date)s, %(description)s, %(usuario_id)s);""" 
        return conectarMySQL('examen_schema').query_db(query, data)

    @classmethod
    def dar_like_un_show(cls,data):
        query = "INSERT INTO likes (programa_id, usuario_id) VALUES (%(id_programa)s, %(id_usuario)s);" 
        return conectarMySQL('examen_schema').query_db(query, data)

    @classmethod
    def dar_unlike_un_show(cls,data):
        query = "DELETE FROM likes WHERE programa_id=%(id_programa)s and usuario_id=%(id_usuario)s;" 
        return conectarMySQL('examen_schema').query_db(query, data)

    @classmethod  
    def obtener_un_show(cls, data):
        query = "SELECT * FROM programas JOIN usuarios ON programas.usuario_id = usuarios.id WHERE programas.id=%(id_show)s;" 
        results =  conectarMySQL('examen_schema').query_db(query, data)
        if len(results) < 1:
            return False
        objeto_show = cls(results[0]) 
        objeto_show.usuario.append(Usuarios(results[0]))
        objeto_show.likes = cls.obtener_likes({"id": objeto_show.id})[0]['cantidad']
        return (objeto_show) 

    @classmethod 
    def obtener_con_usuario(cls, data):
        query = "SELECT p.*, u.*, l.usuario_id as user_like FROM programas p LEFT JOIN likes l ON p.id = l.programa_id and l.usuario_id = %(id_usuario)s JOIN usuarios u ON u.id = p.usuario_id;" 
        results = conectarMySQL('examen_schema').query_db(query, data) 
        if len(results) < 1:
            return []
        todos_show_usuario_instancias = []   
        for show_variable in results:
            objeto_show = cls(show_variable) 
            objeto_show.likes = cls.obtener_likes({"id": objeto_show.id})
            objeto_show.usuario.append(Usuarios(show_variable)) 
            todos_show_usuario_instancias.append(objeto_show)
        return todos_show_usuario_instancias 

    @classmethod
    def editar_show(cls,data):
        query = "UPDATE programas SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s WHERE id=%(id)s;" 
        return conectarMySQL('examen_schema').query_db(query, data)

    @classmethod
    def eliminar_show(cls,data):
        query = "DELETE FROM programas WHERE id=%(id_show)s;"
        return conectarMySQL('examen_schema').query_db(query, data)

    @classmethod
    def obtener_likes(cls,data):
        query = "SELECT count(*) as cantidad FROM likes WHERE programa_id=%(id)s;" 
        return conectarMySQL('examen_schema').query_db(query, data)

    @staticmethod
    def validar_show(show, accion):
        validar = True 
        if len(show['title']) < 3:
            flash("ATENCIÓN ¡TITLE debe tener al menos 3 caracteres!", accion)
            validar = False
        if len(show['network']) < 3:
            flash("ATENCIÓN ¡NETWORK debe tener al menos 3 caracteres!", accion) 
            validar = False
        if (show['release_date']) == "":
            flash("ATENCIÓN ¡RELEASE DATE es requerido!", accion) 
            validar = False
        if len(show['description']) < 3:
            flash("ATENCIÓN ¡DESCRIPTION debe tener al menos 3 caracteres!", accion) 
            validar = False
        return validar
