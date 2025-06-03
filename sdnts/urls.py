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
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    
    path('domiciliario_envios/', views.domiciliario_envios, name='domiciliario_envios'),
      # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # Gestión de Ventas
    path('ventas/', views.ventas, name='ventas'),
    # Gestión de Producción
    path('produccion/', views.produccion, name='produccion'),
    # Gestión de Envíos
    path('envios/', views.envios, name='envios'),
    # Gestión de Proveedores
    path('proveedores/', views.proveedores, name='proveedores'),
    # Gestión de Inventario
    path('entradas/', views.entradas, name='entradas'),
    path('salidas/', views.salidas, name='salidas'),
    # Gestión de Categorías
    path('categorias/', views.categorias, name='categorias'),
    # Gestión de Correos (comentada hasta crear el modelo)
     path('correos/', views.correos, name='correos'),
    # Carga de Datos
    path('cargar-datos/', views.cargarDatos, name='cargar_datos'),
    # Vistas adicionales
    path('insumos/', views.insumos, name='insumos'),
    path('productos/', views.productos, name='productos'),
    path('clientes/', views.clientes, name='clientes'),
    path('domiciliarios/', views.domiciliarios, name='domiciliarios'),
    
    path('reporte-usuarios-pdf/', views.reporte_usuarios_pdf, name='reporte_usuarios_pdf'),
    path('guardar/', views.guardar_usuario, name='guardar_usuario'),
    path('actualizar-usuario/', views.actualizar_usuario, name='actualizar_usuario'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('reporte-usuarios-excel/', views.reporte_usuarios_excel, name='reporte_usuarios_excel'),

]
 