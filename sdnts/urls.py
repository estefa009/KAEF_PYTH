"""
URL configuration for kaef_final project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.http import HttpResponse
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
 path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contactanos/', views.contactanos, name='contactanos'),
    
    path('login/', views.login, name='login'),
    path('auth/registrar/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    
    path('nav/index/', views.nav_index, name='nav_index'),
    path('nav/admin/', views.nav_admin, name='nav_admin'),
    path('nav/user/', views.nav_user, name='nav_user'),
    
    path('recuperar/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('recuperar/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('vistacliente/', views.vistacliente, name='vistacliente'),
    path('catalogocliente/', views.catalogocliente, name='catalogocliente'),
    path('nosotroscliente/', views.nosotroscliente, name='nosotroscliente'),
    path('contactanoscliente/', views.contactanoscliente, name='contactanoscliente'),
    path('perfilcliente/', views.perfilcliente, name='perfilcliente'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),

    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),
     #Domiciliario
    path('mis_domicilios/', views.mis_domicilios, name='mis_domicilios'),
    path('historial_envios/', views.historial_envios, name='historial_envios'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('perfildomi/', views.perfildomi, name='perfildomi'),
    path('editar_perfildomi/', views.editar_perfildomi, name='editar_perfildomi'),

    #administrador
    path('cargarDatos/', views.cargarDatos, name='cargarDatos'),
    path('categorias_admin/', views.categorias_admin, name='categorias_admin'),
    path('correos_admin/', views.correos_admin, name='correos_admin'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('entradas_admin/', views.entradas_admin, name='entradas_admin'),
    path('envios_admin/', views.envios_admin, name='envios_admin'),
    path('insumos_admin/', views.insumos_admin, name='insumos_admin'),
    path('perfil_admin/', views.perfil_admin, name='perfil_admin'),
    path('editarperfil_admin/', views.editarperfil_admin, name='editarperfil_admin'),
    path('usuario/editar/<int:cod_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('agregar_usuario/', views.agregar_usuario, name='agregar_usuario'),

    path('eliminar_usuario/<int:cod_usuario>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('produccion_admin/', views.produccion_admin, name='produccion_admin'),
    path('proveedores_admin/', views.proveedores_admin, name='proveedores_admin'),
    path('salidas_admin/', views.salidas_admin, name='salidas_admin'),
    
    #Ventas
    
    path('ventas_admin/', views.ventas_admin, name='ventas_admin'),
    path('ventas/completa/agregar/', views.agregar_venta_completa, name='agregar_venta_completa'),

    path('reporte-usuarios-pdf/', views.reporte_usuarios_pdf, name='reporte_usuarios_pdf'),
    path('guardar/', views.guardar_usuario, name='guardar_usuario'),
    path('actualizar-usuario/', views.actualizar_usuario, name='actualizar_usuario'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('reporte-usuarios-excel/', views.reporte_usuarios_excel, name='reporte_usuarios_excel'),
    
    

# ...existing code...
    path('procesar_compra/', views.procesar_compra, name='procesar_compra'),
# ...existing code...
]
 