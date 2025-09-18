from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # GET / POST
    path('autores', AutoresView.as_view()),
    path('authors', listar_autores),
    path('editoras', EditorasView.as_view()),
    path('livros', LivrosView.as_view()),
    path('buscar/', AutoresView.as_view()),

    # UPDATE / DELETE
    path('autores/<int:pk>', AutoresCrud.as_view()),
    path('editoras/<int:pk>', EditorasCrud.as_view()),
    path('livros/<int:pk>', LivrosCrud.as_view()),

    # TOKEN
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# urlpatterns = paleta de end points