class Comentario:

    def __init__(self,usuario,descripcion,fecha):

        self.usuario = usuario
        self.descripcion = descripcion
        self.fecha = fecha

    def ver_comentario(self):
        return f"Usuario:{self.usuario}\tComentario: *{self.descripcion}*\tFecha:{self.fecha}"