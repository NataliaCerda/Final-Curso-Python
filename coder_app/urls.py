from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="inicio"),
    path('acerca_de/', acerca_de, name="acerca_de"),
    
    #URLS de la App
    path('profesores/', profesores, name="profesores"),
    path('estudiantes/', estudiantes, name="estudiantes"),
    path('cursos/', cursos, name="cursos"),
    #path('base/', base),
    path('crear-curso/', crear_curso, name="crear-curso"),
    #path('buscar_comision/', buscar_comision, name="buscar_comision"),
    path('crear-profesor/', crear_profesor, name="crear-profesor"),
    path('crear-estudiante/',crear_estudiante, name="crear-estudiante"),
    path('eliminar_estudiante/<estudiante_id>', eliminar_estudiante, name="eliminar_estudiante" ),
    path('modificar_estudiante/<estudiante_id>', modificar_estudiante, name="modificar_estudiante"),
    
    path('profesores/list', ProfesoresList.as_view(), name="profesores_list"),
    path(r'^(?P<pk>\d+)$', ProfesoresDetail.as_view(), name="profesores_detail"), # pk --> primary key para mostrar los detalles
    path(r'^nuevo$', ProfesoresCreate.as_view(), name="profesores_create"),
    path(r'^editar/(?P<pk>\d+)$', ProfesoresUpdate.as_view(), name="profesores_update"),
    path(r'^eliminar/(?P<pk>\d+)$', ProfesoresDelete.as_view(), name="profesores_delete"),
    
    path('login', login_request, name="login"),
    path('register', register_request, name="register"),
    path('logout', logout_request, name="logout"),
    path('editar_perfil', editar_perfil, name="editar_perfil"),
    
    path('detalle_curso/<curso_id>', detalle_curso, name="detalle_curso"),
    path('editar_curso/<curso_id>', editar_curso, name="editar_curso"),
    
    path('detalle_curso/agregar_comentario_curso/<id>', agregar_comentario_curso, name='agregar_comentario_curso'),   
   
 ]