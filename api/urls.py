from django.urls import path
from .views import *

urlpatterns = [
    # GET / POST
    path('autores', AutoresView.as_view()),
    path('authors', listar_autores),
    path('editoras', EditorasView.as_view()),
    path('livros', LivrosView.as_view()),

    # UPDATE / DELETE
    path('autores/<int:pk>', AutoresCrud.as_view()),
    path('editoras/<int:pk>', EditorasCrud.as_view()),
    path('livros/<int:pk>', LivrosCrud.as_view()),
]

# urlpatterns = paleta de end points