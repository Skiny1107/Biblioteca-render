from django.shortcuts import render

def usuarios_home(request):
    mensaje = "Para ser usuario de la biblioteca debe registrarse con su identificación oficial."
    return render(request, 'usuarios/home.html', {"mensaje": mensaje})

def usuarios_detalle(request, id_usuario):
    # Datos simulados
    usuario = {
        "111": {"nombre": "Alex Quemba", "correo": "alexlopez@example.com", "membresia": "Activa"},
    }

    info = usuario.get(str(id_usuario), {"nombre": "No encontrado", "correo": "-", "membresia": "-"})

    return render(request, 'usuarios/detalle.html', {"usuario": info, "id": id_usuario})
