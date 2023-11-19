class Usuario:
    def __init__ (self, usuarioid, nombre, apellido, email, username, tipo, following,solicitud_amistad):
        self.usuarioid = usuarioid
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.username = username
        self.tipo = tipo
        self.following = following
        self.solicitud_amistad = solicitud_amistad

    def ver_usuario(self):
      return f"Nombre {self.nombre} - Apellido {self.apellido} - Username {self.username} - {self.tipo}"

    def ver_datos_follower(self):
       return f"Nombre: {self.nombre} - Username: {self.username}"

    def ver_datos_basicos(self):
       return f"Nombre {self.nombre} - Username {self.username}"




class MUestudiante (Usuario):
    def __init__ (self,   usuarioid, nombre, apellido, email, username, carrera, following,solicitud_mistad):
        super().__init__(usuarioid, nombre, apellido, email, username, "Estudiante",following,solicitud_mistad)
        self.carrera = carrera


class MUprofesor(Usuario):
    def __init__ (self, usuarioid, nombre, apellido, email, username, departamento, following,solicitud_mistad):
        super().__init__(usuarioid, nombre, apellido, email, username, "Profesor",following,solicitud_mistad)
        self.departamento = departamento
