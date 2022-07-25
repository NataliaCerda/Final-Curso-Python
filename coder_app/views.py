from ast import If
from distutils.log import error
from logging import info
from django import views
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse

from .models import Curso, Profesor, Estudiante, Avatar
from .forms import CommentForm, EditarCurso, NuevoCurso, ProfesorNuevo, EstudianteNuevo, UserEditForm, UserRegisterForm
from django.db.models import Q

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required

from django.core.paginator import Paginator

# Create your views here.

def index(request):
    
    if request.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(usuario=request.user)
            url = avatar.imagen.url
        except:
            url = "/media/avatar/generica.png"
            
        return render(request,"coder_app/index.html",{"url":url})
    
    return render(request,"coder_app/index.html",{})

def acerca_de(request):
    
    return render(request,"coder_app/acerca_de.html",{})
    
@staff_member_required
def crear_curso(request):
    
    if request.method == "POST":

        formulario = NuevoCurso(request.POST, request.FILES)

        if formulario.is_valid():

            info_curso = formulario.cleaned_data
            
            #curso = Curso(nombre=info_curso["nombre"], comision=info_curso["comision"])
            curso = Curso(nombre=info_curso["nombre"], comision=info_curso["comision"], descripcion=info_curso["descripcion"])
            curso.save()
            
            if info_curso['imagen'] != None:
                curso.imagen = info_curso['imagen']
                curso.save()
            
            return redirect("cursos")
        else:
            return render(request,"coder_app/formulario_curso.html",{"form":formulario})
    
    else: #GET y otros
    
        formularioVacio = NuevoCurso()
        
        return render(request,"coder_app/formulario_curso.html",{"form":formularioVacio})
    
@login_required
def profesores(request):
    
    profesores = Profesor.objects.all()
    
    return render(request,"coder_app/profesores.html",{"profesores":profesores})

@staff_member_required
def crear_profesor(request):
    
    if request.method == "POST":

        formulario = ProfesorNuevo(request.POST)

        if formulario.is_valid():

            info_profesor = formulario.cleaned_data
            
            profesor = Profesor(nombre=info_profesor["nombre"], apellido=info_profesor["apellido"], email=info_profesor["email"], profesion=info_profesor["profesion"] )

            profesor.save()
            
            return redirect("profesores")
        else:
            return render(request,"coder_app/formulario_profesores.html",{"form":formulario})
    
    else: #GET y otros
    
        formularioVacio = ProfesorNuevo()
        
        return render(request,"coder_app/formulario_profesores.html",{"form":formularioVacio})
    
@login_required
def estudiantes(request):
    
    estudiantes = Estudiante.objects.all()
    
    return render(request,"coder_app/estudiantes.html",{"estudiantes":estudiantes})

@staff_member_required
def eliminar_estudiante(request,estudiante_id):
    
    estudiante = estudiantes.objects.get(id=estudiante_id)
    estudiante.delete()
    
    return redirect("estudiantes")

@staff_member_required
def crear_estudiante(request):
    
    if request.method == "POST":

        formulario = EstudianteNuevo(request.POST)

        if formulario.is_valid():

            info_estudiante = formulario.cleaned_data
            
            estudiante = Estudiante(nombre=info_estudiante["nombre"], apellido=info_estudiante["apellido"], email=info_estudiante["email"] )

            estudiante.save()
            
            return redirect("estudiantes")
        else:
            return render(request,"coder_app/formulario_estudiantes.html",{"form":formulario})
    
    else: #GET y otros
    
        formularioVacio = EstudianteNuevo()
        
        return render(request,"coder_app/formulario_estudiantes.html",{"form":formularioVacio})

@staff_member_required
def modificar_estudiante(request,estudiante_id):
    
    estudiante = Estudiante.objects.get(id=estudiante_id)
    
    if request.method =="POST":
        
        formulario = EstudianteNuevo(request.POST)
        
        if formulario.is_valid():
            
            info_estudiante = formulario.cleaned_data
            
            estudiante.nombre = info_estudiante["nombre"]
            estudiante.apellido = info_estudiante["apellido"]
            estudiante.email = info_estudiante["email"]
            
            estudiante.save()
            
            return redirect("estudiantes")
                
    formulario = EstudianteNuevo(initial={"nombre":estudiante.nombre, "apellido":estudiante.apellido, "email":estudiante.email})
    
    return render(request,"coder_app/formulario_estudiantes.html",{"form":formulario})

@login_required
def cursos(request):
   
    if request.method == "POST":

        search = request.POST["search"]

        if search != "":
            cursos = Curso.objects.filter( Q(nombre__icontains=search) | Q(comision__icontains=search) ).values()

            return render(request,"coder_app/cursos.html",{"cursos":cursos, "search":True, "busqueda":search})
    
    cursos = Curso.objects.all()

    return render(request,"coder_app/cursos.html",{"cursos":cursos, "search":False})

class ProfesoresList(LoginRequiredMixin,ListView):
    model = Profesor
    template_name = "coder_app/profesores_list.html"

class ProfesoresDetail(LoginRequiredMixin,DetailView):
    model = Profesor
    template_name = "coder_app/profesores_detail.html"
    
class ProfesoresCreate(LoginRequiredMixin,CreateView):
    model = Profesor
    success_url = "/coder_app/profesores/list"
    fields = ["nombre", "apellido", "email", "profesion"]

class ProfesoresDelete(LoginRequiredMixin,DeleteView):
    model = Profesor
    success_url = "/coder_app/profesores/list"
    
class ProfesoresUpdate(LoginRequiredMixin,UpdateView):
    model = Profesor
    success_url = "/coder_app/profesores/list"
    fields = ["nombre", "apellido", "email", "profesion"]

def login_request(request):
    
    if request.method == "POST":
        
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("inicio")                
            else:
                return redirect("login")
        else:
            return redirect("login")
            
    form = AuthenticationForm()
    
    return render(request, "coder_app/login.html",{"form":form})

def register_request(request):
    
    if request.method == "POST":
        
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            form.save()
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("inicio")                
            else:
                return redirect("login")

        return render(request, "coder_app/register.html", {"form":form})
    
    form = UserRegisterForm()
    
    return render(request, "coder_app/register.html",{"form":form})

def logout_request(request):
    logout(request)
    return redirect("inicio")

@login_required
def editar_perfil(request):
    
    user = request.user # usuario logueado
    try:
        avatar = Avatar.objects.get(usuario=user)
    except:
        avatar = Avatar(usuario=user)
        avatar.save()
    
    if request.method == "POST":
        
        form = UserEditForm(request.POST, request.FILES) # cargamos datos completados
        
        if form.is_valid():
            
            info = form.cleaned_data
            user.email = info["email"]
            user.first_name = info["first_name"]
            user.last_name = info["last_name"]
            user.save()
            
            if info['imagen'] != None:
                avatar.imagen = info['imagen']
                avatar.save()
            
            return redirect("inicio")
        else:
            return render(request, "coder_app/editar_perfil.html",{"form":form})
    
    else:
        
        form = UserEditForm(initial={"email":user.email, "firts_name":user.first_name, "last_name":user.last_name, "imagen":avatar.imagen})
    
    return render(request, "coder_app/editar_perfil.html", {"form":form})

@login_required
def detalle_curso(request, curso_id):
    
    curso = Curso.objects.get(id=curso_id)
    
    return render(request,"coder_app/detalle_curso.html",{"curso":curso})
    
@staff_member_required
def editar_curso(request, curso_id):

    curso = Curso.objects.get(id=curso_id)
        
    if request.method =="POST":
        
        formulario = EditarCurso(request.POST, request.FILES)
        
        if formulario.is_valid():
            
            info_curso = formulario.cleaned_data
            
            curso.nombre = info_curso["nombre"]
            curso.comision = info_curso["comision"]
            curso.descripcion = info_curso["descripcion"]
            curso.save()
            
            if info_curso['imagen'] != None:
                curso.imagen = info_curso['imagen']
                curso.save()
                
            return redirect("cursos")
        else:
            return render(request, "coder_app/editar_curso.html",{"form":formulario})
    else:
                    
        formulario = EditarCurso(initial={"nombre":curso.nombre, "comision":curso.comision, "descripcion":curso.descripcion,"imagen":curso.imagen})
    
    return render(request,"coder_app/editar_curso.html",{"form":formulario})

def listing(request):
    curso_list = Curso.objects.all()
    paginator = Paginator(curso_list, 3) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "coder_app/cursos.html", {'page_obj': page_obj})

def agregar_comentario_curso(request, id):
    
    curso = get_object_or_404(Curso, id=id)
    
    if request.method == "POST":
        
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.curso = curso
            comentario.save()
            return redirect('detalle_curso', curso.id)
    else:
        
        form = CommentForm()
        
    return render(request, 'coder_app/agregar_comentario_curso.html', {'form': form})

