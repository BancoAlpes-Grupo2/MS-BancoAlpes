""" from django.urls import path, include
from . import views

urlpatterns = [
    #cambios home page crear
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('cliente/<int:pk>', views.customer_cliente, name='cliente' ),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente' ),
    #path('crm/', include('crm.urls')),  # Esto asigna la ruta '/crm/' a tu aplicación CRM
    path('api/cliente/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente-detail'),  # URL para obtener detalles del cliente

]
 """
from django.urls import path
from . import views

urlpatterns = [
    #cambiar path y funcion
    path('createuser/', views.createUserAuthTemplate, name='create_user'),
    path('getusers/', views.getUsersTemplate, name='get_users'),  # Ajustado para que esta sea la ruta raíz de /users/
    path('userinformation/<int:userId>/', views.getUserTemplate, name='get_user'),
    
    #will
    path('', views.getUsers),
    path('create/', views.createUser),
    path('<int:userId>/', views.getUser)
]
