import uuid
import json
import requests
import uuid
from usuarios import Usuario, MUestudiante,MUprofesor
from multimedia import Post
from cometarios import Comentario


""" Inicio sesion con usuarios creados, admin para entrar a la cuenta de administrador, y con los nuevos usuarios"""

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



""" Muestro al usuario con sus followers y sus datos del metodo ver usuario """

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

""" Validacion de si el id existe """

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

""" Validacion de si el username existe """


def buscarUsername(pListMetroUsers,Usernamebuscar):

    Usuarioencontrado = None
    encontrado = False

    while not encontrado:
        for MetroUser in pListMetroUsers:
            if MetroUser.username == Usernamebuscar:
                Usuarioencontrado = MetroUser
                encontrado = True
        break
    return Usuarioencontrado

""" Muestro las publicaciones todas con todos sus atributos, añadiendo sus likes y comentarios """

def mostrar_una_publicacion(PublicacionActual):
    InfoPub = PublicacionActual.ver_multimedia()
    InfoLikes = PublicacionActual.ver_likes()
    InfoComentario = PublicacionActual.ver_comentario()
    print(InfoPub)
    print(InfoLikes)
    print(InfoComentario)


""" Cuando entro al perfil de otro usuario, es decir Ada como usuario quiere ver las publicaciones de Antonio
,asimismo se añadieron las funciones de dar like y comentar, y se entra de publicacion en publicacion """


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

""" Buscar usuario por nombre de usuario, es decir, por el atributo username """

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

""" Buscar usuario por nombre de tipo, es decir, por el atributo carrera, si es estudiante, me muestra la lista de estudiante en tal carrera """

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

""" Buscar usuario por nombre de tipo, es decir, por el atributo carrera, si es profesor, me muestra la lista de estudiante en tal departamento """


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


""" Validacion de que exista el usuario por su username """



def existe_usuario(pListMetroUsers, username):
    Encontrado = False
    for CadaUsuario in pListMetroUsers:
        if username == CadaUsuario.username:
            Encontrado = True
            break
    return Encontrado

""" Validacion de que exista el usuario por correo, se asume que el usuario pertenece a la UNIMET por lo tanto se le pide la primera parte de su correo
si es estudiante se agrega el correo.unimet, si es pofesor, solo el unimet """

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

""" Se registra el usuario y se hace el follow automatico """

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

""" Cambio de la informacion de la cuenta """


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

""" Elimina la cuenta desde el menu propio y lo elimina desde la cuenta de administrador"""


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

""" Si se elimina la cuenta, se eliminan de los followers de los demás """

def eliminar_follower(pListMetroUsers,idusuario):

    for CadaUsuario in pListMetroUsers:
        index = 0
        for CadaSeguidor in CadaUsuario.following:
            if CadaSeguidor == idusuario:
                CadaUsuario.following.pop(index)
            index += 1
    return pListMetroUsers

""" Si se elimina la cuenta, se eliminan sus post """

def eliminar_post(pListaMultimedia,idbuscar):

    for CadaMultimedia in pListaMultimedia:
        if CadaMultimedia.usuario == idbuscar:
            pListaMultimedia.remove(CadaMultimedia)
    return pListaMultimedia


############## MODULO 2 ###################

""" Se crean las publicaciones como obetos desde la api """

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


""" Veo todas las publicaciones """


def mostrar_multimedia_propia(pListaMultimedia,CadaUsuario):
    for CadaMutimedia in pListaMultimedia:
        if CadaUsuario.usuarioid == CadaMutimedia.usuario:
            InfoMulti = CadaMutimedia.ver_multimedia()
            print(InfoMulti)

""" Registro un post como objeto y lo añado a la lista de multimedia """

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


""" Busco todos los ost de un user """

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

""" Validación si el hashtag existe """


def Numeral_buscar(CadaPublicacion, numeral, pListaMultimedia):

   encontrado = False
   for CadaPublicacion in pListaMultimedia:
        if numeral == CadaPublicacion.numeral:
            Encontrado = True
            break
        return encontrado

   """ Busco post por hashtag, lo llame numeral porque era mas facil de escribir a la hora de programar """

def BuscarPostNumeral(pListaMultimedia,CadaPublicacion, numeral_buscar):


    numeral_buscar = input("Hashatg:\n->")
    publicacion_por_numeral = Numeral_buscar(CadaPublicacion, numeral_buscar, pListaMultimedia)
    if publicacion_por_numeral == True:
        for CadaPublicacion in pListaMultimedia:
            if numeral_buscar == CadaPublicacion.numeral:
                print(CadaPublicacion.ver_multimedia)




#### FOLLOWING  ####

""" Muestro los followers con sus datos como objeto, con su metodo de ver """

def followers(CadaUsuario):

    for CadaFollower in CadaUsuario.following:
        if CadaFollower == CadaUsuario.usuarioid:
            print(CadaFollower.ver_datos_follower())

""" Solicito seguir a un usuario si no somos dela misma carrera """


def solicitud_amistad_usuario(CadaUsuario,OtroUsuario):

#Caso estudiante

    if CadaUsuario.tipo == "Estudiante" and OtroUsuario.tipo == "Estudiante":
        if CadaUsuario.carrera == OtroUsuario.carrera:
            idusuariosolicitud = CadaUsuario.usuarioid
            OtroUsuario.following.append(idusuariosolicitud)
            print("Usted fue añadido como seguidor de " + OtroUsuario.nombre)
        else:
            encontrado = False
            for CadaSolicitud in OtroUsuario.solicitud_amistad:
                if CadaSolicitud == OtroUsuario.username:
                    encontrado = True
                    break
            if encontrado == False:
                OtroUsuario.solicitud_amistad.append(CadaUsuario.username)
                print("Solicitud de amistad enviada")
    elif CadaUsuario.tipo == "Profesor" and OtroUsuario.tipo == "Profesor":
        #Caso profesor
        if CadaUsuario.departamento == OtroUsuario.departamento:
            idusuariosolicitud = CadaUsuario.usuarioid
            OtroUsuario.following.append(idusuariosolicitud)
            print("Usted fue añadido como seguidor de " + OtroUsuario.nombre)
        else:
            encontrado = False
            for CadaSolicitud in OtroUsuario.solicitud_amistad:
                if CadaSolicitud == OtroUsuario.username:
                    encontrado = True
                    break
            if encontrado == False:
                OtroUsuario.solicitud_amistad.append(CadaUsuario.username)
                print("Solicitud de amistad enviada")
    else:
        encontrado = False
        for CadaSolicitud in OtroUsuario.solicitud_amistad:
            if CadaSolicitud == OtroUsuario.username:
                encontrado = True
                break
        if encontrado == False:
            OtroUsuario.solicitud_amistad.append(CadaUsuario.username)
            print("Solicitud de amistad enviada")



    return CadaUsuario,OtroUsuario

""" Dejo de seguir a un usuario  """

def dejar_seguir(CadaUsuario, OtroUsuario):

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

""" Acepto la solicitud de un usuario  """


def aceptar_solicitud(UsuarioActual, UsuarioSolicitante):

    UsuarioActual.following.append(UsuarioSolicitante.usuarioid)
    UsuarioActual.solicitud_amistad.remove(UsuarioSolicitante.username)
    return UsuarioActual

"""  No dejo que un usuario me siga  """

def negar_solicitud(UsuarioActual, UsuarioSolicitante):

    UsuarioActual.solicitud_amistad.remove(UsuarioSolicitante.username)
    return UsuarioActual


""" Muestra las solicitudes por username del que solicitó seguir  """

def mostrar_solicitud(CadaSolicitud):
    print("Solicitud de amistad de: " + CadaSolicitud)

""" Parecido al menu de las publicaciones, enu de solicitudes para verla una por una y aceptar y negar, con las funciones anteriores """


def menu_mostrar_solicitud_amistad(pListMetroUsers, UsuarioActual):
    ListaAmistadUsername = UsuarioActual.solicitud_amistad

    if ListaAmistadUsername == []:
        print("El usuario " + UsuarioActual.username + " no tiene aún solicitudes de amistad")
    else:
        index = 0
        MaxIndex = len(ListaAmistadUsername)-1
        while True:
            mostrar_solicitud(ListaAmistadUsername[index])
            menu_sol_otro = input("1.Anterior\n2.Siguiente\n3.Aceptar Solicitud\n4.Negar Solicitud\n5.Regresar\n->")

            if menu_sol_otro == "1":
                if index > 0:
                    index -= 1

            if menu_sol_otro == "2":
                if index < MaxIndex:
                    index += 1

            if menu_sol_otro == "3":
                UsuarioSolicitante = buscarUsername(pListMetroUsers, ListaAmistadUsername[index])
                UsuarioActual = aceptar_solicitud(UsuarioActual, UsuarioSolicitante)
                break

            if menu_sol_otro == "4":
                UsuarioSolicitante = buscarUsername(pListMetroUsers, ListaAmistadUsername[index])
                UsuarioActual = negar_solicitud(UsuarioActual, UsuarioSolicitante)
                break

            if menu_sol_otro == "5":
                break

        return pListMetroUsers, UsuarioActual




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

def eliminar_comentario(pListaMultimedia,CadaUsuario,CadaPublicacion):

    for CadaPublicacion in pListaMultimedia:
        if CadaPublicacion.usuario == CadaUsuario.usuarioid:
            index = 0
            MaxIndex = len(pListaMultimedia)-1
            while True:
                mostrar_solicitud( CadaUsuario.solicitud_amistad[index])
                menu_comment_otro = input("1.Anterior\n2.Siguiente\n3.Eliminar\n5.Regresar\n->")

                if menu_comment_otro == "1":
                    if index > 0:
                        index -= 1

                if menu_comment_otro == "2":
                    if index < MaxIndex:
                        index += 1
                if menu_comment_otro == "3":
                        for CadaComentario in CadaPublicacion.comentarios:
                            CadaPublicacion.comentarios.remove(CadaComentario)



### LIKES #

""" Funcion de dar like, y si ya lo tenia, se le quita. Esa validación esta dentro de la funcion """

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

""" Trabaje con menus diferentes y fui del más pequeño al más grande, está el de ver perfil, el de buscar usuarios, el de buscar multimedia, y dentro de ellos, pequeños menus para hacer distintas funciones """

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
        menu_perfil = input("1.Ver Perfil\n2.Mis Publicaciones\n3.Buscar Usuario\n4.Subir una publicación\n5.Buscar Publicaciones\n6.Solicitudes de amistad\n7.Cerrar Sesión\n->")

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
            menu_mostrar_solicitud_amistad(ListMetroUsers, UsuarioActual)

        if menu_perfil == "7":
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

""" Este menu es para cuando entro a la cuenta de un usuario, y quiero ver sus publicaciones y seguir o dejar de seguir. Dentro de la funcion esta la validacion de que si no lo sigo no puedo ver sus fotos hasta solicitar la amistad  """

def menu_otrousuario(ListMetroUsers, ListaMultimedia, OtroUsuario, UsuarioActual):


    while True:

        menu_otro = input("\nCuenta de : " + OtroUsuario.nombre + "\n\n1.Ver Perfil\n2.Publicaciones\n3.Seguir\n4.Dejar de seguir\n5.Regresar\n->")

        if menu_otro == "1":
            mostrar_usuario(ListMetroUsers, OtroUsuario)

        if menu_otro == "2":
            SoyFolowing = False
            if OtroUsuario.following != []:
                for CadaFollow in OtroUsuario.following:
                    if CadaFollow == UsuarioActual.usuarioid:
                        SoyFolowing = True
            if SoyFolowing == True:
                ListaMultimedia = mostrar_multimedia_otro(ListaMultimedia, OtroUsuario, UsuarioActual)
            else:
                print("No puede ver las publicaciones de este usuario. Usted no lo sigue.")


        if menu_otro == "3":
            UsuarioActual, OtroUsuario = solicitud_amistad_usuario(UsuarioActual, OtroUsuario)
            index = 0
            for CadaUsuario in ListMetroUsers:
                if CadaUsuario.usuarioid == OtroUsuario.usuarioid:
                    break
                else:
                    index += 1
            ListMetroUsers[index] = OtroUsuario


        if menu_otro == "4":
            UsuarioActual,OtroUsuario = dejar_seguir(UsuarioActual,OtroUsuario)
            index = 0
            for CadaUsuario in ListMetroUsers:
                if CadaUsuario.usuarioid == OtroUsuario.usuarioid:
                    break
                else:
                    index += 1
            ListMetroUsers[index] = OtroUsuario


        if menu_otro == "5":
            break


    return ListaMultimedia,ListMetroUsers

""" Este menu es del admin  """

def menu_estadisticas(pListaMultimedia,pListMetroUsers, ListaCuentasElinminadas):
    while True:
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
            if ListaCuentasElinminadas == []:
                print("No hay cuentas eliminadas...\n")
            else:
                print("Cuentas elmininadas:")
                for CadaCuenta in ListaCuentasElinminadas:
                    print (CadaCuenta.username)
                print("\n")
        if opcion =="8":
            break


######################## ADMIN ############################

""" Borrar un cuenta como administrador  """

def borrar_cuenta_admin(pListMetroUsers, UsuarioActual, pListaMultimedia, ListaCuentasElinminadas):

    pListMetroUsers = eliminar_follower(pListMetroUsers,UsuarioActual.usuarioid)
    pListaMultimedia = eliminar_post(pListaMultimedia,UsuarioActual.usuarioid)
    pListMetroUsers.remove(UsuarioActual)
    print("* Cuenta Eliminada *")
    ListaCuentasElinminadas.append(UsuarioActual)
    return pListMetroUsers, pListaMultimedia, ListaCuentasElinminadas

""" Eliminar post como admin  """

def mostrar_multimedia_admin(pListaMultimedia, UsuarioActual):

    for CadaMutimedia in pListaMultimedia:
        index = 0
        MaxIndex = len(pListaMultimedia)-1
        while True:
            mostrar_una_publicacion(ListaMultimediaOtro[index])
            menu_pub_otro = input("Admin ### Multimedia\n\n1.Anterior\n2.Siguiente\n3.Eliminar\n4.Regresar\n->")

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

""" Meterme como admin en la cuenta de otro usuario y borrar su cuenta  """

def admin_menu_otrousuario(ListMetroUsers, ListaMultimedia, OtroUsuario, UsuarioActual, ListaCuentasElinminadas):

    while True:

        menu_otro = input("Admin ### Opciones del usuario : " + OtroUsuario.nombre + "\n\n1.Ver Perfil\n2.Publicaciones\n3.Eliminar cuenta\n4.Regresar\n->")

        if menu_otro == "1":
            mostrar_usuario(ListMetroUsers, OtroUsuario)

        if menu_otro == "2":
            pListaMultimedia = mostrar_multimedia_admin(ListaMultimedia, UsuarioActual)

        if menu_otro == "3":
            confirmar = input("Desea eliminar la cuenta de " + OtroUsuario.nombre + " (username: " + OtroUsuario.username + ")?:\n1.Si\n2.No\n->")
            if confirmar =="1":
                ListMetroUsers,ListaMultimedia, ListaCuentasElinminadas = borrar_cuenta_admin(ListMetroUsers,OtroUsuario,ListaMultimedia, ListaCuentasElinminadas)
                break

        if menu_otro == "4":
            break
    return ListMetroUsers, ListaMultimedia, ListaCuentasElinminadas

def admin_BuscarUsuarioUsername(pListMetroUsers,pListaMultimedia,pUsuarioActual, ListaCuentasElinminadas):

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

                pListMetroUsers, pListaMultimedia, ListaCuentasElinminadas = admin_menu_otrousuario(pListMetroUsers, pListaMultimedia, OtroUsuario, pUsuarioActual, ListaCuentasElinminadas)
            else:
                print("* Usuario no encontrado *")
    return pListMetroUsers, pListaMultimedia, ListaCuentasElinminadas


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

def menu_buscar_admin(ListMetroUsers,ListaMultimedia,CadaUsuario, ListaCuentasEliminadas):

    while True:
        menu_buscar = input("Admin ### Menu Buscar ### \n\n1.Username\n2.Por Carrera\n3.Por Departamento\n4.Regresar\n->")
        if menu_buscar == "1":

            ListMetroUsers, ListaMultimedia, ListaCuentasElinminadas = admin_BuscarUsuarioUsername(ListMetroUsers,ListaMultimedia,CadaUsuario, ListaCuentasEliminadas)

        if menu_buscar == "2":
            admin_BuscarUsuarioCarrera(ListMetroUsers)
        if menu_buscar == "3":
            admin_BuscarUserDepartamento(ListMetroUsers)
        if menu_buscar == "4":
            break
    return ListaMultimedia, ListMetroUsers, ListaCuentasElinminadas

def menu_post_buscar_admin(pListaMultimedia,pListMetroUsers,CadaUsuario,ListaPostNumeral,CadaPublicacion, numeral):

    while True:
        menu_post_buscar = input("Admin ### Buscar Post ### Buscar Post\n1.Por User\n2.Por Hashtag\n3.Regresar")

        if menu_post_buscar == "1":
            BuscarPostUser(ListaMultimedia,ListMetroUsers,CadaUsuario)

        if menu_post_buscar =="2":
            BuscarPostNumeral(CadaPublicacion, numeral, ListaMultimedia)

        if menu_post_buscar == "3":
            break
    return ListaMultimedia

"""Admin: Menu principal del usuario ADMIN """
def admin_menu_usuario(ListMetroUsers,ListaMultimedia,UsuarioActual, ListaCuentasElinminadas):
    while True:
        menu_perfil = input("Admin ### Menu Principal ###\n\n1.Buscar Usuario\n2.Buscar Publicaciones\n3.Estadisticas\n4.Salir\n->")

        if menu_perfil == "1":
           ListMetroUsers, ListaMultimedia, ListaCuentasElinminadas = menu_buscar_admin(ListMetroUsers, ListaMultimedia, UsuarioActual, ListaCuentasElinminadas)

        if menu_perfil == "2":
            pass
        if menu_perfil == "3":
            menu_estadisticas(ListaMultimedia, ListMetroUsers, ListaCuentasElinminadas)

        if menu_perfil == "4":
            if cerrar_sesion(UsuarioActual) == True:
                break
    #debe retornar las listas porque pudo modificarlas. Pudo eliminar un usuario, o pudo eliminar publicaciones o comentarios.
    return ListMetroUsers, ListaMultimedia, ListaCuentasElinminadas

################### FIN ADMIN ############################


### MODULO 4 ###


def usuario_publicaciones(pListaMultimedia):
    lista_usuario_pub = []

    for CadaPublicacion in pListaMultimedia:
        if lista_usuario_pub == []:
            lista_usuario_pub.append(CadaPublicacion.usuario)
        else:
            usuario_encontrado = False
            for CadaUsuarioenLista in lista_usuario_pub:
                if CadaUsuarioenLista == CadaPublicacion.usuario:
                    usuario_encontrado = True
            if usuario_encontrado == False:
                lista_usuario_pub.append(CadaPublicacion.usuario)

    return lista_usuario_pub

def usuario_con_mas_publicaciones(pListaMultimedia):
    usuarios = usuario_publicaciones(pListaMultimedia)
    usuario_contador = []
    #Inicializo la lista de usuario que publicaron con 0
    for CadaUsuario in usuarios:
        usuario_contador.append([CadaUsuario, 0])

    for CadaPublicacion in pListaMultimedia:
        usuario = CadaPublicacion.usuario
        #busco en la lista al usuario y le sumo 1 a su contador
        for cadaUserioCont in usuario_contador:
            if cadaUserioCont[0] == usuario:
                cadaUserioCont[1] += 1

    usuarioMax = usuario_contador[0][0]
    MaxPublicaciones = usuario_contador[0][1]

    for cadaUserioCont in usuario_contador:
        if cadaUserioCont[1] > MaxPublicaciones:
            usuarioMax = cadaUserioCont[0]

    return usuarioMax

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
    ListaCuentasElinminadas = []

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
                    ListMetroUsers, ListaMultimedia, ListaCuentasElinminadas = admin_menu_usuario(ListMetroUsers, ListaMultimedia, UsuarioActual, ListaCuentasElinminadas)

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
















