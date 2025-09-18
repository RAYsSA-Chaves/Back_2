import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Autor

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Caminho do arquivo csv
        parser.add_argument("--arquivo", default="population/livros.csv")
        # Parâmetro para passar ao rodar (apaga todo os registros antes)
        parser.add_argument("--truncate", action="store_true")
        # Pârametro para passar ao rodar (verifica atualizações em todos os registros exsitentes)
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *a, **o):
        # Ler o csv
        df = pd.read_csv(o["arquivo"], encoding="utf-8-sig")
        # Normaliza nomes das colunas
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]

        # Se passado ao rodar, apaga todos os registros
        if o["truncate"]:
            Autor.objects.all().delete()

        # Padroniza os dados
        df["nome"] = df["nome"].astype(str).str.strip()
        df["sobrenome"] = df["sobrenome"].astype(str).str.strip()
        df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors="coerce", format="%Y-%m-%d").dt.date
        df["nacao"] = df.get("nacao", "").astype(str).str.strip().str.capitalize().replace({"": None}) 
        # get = tenta pegar a coluna nação ou usa uma vazia; replace = substitui strings vazias por None salvar Null no banco

        # Consulta onde nome E sobrenome são vazios e gera um novo df SEM aquela linha
        df = df.query("nome !='' and sobrenome != '' ") 

        # Exclui a linha que não possuir data de nascimento
        df = df.dropna(subset=["data_nascimento"]) 

        # Atualiza ou cria registros
        if o["update"]:
            criados = atualizados = 0
            # intertuple = tupla; por padrão ela vem com index de cada elemento criado
            for r in df.itertuples(index=False):
                _, created = Autor.objects.update_or_create(
                    # Parâmetros de busca para localizar se o registro já existe no banco
                    nome=r.nome, sobrenome=r.sobrenome, data_nascimento = r.data_nascimento,
                    # Valores que podem ser atualizados se o registro existir ou atribuídos se for criado um novo
                    defaults={"nacao": r.nacao}
                )

                criados += int(created) # SE foi criado
                atualizados += (not created) # SE foi atualizado

            # print
            self.stdout.write(self.style.SUCCESS(f'Criados: {criados} | Atualizados: {atualizados}'))

        else:
            # Apenas cria 
            objs = [Autor(
                nome=r.nome, sobrenome=r.sobrenome, data_nascimento = r.data_nascimento, nacao=r.nacao
            ) for r in df.itertuples(index=False)]
            
            Autor.objects.bulk_create(objs, ignore_conflicts=True) # ignora/pula duplicados

            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))