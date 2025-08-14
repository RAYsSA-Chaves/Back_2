from django.urls import path
from .views import *

urlpatterns = [
    path('autores', AutoresView.as_view()),
    path('crud/<int:pk>', AutoresCrud.as_view()),
    path('authors', listar_autores)
]

# urlpatterns = paleta de end points