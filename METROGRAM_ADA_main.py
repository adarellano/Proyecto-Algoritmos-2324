import uuid
import json
import requests
import uuid
from usuarios import Usuario, MUestudiante,MUprofesor
from multimedia import Post
from cometarios import Comentario


def iniciar_sesion(pListMetroUsers,pUsuarioActual):

    pUsuarioActual = None
    encontrado = False
    login = input("Usuario:\n->")
    for CadaUsuario in pListMetroUsers:
        if login.lower() == CadaUsuario.username.lower():
            pUsuarioActual = CadaUsuario
            encontrado = True
            break
    return encontrado,pUsuarioActual

def cerrar_sesion(pUsuarioActual):

    cierro_sesion = False
    logout = input("Desea cerrar sesión?:\n1.Si\n2.No\n->")
    if logout =="1":
        print(f"{pUsuarioActual.username} ha cerrardo sesión")
        cierro_sesion = True

    return cierro_sesion




#################   MODULO 1 ###################

def TraerMetroUsuarios(pListMetroUsers):
    """Permite cargar los usuarios al sistema
    Argumentos:
        pListMetroUsers (list) : Lista de los usuarios del sistema Metrogram
        """
    mydataByte = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json')
    mydataJson = (mydataByte.json())

    for item in mydataJson:
        if item.get("type") == "student":
            Metroestudiante = MUestudiante( item.get("id")
                                           ,item.get("firstName")
                                           ,item.get("lastName")
                                           ,item.get("email")
                                           ,item.get("username")
                                           ,item.get("major")
                                           ,item.get("following")
                                           ,[]
                                           )
            pListMetroUsers.append(Metroestudiante)
        elif item.get("type") == "professor":
            MetroProfesor = MUprofesor( item.get("id")
                                           ,item.get("firstName")
                                           ,item.get("lastName")
                                           ,item.get("email")
                                           ,item.get("username")
                                           ,item.get("department")
                                           ,item.get("following")
                                           ,[]
                                           )
            pListMetroUsers.append(MetroProfesor)

            #Inclusion del usuario ADMIN
            nuevoid = uuid.uuid1()
            Metroestudiante = MUestudiante(nuevoid
                                           ,"admin"
                                           ,"admin"
                                           ,"admin@unimet.edu.ve"
                                           ,"admin"
                                           ,"admin"
                                           ,[]
                                           ,[]
                                           )
            pListMetroUsers.append(Metroestudiante)




def mostrar_usuario(pListMetroUsers,CadaUsuario):

    print(CadaUsuario.ver_usuario())
    print("FOLLOWERS:")
    for CadaFollower in CadaUsuario.following:
        Following = buscarid(pListMetroUsers,CadaFollower)
        if Following == None:
            InfoF = "No tienes seguidores"
        else:
            InfoF = Following.ver_datos_follower()

        print(InfoF)



def buscarid(pListMetroUsers,idbuscar):

    Usuarioencontrado = None
    encontrado = False

    while not encontrado:
        for MetroUser in pListMetroUsers:
            if MetroUser.usuarioid == idbuscar:
                Usuarioencontrado = MetroUser
                encontrado = True
        break
    return Usuarioencontrado

def mostrar_una_publicacion(PublicacionActual):
    InfoPub = PublicacionActual.ver_multimedia()
    InfoLikes = PublicacionActual.ver_likes()
    InfoComentario = PublicacionActual.ver_comentario()
    print(InfoPub)
    print(InfoLikes)
    print(InfoComentario)




def mostrar_multimedia_otro(pListaMultimedia, UsuarioVisitado, UsuarioActual):
    ListaMultimediaOtro = []
    for CadaMutimedia in pListaMultimedia:
        if UsuarioVisitado.usuarioid == CadaMutimedia.usuario:
            ListaMultimediaOtro.append(CadaMutimedia)

    if ListaMultimediaOtro == []:
        print("El usuario " + UsuarioVisitado.username + " no tiene aún publiaciones")
    else:
        index = 0
        MaxIndex = len(ListaMultimediaOtro)-1
        while True:
            mostrar_una_publicacion(ListaMultimediaOtro[index])
            menu_pub_otro = input("1.Anterior\n2.Siguiente\n3.Dar like\n4.Comentar\n5.Regresar\n->")

            if menu_pub_otro == "1":

                if index > 0:
                    index -= 1

            if menu_pub_otro == "2":

                if index < MaxIndex:
                    index += 1

            if menu_pub_otro == "3":
                pListaMultimedia = dar_like_publicacion(pListaMultimedia, ListaMultimediaOtro[index], UsuarioActual)
            if menu_pub_otro == "4":

                pListaMultimedia = crear_comentario(pListaMultimedia,UsuarioActual,ListaMultimediaOtro[index])

            if menu_pub_otro == "5":
                break

    return pListaMultimedia



    if ListaMultimediaOtro == []:
        print("El usuario " + UsuarioVisitado.username + " no tiene aún publiaciones")
    else:
        index = 0
        MaxIndex = len(ListaMultimediaOtro)-1
        while True:
            mostrar_una_publicacion(ListaMultimediaOtro[index])
            menu_pub_otro = input("1.Anterior\n2.Siguiente\n3.Dar like\n4.Regresar\n->")

            if menu_pub_otro == "1":
                if index > 0:
                    index -= 1

            if menu_pub_otro == "2":
                if index < MaxIndex:
                    index += 1

            if menu_pub_otro == "3":
                pListaMultimedia = dar_like_publicacion(pListaMultimedia, ListaMultimediaOtro[index], UsuarioActual)
            if menu_pub_otro == "4":
                break
    return pListaMultimedia


def BuscarUsuarioUser(pListMetroUsers,pListaMultimedia,pUsuarioActual):


    encontrado = False
    while not encontrado:
        user = input("Username de la persona a buscar\n->")
        if user.lower() == pUsuarioActual.username.lower():
            print("* Colocó su propio username. Intente con otro *")
        else:
            encontrado = existe_usuario(pListMetroUsers, user)
            if encontrado == True:
                OtroUsuario = None
                for CadaUsuario in pListMetroUsers:
                    if user == CadaUsuario.username:
                        OtroUsuario = CadaUsuario
                        break

                pListaMultimedia,pListMetroUsers = menu_otrousuario(pListMetroUsers, pListaMultimedia, OtroUsuario, pUsuarioActual)
            else:
                print("* Usuario no encontrado *")
    return pListaMultimedia,pListMetroUsers

def BuscarUsuarioCarrera(pListMetroUsers):

    Listaedu = []


    buscacarrera = str(input("Carrera:\n->"))


    for CadaEstudiante in pListMetroUsers:
            if CadaEstudiante.tipo == "Estudiante":
                es_estudiante = CadaEstudiante.carrera
                if buscacarrera.lower() == es_estudiante.lower():
                    Listaedu.append(CadaEstudiante)
    for CadaCarreraEstudiante in Listaedu:
        print(CadaCarreraEstudiante.ver_datos_basicos())



def BuscarUserDepartamento(pListMetroUsers):

    ListaProf = []

    buscadepartamento = str(input("Departamento\n->"))

    for CadaProfesor in pListMetroUsers:
        if CadaProfesor.tipo == "Profesor":
            es_profesor = CadaProfesor.departamento
            if buscadepartamento.lower() == es_profesor.lower():
                ListaProf.append(CadaProfesor)
    for CadaDepartamentoProfesor in ListaProf:
        print(CadaDepartamentoProfesor.ver_datos_basicos())



def existe_usuario(pListMetroUsers, username):
    Encontrado = False
    for CadaUsuario in pListMetroUsers:
        if username == CadaUsuario.username:
            Encontrado = True
            break
    return Encontrado

def existe_correo(pListMetroUsers, usuariocorreo, tipo):

    if tipo == "1":
        usuariocorreo = usuariocorreo + "@correo.unimet.edu.ve"

    if tipo == "2":
        usuariocorreo = usuariocorreo + "@unimet.edu.ve"

    encontrado = False
    for CadaUsuario in pListMetroUsers:
        if usuariocorreo == CadaUsuario.email:
            encontrado = True
    return encontrado


def registrar_usuarios(pListMetroUsers):

    encontrado = True
    while encontrado:
        userunico = input("COLOCA TU USERNAME:\n->")
        encontrado = existe_usuario(pListMetroUsers, userunico)
        if encontrado == True:
            print("* Error ese username ya existe *\n Intenta con otro")

    nuevoid = uuid.uuid1()
    nuevonombre = str(input("COLOCA TU NOMBRE:\n->"))
    nuevoapellido = str(input("COLOCA TU APELLIDO:\n->"))
    nuevotipo = str(input("1.ESTUDIANTE\n2.PROFESOR\n->"))


    encontrado_email = True
    while encontrado_email:
        nuevoemail = str(input("COLOCA EL USUARIO DE TU EMAIL:\n->"))
        encontrado_email = existe_correo(pListMetroUsers,nuevoemail,nuevotipo)
        if encontrado_email == True:
            print(" Ya existe un usuario con ese correo\nIntenta de nuevo")

    if nuevotipo == "1":
        nuevacarrera = input("CARRERA:")

        nuevoMUestudiante = MUestudiante(nuevoid,nuevonombre.title(),nuevoapellido.title(),nuevoemail,userunico,nuevacarrera,[],[])
#ellos se añaden a  mis followers
        for CadaUsuario in pListMetroUsers:
            if CadaUsuario.tipo =="Estudiante":
                if nuevacarrera == CadaUsuario.carrera:
                    nuevoMUestudiante.following.append(CadaUsuario.usuarioid)

#yo me añado a su lista de followers
        index = 0
        max_index = len(pListMetroUsers)

        while index < max_index:

            CadaUsuario = pListMetroUsers[index]
            if CadaUsuario.tipo =="Estudiante":
                if nuevacarrera == CadaUsuario.carrera:
                    CadaUsuario.following.append(nuevoMUestudiante.usuarioid)
                    pListMetroUsers[index] = CadaUsuario
            index += 1

        pListMetroUsers.append(nuevoMUestudiante)

    if nuevotipo == "2":
        nuevodepartamento = input("DEPARTAMENTO:")
        nuevoMUprofesor = MUprofesor(nuevoid,nuevonombre.title(),nuevoapellido.title(),nuevoemail,userunico,nuevodepartamento,[])
#ellos se añaden a  mis followers
        for CadaUsuario in pListMetroUsers:
            if CadaUsuario.tipo =="Profesor":
                if nuevodepartamento == CadaUsuario.departamento:
                    nuevoMUestudiante.following.append(CadaUsuario.usuarioid)

#yo me añado a su lista de followers
        index = 0
        max_index = len(pListMetroUsers)

        while index < max_index:

            CadaUsuario = pListMetroUsers[index]
            if CadaUsuario.tipo =="Profesor":
                if nuevacarrera == CadaUsuario.carrera:
                    CadaUsuario.following.append(nuevoMUestudiante.usuarioid)
                    pListMetroUsers[index] = CadaUsuario
            index += 1

        pListMetroUsers.append(nuevoMUprofesor)



    print("** USUARIO CREADO CON EXITO **")



def cambiar_info(pListMetroUsers,UsuarioActual):


    opcion_cambiar = str(input("Deseas cambiar la información de tu cuenta?\n1.Si\n2.No"))

    if opcion_cambiar == "1":
        info_cambiar = str(input("Que deseas cambiar:\n1.Nombre\n2.Apellido\n3.Username\n4.Email"))
        if info_cambiar == "1":
            nuevonombre = input("Nuevo Nombre:\n->")
            UsuarioActual.nombre = nuevonombre.title()

        if info_cambiar == "2":
            nuevoapellido = str(input("Nuevo Apellido:\n->"))
            UsuarioActual.apellido = nuevoapellido.title()

        if info_cambiar == "3":

            encontrado = True
            while encontrado:
                nuevousername = str(input("Nuevo Username:\n->"))
                encontrado = existe_usuario(pListMetroUsers, nuevousername)
                if encontrado == True:
                    print("* Error ese username ya existe *\n Intenta con otro")
            UsuarioActual.username = nuevousername

        if info_cambiar == "4":

            encontrado_email = True
            while encontrado_email:
                nuevoemail = str(input("Nuevo Email:\n->"))
                encontrado_email = existe_correo(pListMetroUsers,nuevoemail,UsuarioActual.tipo)
                if encontrado_email == True:
                    print(" Ya existe un usuario con ese correo\nIntenta de nuevo")
            UsuarioActual.email = nuevoemail


    if opcion_cambiar == "2":
        print("No se han hecho cambios en la información")

    return UsuarioActual

def actualizar_usuario(pListMetroUsers,UsuarioActual):
    index = 0
    for CadaUsuario in  pListMetroUsers:
        if CadaUsuario.usuarioid == UsuarioActual.usuarioid:
            pListMetroUsers[index] = UsuarioActual
        index += 1
    return pListMetroUsers



def borrar_cuenta(pListMetroUsers,UsuarioActual,pListaMultimedia):

    borro_cuenta = False
    opcion_eliminar = input("Desea eliminar su cuenta?\n1.Si\n2.No")


    if opcion_eliminar == "1":

        eliminar_follower(pListMetroUsers,UsuarioActual.usuarioid)

        eliminar_post(pListaMultimedia,UsuarioActual.usuarioid)

        pListMetroUsers.remove(UsuarioActual)
        borro_cuenta = True
        print("* Cuenta Eliminada *")
    return borro_cuenta, pListMetroUsers,pListaMultimedia


def eliminar_follower(pListMetroUsers,idusuario):

    for CadaUsuario in pListMetroUsers:
        index = 0
        for CadaSeguidor in CadaUsuario.following:
            if CadaSeguidor == idusuario:
                CadaUsuario.following.pop(index)
            index += 1
    return pListMetroUsers

def eliminar_post(pListaMultimedia,idbuscar):

    for CadaMultimedia in pListaMultimedia:
        if CadaMultimedia.usuario == idbuscar:
            pListaMultimedia.remove(CadaMultimedia)
    return pListaMultimedia


############## MODULO 2 ###################

def TraerMultimedia(pListaMultimedia):
    mymultiByte = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json")
    mimultijson = mymultiByte.json()

    for item1 in mimultijson:
        dicmulti = item1.get("multimedia")
        MetroPost = Post(item1.get("publisher"),
                        item1.get("type"),
                        item1.get("caption"),
                        item1.get("date"),
                        item1.get("tags"),
                        [],
                        [],
                        dicmulti.get("url"))
        pListaMultimedia.append(MetroPost)


def mostrar_multimedia_propia(pListaMultimedia,CadaUsuario):
    for CadaMutimedia in pListaMultimedia:
        if CadaUsuario.usuarioid == CadaMutimedia.usuario:
            InfoMulti = CadaMutimedia.ver_multimedia()
            print(InfoMulti)



def registrar_post(pListaMultimedia,CadaUsuario):

        publicacion_user = input("SUBIR UNA PUBLICACIÓN:\n1.Si\n2.No\n->")
        if publicacion_user == "1":

            numeralnuevo = []

            foto_video = input("Desea subir\n1.Foto\n2.Video\n->")

            if foto_video == "1":

                descripcionnueva = (input("Coloca la descripcion de tu foto:\n->"))
                nuevotipo = "Foto"
                numeralesnuevos = input("Haghtags:\n->")
                numeralnuevo.append(numeralesnuevos)
                fechanueva = input("Fecha de la publicación:\n->")
                nueva_url = input("Coloca la descripcion de la url de tu foto:\n")
                nuevaurl = (f"htpps:://{nueva_url}/")
                NuevaMultimedia = Post(CadaUsuario.usuarioid,nuevotipo,descripcionnueva,fechanueva,numeralnuevo,[],[],nuevaurl)
                pListaMultimedia.append(NuevaMultimedia)





            if foto_video == "2":

                descripcionnueva = (input("Coloca la descripcion de tu video:\n->"))
                nuevotipo = "Video"
                numeralesnuevos = input("Haghtags:\n->")
                numeralnuevo.append(numeralesnuevos)
                fechanueva = input("Fecha de la publicación:\n->")
                nueva_url = input("Coloca la descripcion de la url de tu vídeo:\n")
                nuevaurl = (f"htpps:://{nueva_url}/")
                NuevaMultimedia = Post(CadaUsuario.usuarioid,nuevotipo,descripcionnueva,fechanueva,numeralnuevo,[],[],nuevaurl)
                pListaMultimedia.append(NuevaMultimedia)



def BuscarPostUser(pListaMultimedia,pListMetroUsers,CadaUsuario):


    encontrado = False
    while not encontrado:
        user_post = input("Username:\n->")
        encontrado = existe_usuario(pListMetroUsers, user_post)
        if encontrado == True:
            for CadaUsuario in pListMetroUsers:
                if user_post == CadaUsuario.username:
                    print(mostrar_multimedia_propia(pListaMultimedia,CadaUsuario))
                    encontrado = True
                    break
        else:
            print("* Usuario no encontrado *")


def Numeral_buscar(CadaPublicacion, numeral, pListaMultimedia):

   encontrado = False
   for CadaPublicacion in pListaMultimedia:
        if numeral == CadaPublicacion.numeral:
            Encontrado = True
            break
        return encontrado

def BuscarPostNumeral(pListaMultimedia,CadaPublicacion, numeral_buscar):


    numeral_buscar = input("Hashatg:\n->")
    publicacion_por_numeral = Numeral_buscar(CadaPublicacion, numeral_buscar, pListaMultimedia)
    if publicacion_por_numeral == True:
        for CadaPublicacion in pListaMultimedia:
            if numeral_buscar == CadaPublicacion.numeral:
                print(CadaPublicacion.ver_multimedia)




#### FOLLOWING  ####

def followers(CadaUsuario):

    for CadaFollower in CadaUsuario.following:
        if CadaFollower == CadaUsuario.usuarioid:
            print(CadaFollower.ver_datos_follower())


def solicitud_amistad(CadaUsuario,OtroUsuario):

#Caso estudiante

    if CadaUsuario.tipo == "Estudiante" and OtroUsuario.tipo == "Estudiante":
        if CadaUsuario.carrera == OtroUsuario.carrera:
            idusuariosolicitud = CadaUsuario.usuarioid
            OtroUsuario.following.append(idusuariosolicitud)
        else:
            encontrado = False
            for CadaSolicitud in OtroUsuario.solicitud_amistad:
                if CadaSolicitud == OtroUsuario.username:
                    encontrado = True
                    break
            if encontrado == False:
                OtroUsuario.solicitud_amistad.append(CadaUsuario.username)
    elif CadaUsuario.tipo == "Profesor" and OtroUsuario.tipo == "Profesor":
        #Caso profesor
        if CadaUsuario.departamento == OtroUsuario.departamento:
            idusuariosolicitud = CadaUsuario.usuarioid
            CadaUsuario.following.append(idusuariosolicitud)
        else:
            encontrado = False
            for CadaSolicitud in OtroUsuario.solicitud_amistad:
                if CadaSolicitud == OtroUsuario.username:
                    encontrado = True
                    break
            if encontrado == False:
                OtroUsuario.solicitud_amistad.append(CadaUsuario.username)
    else:
        encontrado = False
        for CadaSolicitud in OtroUsuario.solicitud_amistad:
            if CadaSolicitud == OtroUsuario.username:
                encontrado = True
                break
        if encontrado == False:
            OtroUsuario.solicitud_amistad.append(CadaUsuario.username)


    return CadaUsuario,OtroUsuario



def dejar_seguir(CadaUsuario,OtroUsuario):

    for follower in OtroUsuario.following:
        if follower == CadaUsuario.usuarioid:
            OtroUsuario.following.remove(follower)

    encontrado = False
    for CadaSolicitud in OtroUsuario.solicitud_amistad:
        if CadaSolicitud == OtroUsuario.username:
            encontrado = True
            break
        if encontrado == False:
            OtroUsuario.solicitud_amistad.append(CadaUsuario.username)


    return CadaUsuario,OtroUsuario


def aceptar_solicitud(CadaUsuario,OtroUsuario):

    for CadaSolicitud in CadaUsuario.solicitud_amistad:
        if CadaSolicitud == OtroUsuario.username:
            CadaUsuario.follow.append(OtroUsuario.usuarioid)
            CadaUsuario.solicitud_amistad.remove(CadaSolicitud)
    return CadaUsuario

def negar_solicitud(CadaUsuario,OtroUsuario):

    for CadaSolicitud in CadaUsuario.solicitud_amistad:
        if CadaSolicitud == OtroUsuario.username:
            CadaUsuario.solicitud_amistad.remove(CadaSolicitud)
    return CadaUsuario


def mostrar_solicitudes(CadaSolicitud):
    for CadaSolicitud in CadaUsuario.solicitud_amistad:
        print(CadaSolicitud)



def menu_mostrar_solicitud_amistad(pListMetroUsers,UsuarioActual):
    pListaSolicitudAmistad = []
    for CadaSolicitud in UsuarioActual.solicitud_amistad:

        if ListaSolicitudAmistad == []:
            print(f"{CadaUsuario.username} + no tiene aún solicitudes")
        else:
            index = 0
            MaxIndex = len(ListaSolicitudAmistad)-1
            while True:
                mostrar_solicitudes(UsuarioActual.solicitud_amistad[index])
                menu_sol_otro = input("1.Anterior\n2.Siguiente\n3.Aceptar Solicitud\n4.Negar Solicitud\n5.Regresar\n->")

                if menu_sol_otro == "1":
                    if index > 0:
                        index -= 1

                if menu_sol_otro == "2":
                    if index < MaxIndex:
                        index += 1

                if menu_pub_otro == "3":
                    UsuarioActual = aceptar_solicitud(UsuarioActual,OtroUsuario)
                if menu_sol_otro == "4":
                    UsuarioActual = negar_solicitud(UsuarioActual,OtroUsuario)
                if menu_sol_otro == "5":
                    break
        return CadaUsuario




### COMENTARIOS ###

def crear_comentario(pListaMultimedia,CadaUsuario,CadaPublicacion):


    comenta = input("Quieres comentar: \n1.Si\n2.No\n->")
    if comenta == "1":
        comentario = input("Comenta:\n->")
        fecha = input("Fecha del comentario:\n->")
        NewComentario = Comentario(CadaUsuario.username,comentario,fecha)
        CadaPublicacion.comentarios.append(NewComentario)
        index = 0
        for CadaP in pListaMultimedia:
            if CadaP.usuario == CadaPublicacion.usuario and CadaPublicacion.fecha == CadaP.fecha:
                pListaMultimedia[index] = CadaPublicacion
            index +=1

    return pListaMultimedia

def eliminar_comentario(pListaMultimedia,UsuarioActual,CadaPublicacion):

    for CadaPublicacion in pListaMultimedia:
        if CadaPublicacion.usuario == CadaUsuario.usuarioid:
            index = 0
            MaxIndex = len(pListaMultimedia)-1
            while True:
                mostrar_multimedia_propia(pListaMultimedia,)
                menu_comment = input("1.Anterior\n2.Siguiente\n3.Eliminar\n4.Regresar\n->")

                if menu_comment == "1":
                    if index > 0:
                        index -= 1

                if menu_comment == "2":
                    if index < MaxIndex:
                        index += 1
                if menu_comment== "3":
                        for CadaComentario in CadaPublicacion.comentarios:
                            CadaPublicacion.comentarios.remove(CadaComentario)
                if menu_comment =="4":
                    break
    return pListaMultimedia



### LIKES #

def dar_like_publicacion(pListaMultimedia, pPublicacionActual, UsuarioActual):
    for CadaPublicacion in pListaMultimedia:
        if CadaPublicacion.usuario == pPublicacionActual.usuario and CadaPublicacion.fecha == pPublicacionActual.fecha:
            if CadaPublicacion.likes == []:
                CadaPublicacion.likes.append(UsuarioActual.username)
            else:
                ExisteLike =False
                for CadaLike in CadaPublicacion.likes:
                    if CadaLike == UsuarioActual.username:
                        ExisteLike = True
                if ExisteLike == True:
                    CadaPublicacion.likes.remove(UsuarioActual.username)
                else:
                    CadaPublicacion.likes.append(UsuarioActual.username)
    return pListaMultimedia


### MENUS ###

def menu_dentro_perfil(pListMetroUsers,UsuarioActual,pListaMultimedia):

    usuario_existe = True

    while True:
        menu_dentro_perfil = input("1.Cambiar información de la cuenta\n2.Borrar cuenta\n3.Regresar\n->")

        if menu_dentro_perfil == "1":

            UsuarioActual = cambiar_info(pListMetroUsers,UsuarioActual)


        if menu_dentro_perfil == "2":
            borro_cuenta, pListMetroUsers,pListaMultimedia = borrar_cuenta(pListMetroUsers,UsuarioActual,pListaMultimedia)
            if borro_cuenta == True:
                usuario_existe = False
                break

        if menu_dentro_perfil =="3":
            break
    return usuario_existe,UsuarioActual

def menu_usuarioactual(ListMetroUsers,ListaMultimedia,UsuarioActual,CadaPublicación):
    while True:
        menu_perfil = input("1.Ver Perfil\n2.Mis Publicaciones\n3.Buscar Usuario\n4.Subir una publicación\n5.Buscar Publicaciones\n6.Solicitudes de amistad\n7.Eliminar comentarios\n8.Cerrar Sesión\n->")

        if menu_perfil == "1":
            mostrar_usuario(ListMetroUsers,UsuarioActual)
            usuario_existe,UsuarioActual = menu_dentro_perfil(ListMetroUsers,UsuarioActual,ListaMultimedia)
            if usuario_existe == False:
                break

        if menu_perfil == "2":

            mostrar_multimedia_propia(ListaMultimedia,UsuarioActual)

        if menu_perfil == "3":

            ListaMultimedia,ListMetroUsers = menu_buscar(ListMetroUsers,ListaMultimedia,UsuarioActual)

        if menu_perfil == "4":

            registrar_post(ListaMultimedia,UsuarioActual)

        if menu_perfil == "5":

            menu_post_buscar(ListaMultimedia,ListMetroUsers,UsuarioActual)

        if menu_perfil == "6":

            UsuarioActual = menu_mostrar_solicitud_amistad(ListMetroUsers,UsuarioActual)

        if menu_perfil == "7":

            eliminar_comentario(ListaMultimedia,UsuarioActual,CadaPublicacion)

        if menu_perfil == "8":
            if cerrar_sesion(UsuarioActual) == True:
                break
    return UsuarioActual,ListaMultimedia,ListMetroUsers

def menu_buscar(ListMetroUsers,ListaMultimedia,CadaUsuario):


    while True:
        menu_buscar = input("1.Username\n2.Por Carrera\n3.Por Departamento\n4.Regresar\n->")
        if menu_buscar == "1":

            ListaMultimedia,ListMetroUsers = BuscarUsuarioUser(ListMetroUsers,ListaMultimedia,CadaUsuario)

        if menu_buscar == "2":
            BuscarUsuarioCarrera(ListMetroUsers)
        if menu_buscar == "3":
            BuscarUserDepartamento(ListMetroUsers)
        if menu_buscar == "4":
            break
    return ListaMultimedia, ListMetroUsers

def menu_post_buscar(pListaMultimedia,pListMetroUsers,CadaUsuario):

    while True:
        menu_post_buscar = input("Buscar Post\n1.Por User\n2.Por Hashtag\n3.Regresar")

        if menu_post_buscar == "1":
            BuscarPostUser(pListaMultimedia,pListMetroUsers,CadaUsuario)

        if menu_post_buscar =="2":
            BuscarPostNumeral(pListaMultimedia,CadaPublicacion, numeral_buscar)

        if menu_buscar == "3":
            break


def menu_otrousuario(ListMetroUsers, ListaMultimedia, OtroUsuario, UsuarioActual):


    while True:

        menu_otro = input("\nCuenta de : " + OtroUsuario.nombre + "\n\n1.Ver Perfil\n2.Publicaciones\n3.Seguir\n4.Dejar de seguir\n5.Regresar\n->")

        if menu_otro == "1":
            mostrar_usuario(ListMetroUsers, OtroUsuario)

        if menu_otro == "2":
            ListaMultimedia = mostrar_multimedia_otro(ListaMultimedia, OtroUsuario, UsuarioActual)


        if menu_otro == "3":
            UsuarioActual,OtroUsuario = solicitud_amistad(UsuarioActual,OtroUsuario)
            index = 0
            for CadaUsuario in ListMetroUsers:
                if CadaUsuario.usuarioid == OtroUsuario.usuarioid:
                    break
                else:
                    index += 1
            ListaMultimedia[index] = OtroUsuario


        if menu_otro == "4":
            UsuarioActual,OtroUsuario = dejar_seguir(UsuarioActual,OtroUsuario)
            index = 0
            for CadaUsuario in ListMetroUsers:
                if CadaUsuario.usuarioid == OtroUsuario.usuarioid:
                    break
                else:
                    index += 1
            ListaMultimedia[index] = OtroUsuario


        if menu_otro == "5":
            break


    return ListaMultimedia,ListMetroUsers

def menu_estadisticas(pListaMultimedia,pListMetroUsers):
    opcion = input("1.Usuario con más publicaciones\n2.Carrera con mayor publicaciones\n3.Post con más interacciones\n4.Usuarios con más interacciones\n5.Usuario con más post eliminados\n6.Carreras con más comentarios inapropiados\n7.Usuarios eliminados\n->")
    if opcion =="1":
        usuario_mas_publi = usuario_con_mas_publicaciones(pListaMultimedia)
        for CadaUsuario in pListMetroUsers:
            if usuario_mas_publi == CadaUsuario.usuarioid:
                username_mas_puli = CadaUsuario.username
                print(f"El usuario con más publicaciones es: {username_mas_puli}")
    if opcion =="2":
        carrera_max = carrera_con_mas_publicaciones(pListaMultimedia,pListMetroUsers)
        print(f"La carrera con más publicaciones es: {carrera_max}")
    if opcion =="3":
        pass
    if opcion =="4":
        pass
    if opcion =="5":
        pass
    if opcion =="6":
        pass
    if opcion =="7":
        cuentas_eliminadas = borrar_cuenta_admin(pListMetroUsers,CadaUsuario,pListaMultimedia)


######################## ADMIN ############################

def borrar_cuenta_admin(pListMetroUsers,UsuarioActual,pListaMultimedia):
    cuentas_eliminadas = []

    pListMetroUsers = eliminar_follower(pListMetroUsers,UsuarioActual.usuarioid)
    pListaMultimedia = eliminar_post(pListaMultimedia,UsuarioActual.usuarioid)
    pListMetroUsers.remove(UsuarioActual)
    print("* Cuenta Eliminada *")
    cuenta_eliminada = cuentas_eliminadas.append(UsuarioActual)
    return pListMetroUsers, pListaMultimedia, cuentas_eliminadas



def mostrar_multimedia_admin(pListaMultimedia, UsuarioActual):

    for CadaMutimedia in pListaMultimedia:
        index = 0
        MaxIndex = len(pListaMultimedia)-1
        while True:
            mostrar_una_publicacion(ListaMultimediaOtro[index])
            menu_pub_otro = input("1.Anterior\n2.Siguiente\n3.Eliminar\n4.Regresar\n->")

            if menu_pub_otro == "1":

                if index > 0:
                    index -= 1

            if menu_pub_otro == "2":

                if index < MaxIndex:
                    index += 1

            if menu_pub_otro == "3":
                pListaMultimedia = eliminar_post(pListaMultimedia,UsuarioActual.usuarioid)
            if menu_pub_otro == "4":
                break


def admin_menu_otrousuario(ListMetroUsers, ListaMultimedia, OtroUsuario, UsuarioActual):

    while True:

        menu_otro = input("Admin ### Opciones del usuario : " + OtroUsuario.nombre + "\n\n1.Ver Perfil\n2.Publicaciones\n3.Eliminar cuenta\n4.Regresar\n->")

        if menu_otro == "1":
            mostrar_usuario(ListMetroUsers, OtroUsuario)

        if menu_otro == "2":
            pListaMultimedia = mostrar_multimedia_admin(pListaMultimedia, UsuarioActual)

        if menu_otro == "3":
            confirmar = input("Desea eliminar la cuenta de " + OtroUsuario.nombre + " (username: " + OtroUsuario.username + ")?:\n1.Si\n2.No\n->")
            if confirmar =="1":
                ListMetroUsers,ListaMultimedia= borrar_cuenta_admin(ListMetroUsers,OtroUsuario,ListaMultimedia)
                break

        if menu_otro == "4":
            break
    return ListMetroUsers, ListaMultimedia

def admin_BuscarUsuarioUsername(pListMetroUsers,pListaMultimedia,pUsuarioActual):


    encontrado = False
    while not encontrado:
        user = input("Admin ### \n\nUsername de la persona a buscar\n->")
        if user == pUsuarioActual.username:
            print("* Colocó su propio username. Intente con otro *")
        else:
            encontrado = existe_usuario(pListMetroUsers, user)
            if encontrado == True:
                OtroUsuario = None
                for CadaUsuario in pListMetroUsers:
                    if CadaUsuario.username == user:
                        OtroUsuario = CadaUsuario
                        break

                pListMetroUsers, pListaMultimedia = admin_menu_otrousuario(ListMetroUsers, ListaMultimedia, OtroUsuario, UsuarioActual)
            else:
                print("* Usuario no encontrado *")
    return pListMetroUsers, pListaMultimedia

def admin_BuscarUsuarioMultimedia():

    pass

def admin_menu_buscar(ListMetroUsers,ListaMultimedia,CadaUsuario):

    while True:
        menu_buscar = input("Admin ### Menu Buscar ###\n\n1.Username\n2.Regresar\n->")

        if menu_buscar == "1":

            admin_BuscarUsuarioUsername(ListMetroUsers,ListaMultimedia,CadaUsuario)

        if menu_buscar == "2":
            break

    return ListMetroUsers, ListaMultimedia

#Admin: Menu principal del usuario ADMIN
def admin_menu_usuario(ListMetroUsers,ListaMultimedia,UsuarioActual):
    while True:
        menu_perfil = input("Admin ### Menu Principal ###\n\n1.Buscar Usuario\n2.Buscar Publicaciones\n3.Estadisticas\n4.Salir\n->")

        if menu_perfil == "1":
           ListMetroUsers, ListaMultimedia = menu_buscar_admin(ListMetroUsers,ListaMultimedia,UsuarioActual)

        if menu_perfil == "2":
            pass
        if menu_perfil == "3":
            menu_estadisticas(ListaMultimedia,ListMetroUsers)

        if menu_perfil == "4":
            if cerrar_sesion(UsuarioActual) == True:
                break
    #debe retornar las listas porque pudo modificarlas. Pudo eliminar un usuario, o pudo eliminar publicaciones o comentarios.
    return ListMetroUsers, ListaMultimedia

################### FIN ADMIN ############################

def admin_BuscarUsuarioCarrera(pListMetroUsers):

    Listaedu = []


    buscacarrera = str(input("Carrera:\n->"))


    for CadaEstudiante in pListMetroUsers:
            if CadaEstudiante.tipo == "Estudiante":
                es_estudiante = CadaEstudiante.carrera
                if buscacarrera == es_estudiante:
                    Listaedu.append(CadaEstudiante)
    for CadaCarreraEstudiante in Listaedu:
        print(CadaCarreraEstudiante.ver_datos_basicos())



def admin_BuscarUserDepartamento(pListMetroUsers):

    ListaProf = []

    buscadepartamento = str(input("Departamento\n->"))

    for CadaProfesor in pListMetroUsers:
        if CadaProfesor.tipo == "Profesor":
            es_profesor = CadaProfesor.departamento
            if buscadepartamento == es_profesor:
                ListaProf.append(CadaProfesor)
    for CadaDepartamentoProfesor in ListaProf:
        print(CadaDepartamentoProfesor.ver_datos_basicos())

def menu_buscar_admin(ListMetroUsers,ListaMultimedia,CadaUsuario):


    while True:
        menu_buscar = input("1.Username\n2.Por Carrera\n3.Por Departamento\n4.Regresar\n->")
        if menu_buscar == "1":

            ListaMultimedia,ListMetroUsers = BuscarUsuarioUser(ListMetroUsers,ListaMultimedia,CadaUsuario)

        if menu_buscar == "2":
            admin_BuscarUsuarioCarrera(pListMetroUsers)
        if menu_buscar == "3":
            admin_BuscarUserDepartamento(pListMetroUsers)
        if menu_buscar == "4":
            break
    return ListaMultimedia, ListMetroUsers

def menu_post_buscar_admin(pListaMultimedia,pListMetroUsers,CadaUsuario,ListaPostNumeral,CadaPublicacion, numeral):

    while True:
        menu_post_buscar = input("Buscar Post\n1.Por User\n2.Por Hashtag\n3.Regresar")

        if menu_post_buscar == "1":
            BuscarPostUser(ListaMultimedia,ListMetroUsers,CadaUsuario)

        if menu_post_buscar =="2":
            BuscarPostNumeral(CadaPublicacion, numeral, ListaMultimedia)

        if menu_post_buscar == "3":
            break
    return ListaMultimedia


### MODULO 4 ###


def usuario_con_mas_publicaciones(pListaMultimedia):
    contador = {}
    for CadaPublicacion in pListaMultimedia:
        usuario = CadaPublicacion.usuario
        if usuario in contador:
            contador[usuario] += 1
        else:
            contador[usuario] = 1
    usuario_mas_publi = max(contador, key=contador.get)
    return usuario_mas_publi

def carrera_con_mas_publicaciones(pListaMultimedia,pListMetroUsers):
    contador_carreras = {}
    for CadaPublicacion in pListaMultimedia:
        ElUsuario = CadaPublicacion.usuario
        for CadaUsuario in pListMetroUsers:
            if CadaUsuario.tipo == "Estudiante":
                idUsuario = CadaUsuario.usuarioid
                if ElUsuario == idUsuario:
                    carrera = CadaUsuario.carrera
                    if carrera in contador_carreras:
                        contador_carreras[carrera] += 1
                    else:
                        contador_carreras[carrera] = 1
    carrera_max = max(contador_carreras, key=contador_carreras.get)
    return carrera_max




def main():


    UsuarioActual = None
    CadaPublicación = None
    numeral = None
    ListMetroUsers = []
    ListaMultimedia = []
    ListaPostNumeral = []
    TraerMetroUsuarios(ListMetroUsers)
    TraerMultimedia(ListaMultimedia)
    #mostrar_usuario(pListMetroUsers)
    #misma_carrera(ListMetroUsers,UsuarioActual,UsuarioActual)


    while True:
        opcion = input("*** Bienvenido a METROGRAM ***\n\n1.Iniciar sesión\n2.Nuevo usuario\n3.Salir\n->")

        if opcion == "1":
            UsuarioExiste,UsuarioActual = iniciar_sesion(ListMetroUsers,UsuarioActual)
            if UsuarioExiste == True:
                if UsuarioActual.username == "admin":
                    print(f" ### Bienvenido {UsuarioActual.nombre} ###")
                    ListMetroUsers, ListaMultimedia = admin_menu_usuario(ListMetroUsers, ListaMultimedia, UsuarioActual)

                else:

                    print(f" *** Bienvenido {UsuarioActual.nombre} ***")
                    UsuarioActual,ListaMultimedia,ListMetroUsers = menu_usuarioactual(ListMetroUsers,ListaMultimedia,UsuarioActual,numeral)
                    ListMetroUsers = actualizar_usuario(ListMetroUsers,UsuarioActual)

            else:
                print("Usuario no encontrado")


        elif opcion == "2":
            registrar_usuarios(ListMetroUsers)

        elif opcion == "3":
            print("*** METROGRAM ***")
            print("*** METROGRAM ***")
            print("*** METROGRAM ***")
            break

main()
















