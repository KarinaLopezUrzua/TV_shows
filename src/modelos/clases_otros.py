from src.config.mysqlconnection import conectarMySQL
from flask import flash
from src.modelos.clases_usuarios import Usuarios

class Recetas:
    db = 'recetas_usuarios'

    def __init__(self, data): #en cada uno de los atributos de objetos estamos almacenando el valor de la clave de ese diccionario que obtenemos de la bd de nuestra tabla 
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.instrucciones = data["instrucciones"]
        self.fecha_creacion = data["fecha_creacion"]
        self.tiempo_preparacion = data["tiempo_preparacion"]
        self.created_at = data["created_at"]
        self.update_at = data["update_at"]
        self.usuario_id = data["usuario_id"]
        self.usuario = []
#se crea un diccionario vacio, para asignar a los usuarios con las recetas creadas self.usuario = None

#METODO CREATE con INSERT
    @classmethod
    def ingresar_receta(cls, data): #(nombre de las columnas en nuestra tabla y en VALUES nombre de las claves de nuestro diccionario del controlador de forma sanitizada)
        query = """INSERT INTO recetas (nombre, descripcion, instrucciones, fecha_creacion, tiempo_preparacion, usuario_id) 
        VALUES(%(nombre)s, %(descripcion)s, %(instrucciones)s, %(fecha_creacion)s, %(tiempo_preparacion)s, %(usuario_id)s);""" #se coloca al final NOW(), NOW()), solo si por defecto nuesrta tabla no lo tiene predeterminado y arriba created_at y update_at
        return conectarMySQL('examen_schema').query_db(query, data)
#no es necesario transformsarlo en objeto ya que solo estamos guardando informacion

#para obtener un usuario a traves de su id
    @classmethod  # ahora usamos métodos de clase para consultar nuestra base de datos de forma sanitizada
    def obtener_una_receta(cls, data):
        query = "SELECT * FROM recetas JOIN usuarios ON recetas.usuario_id = usuarios.id WHERE recetas.id=%(id_receta)s;" #aca la variable que queremos es el WHERE id=1 (2 o 3, etc), debemos sanitizarla con % y s
        results =  conectarMySQL('examen_schema').query_db(query, data)
        if len(results) < 1:
            return False
        objeto_receta = cls(results[0]) #la receta la hacemos un objeto
        objeto_receta.usuario.append(Usuarios(results[0]))
        return (objeto_receta) #aca retorna solo el diccionario, no objetos

    @classmethod # ahora usamos métodos de clase para consultar o leer nuestra base de datos. NADA MAS
    def obtener_todas_recetas(cls):
        query = "SELECT * FROM recetas;" #aqui llamamos a la tabla e nuestra base de datos
        results = conectarMySQL('examen_schema').query_db(query) #result serian un diccionario en donde conectamos con el nombre de nuestra base de datos y  vamos a llamar a la función conectarMySQL con el esquema al que te diriges
        
        recetas_instancias = []   # creamos una lista vacía para agregar nuestras instancias de recetas
        for receta_variable in results: # Iterar sobre los resultados de la base de datos y crear instancias de receta_instancias con cls
            recetas_instancias.append(cls(receta_variable)) #convertimos una lista de diccionarios en una lista de objetos
        return recetas_instancias #retornamos una lista de objetos, lo transformamos a un objeto para poder usarlo en logica compleja desde html

    @classmethod 
    def obtener_recetas_con_usuario(cls):#obtenemos las recetas con el usuario que la creo. nos entrega info de 2 tablas la de receta y usuario
        query = "SELECT * FROM recetas JOIN usuarios ON recetas.usuario_id = usuarios.id;" 
        results = conectarMySQL('examen_schema').query_db(query) 
        if len(results) < 1:
            return []
        todas_recetas_usuario_instancias = []   #creamos lista vacia que contiene todas las recetas
        for receta_variable in results:
            objeto_receta = cls(receta_variable) #la receta la hacemos un objeto
            objeto_receta.usuario.append(Usuarios(receta_variable)) #a ese objeto le agregamos el ususario que esta ligado, llamamos al atributo que es una lista vacia que hicimos arriba (usuario) y metemos toda la informacion de la clase Usuario en esa lista
            todas_recetas_usuario_instancias.append(objeto_receta)
        return todas_recetas_usuario_instancias 

#update para modificar una receta
    @classmethod
    def editar_receta(cls,data):
        query = "UPDATE recetas SET nombre=%(nombre)s, descripcion=%(descripcion)s, instrucciones=%(instrucciones)s, fecha_creacion=%(fecha_creacion)s, tiempo_preparacion=%(tiempo_preparacion)s WHERE id=%(id)s;" 
        return conectarMySQL('examen_schema').query_db(query, data)


#METODO DELETE, eliminar una receta 
    @classmethod
    def eliminar_receta(cls,data):
        query = "DELETE FROM recetas WHERE id=%(id_receta)s;"
        return conectarMySQL('examen_schema').query_db(query, data)

    @staticmethod
    def validar_recetas(receta):
        validar = True # asumimos que esto es true
        if len(receta['nombre']) < 2:
            flash("ATENCIÓN ¡NOMBRE debe tener al menos 2 caracteres!", 'crear')
            validar = False
        if len(receta['descripcion']) < 3:
            flash("ATENCIÓN ¡DESCRIPCIÓN debe tener al menos 3 caracteres!", 'crear') 
            validar = False
        if len(receta['instrucciones']) < 3:
            flash("ATENCIÓN ¡INSTRUCCIONES debe tener al menos 3 caracteres!", 'crear') 
            validar = False
        return validar

    @staticmethod
    def validar_editar(receta1):
        validar = True # asumimos que esto es true
        if len(receta1['nombre']) < 2:
            flash("ATENCIÓN ¡NOMBRE debe tener al menos 2 caracteres!", 'editar')
            validar = False
        if len(receta1['descripcion']) < 3:
            flash("ATENCIÓN ¡DESCRIPCIÓN debe tener al menos 3 caracteres!", 'editar') 
            validar = False
        if len(receta1['instrucciones']) < 3:
            flash("ATENCIÓN ¡INSTRUCCIONES debe tener al menos 3 caracteres!", 'editar') 
            validar = False
        return validar