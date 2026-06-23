from django.shortcuts import render

def prestamos_home(request):
    mensaje = "Reglas generales de los préstamos: máximo 3 libros por usuario, duración 7 días, devolver en buen estado."
    return render(request, 'prestamos/home.html', {"mensaje": mensaje})


def prestamos_hoy(request):
    libros_hoy = [
        "Cien años de soledad - Gabriel García Márquez",
        "El Principito - Antoine de Saint-Exupéry",
        "1984 - George Orwell",
    ]
    return render(request, 'prestamos/hoy.html', {"libros": libros_hoy})
