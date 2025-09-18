import django_filters as df
import django.db.models as Q
from .models import Autor

class AutorFilter(df.FilterSet):
    nome = df.CharFilter(method='filter_nome')
    nacionalidade = df.CharFilter(method='nacionalidade', lookup_expr='iexact')

    def filter_nome(self, qs, name, value: str):
        if not value:
            return qs
        return qs.filter(Q(nome__icontains=value) | Q(sobrenome__icontains=value))
    
    def nacao(self, qs, name, value: str):
        if not value:
            return qs
        return qs.filter(Q(nacao_icontains=value))

    class Meta:
        model = Autor
        fields = []