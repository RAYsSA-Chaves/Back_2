from rest_framework import serializers
from .models import Autor

# serializers transforma a tabela em json

class AutorSerializers(serializers.ModelSerializer):
    class Meta: # classe obrigatória para pegar os metadados
        model = Autor
        fields = '__all__' # seleciona todos os campos, em vez de escrever um por um
