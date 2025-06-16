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
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar-carrito/', views.actualizar_carrito, name='actualizar_carrito'),
     #Domiciliario
    path('mis_domicilios/', views.mis_domicilios, name='mis_domicilios'),
    path('historial_envios/', views.historial_envios, name='historial_envios'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('perfildomi/', views.perfildomi, name='perfildomi'),
    path('editar_perfildomi/', views.editar_perfildomi, name='editar_perfildomi'),

    #administrador
    path('cargar-datos/', views.cargar_datos_view, name='cargarDatos'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('perfil_admin/', views.perfil_admin, name='perfil_admin'),
    path('editarperfil_admin/', views.editarperfil_admin, name='editarperfil_admin'),
    path('usuario/editar/<int:cod_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('agregar_usuario/', views.agregar_usuario, name='agregar_usuario'),

    path('eliminar_usuario/<int:cod_usuario>/', views.eliminar_usuario, name='eliminar_usuario'),



    #produccion_admin
    path('produccion_admin/', views.produccion_admin, name='produccion_admin'),
    path('produccion/editar/<int:cod_produccion>/', views.editar_produccion, name='editar_produccion'),
    path('produccion/estado/<int:cod_produccion>/', views.cambiar_estado_produccion, name='cambiar_estado_produccion'),
    path('produccion/asignar-envio/<int:cod_produccion>/', views.asignar_envio_produccion, name='asignar_envio_produccion'),
    path('produccion/eliminar/<int:cod_produccion>/', views.eliminar_produccion, name='eliminar_produccion'),

    
    
    #Ventas
    
    path('ventas_admin/', views.ventas_admin, name='ventas_admin'),
    path('ventas/completa/agregar/', views.agregar_venta_completa, name='agregar_venta_completa'),
    path('ventas/<int:venta_id>/detalle/', views.detalle_ventas, name='detalle_ventas'),
    path('ventas/<int:venta_id>/editar_estado/', views.editar_estado_venta, name='editar_estado_venta'),

    #Envios del administrador
    path('envios/envios_admin/', views.envios_admin, name='envios_admin'),
    path('envios/envios/crear/', views.crear_envio, name='crear_envio'),
    path('envios/envios/editar/<int:pk>/', views.editar_envio, name='editar_envio'),
    path('envios/envios/eliminar/<int:pk>/', views.eliminar_envio, name='eliminar_envio'),
    
    #proveedores
    path('proveedores_admin/', views.proveedores_admin, name='proveedores_admin'),
    path('proveedores/agregar_proveedores/', views.agregar_proveedores, name='agregar_proveedores'),
    path('proveedores/editar_proveedores/<int:cod_proveedor>/', views.editar_proveedores, name='editar_proveedores'),
    path('proveedores/eliminar_proveedores/<int:cod_proveedor>/', views.eliminar_proveedores, name='eliminar_proveedores'),
    #entradas
    path('entradas_admin/', views.entradas_admin, name='entradas_admin'),
    path('entradas/agregar/', views.agregar_entradas, name='agregar_entradas'),
    path('entradas/editar/<int:cod_entrada>/', views.editar_entrada, name='editar_entrada'),
    path('entradas/eliminar/<int:cod_entrada>/', views.eliminar_entrada, name='eliminar_entrada'),
    #categorias
    path('categorias_admin/', views.categorias_admin, name='categorias_admin'),
    path('categorias/eliminar/<int:cod_categoria>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('categorias/agregar_categoria', views.agregar_categoria, name='agregar_categoria'),

    #insumos
    path('insumos_admin/', views.insumos_admin, name='insumos_admin'),
    path('insumos/agregar/', views.agregar_insumo, name='agregar_insumo'),
    path('insumos/editar/<int:cod_insumo>/', views.editar_insumo, name='editar_insumo'),
    path('insumos/eliminar/<int:cod_insumo>/', views.eliminar_insumo, name='eliminar_insumo'),
  
    #salidas
    path('salidas_admin/', views.salidas_admin, name='salidas_admin'),
    path('salidas/eliminar/<int:cod_salida>/', views.eliminar_salida, name='eliminar_salida'),
    path('salidas/agregar/', views.agregar_salida, name='agregar_salida'),

    #correo
    path('correos_admin/', views.correos_admin, name='correos_admin'),
    path('correo/<int:cod_correo>/', views.ver_correo, name='ver_correo'),
    path('correos/enviar_correos_masivos/', views.enviar_correos_masivos, name='enviar_correos_masivos'),
    #productos
    path('productos_admin/', views.productos_admin, name='productos_admin'),
    path('productos_admin/<int:cod_producto>/cambiar_estado/', views.cambiar_estado_producto, name='cambiar_estado_producto'),
    path('productos_admin/<int:cod_producto>/editar_receta/', views.editar_receta_producto, name='editar_receta_producto'),
    path('productos_admin/<int:cod_producto>/ver_receta/', views.ver_receta_producto, name='ver_receta_producto'),
    path('productos_admin/<int:cod_producto>/generar_receta_base/', views.generar_receta_base, name='generar_receta_base'),


    
    # Reportes de inventario
    path('reporte_insumo/', views.reporte_insumo, name='reporte_insumo'),
    path('reporte_entradas/', views.reporte_entradas, name='reporte_entradas'),
    path('reporte_salidas/', views.reporte_salidas, name='reporte_salidas'),
    
    # Reportes de producción
    path('produccion/', views.reporte_produccion, name='reporte_produccion'),
    path('categorias/', views.reporte_categorias, name='reporte_categorias'),

    # Reportes de ventas y envíos
    path('ventas/', views.reporte_ventas, name='reporte_ventas'),
    path('envios/', views.reporte_envios, name='reporte_envios'),
    
    # Reportes de proveedores
    path('proveedores/', views.reporte_proveedores, name='reporte_proveedores'),
    
    # Reporte de usuarios
    path('usuarios/', views.reporte_usuarios_pdf, name='usuarios_pdf'),

    path('notificaciones/', views.notificaciones_admin, name='notificaciones_admin'),

    
    # ...
]
    
    # ...


