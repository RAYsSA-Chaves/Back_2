import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Livro, Autor, Editora

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--arquivo", default="population/livros.csv")
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *a, **o):
        # Ler o csv
        df = pd.read_csv(o["arquivo"], encoding="utf-8-sig")
        # Normaliza nomes das colunas
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]

        # Se passado ao rodar, apaga todos os registros
        if o["truncate"]:
            Livro.objects.all().delete()

        # Padroniza os dados
        df["titulo"] = df["titulo"].astype(str).str.strip()
        df["subtitulo"] = df["subtitulo"].astype(str).str.strip()
        df["isbn"] = df["isbn"].astype(str).str.strip()
        df["descricao"] = df["descricao"].astype(str).str.strip()
        df["idioma"] = df["idioma"].astype(str).str.strip()
        df["ano"] = df["ano"].astype(int)
        df["paginas"] = df["paginas"].astype(int)
        df["preco"] = df["preco"].astype(float)
        df["estoque"] = df["estoque"].astype(int)
        df["desconto"] = df["desconto"].astype(float)
        df["disponivel"] = df["disponivel"].astype(bool)
        df["dimensoes"] = df["dimensoes"].astype(str).str.strip().replace({"": "Desconhecido"})
        df["peso"] = df["peso"].astype(str).str.strip().replace({"": "Desconhecido"})

        # Pegar autores existentes na tabela
        autores_banco = Autor.objects.all()
        autores_existentes = []
        for autor in autores_banco:
            autores_existentes.append({"nome_completo": autor.nome + " " + autor.sobrenome, "id": autor.id})

        # Pegar editoras existentes na tabela
        editoras_banco = Editora.objects.all()
        editoras_existentes = []
        for editora in editoras_banco:
            editoras_existentes.append({"editora": editora.editora, "id": editora.id})

        # Guardar os IDs de autor e editora
        autores_ids = []
        editoras_ids = []

        for i in range(len(df)):
            # Verifica se autor existe
            autor_obj = None
            for a in autores_banco:
                if (a.nome + " " + a.sobrenome).lower() == df.loc[i, "autor"].strip().lower():
                    autor_obj = a
                    break
            autores_ids.append(autor_obj)

            # Verifica se editora existe
            editora_obj = None
            for e in editoras_banco:
                if e.editora.lower() == df.loc[i, "editora"].strip().lower():
                    editora_obj = e
                    break
            # Se não existe, cria na tabela de editoras
            if editora_obj is None:
                editora_obj = Editora.objects.create(editora=df.loc[i, "editora"].strip())
                editoras_banco = list(editoras_banco) + [editora_obj]  # adiciona à lista

            editoras_ids.append(editora_obj)

        # Pega os IDs automaticamente (porque está sendo passado como uma ForeignKey) e adiciona ao DataFrame
        df["autor_id"] = autores_ids
        df["editora_id"] = editoras_ids

        # Excluir linhas que não tiverem titulo, isbn, autor e editora
        df = df.dropna(subset=["titulo", "isbn", "autor_id", "editora_id"])
        # Excluir linhas que tiverem preço inválido
        df = df.query("preco >= 0")

        # Atualiza ou cria registros
        if o["update"]:
            criados = atualizados = 0
            for r in df.itertuples(index=False):
                _, created = Livro.objects.update_or_create(
                    # Parâmetros de busca para localizar se o registro já existe no banco
                    titulo=r.titulo, subtitulo=r.subtitulo, isbn=r.isbn, descricao=r.descricao, paginas=r.paginas, ano=r.ano, preco=r.preco, estoque=r.estoque, desconto=r.desconto, disponivel=r.disponivel, dimensoes=r.dimensoes, peso=r.peso, idioma=r.idioma, 
                    autor=r.autor_id, 
                    editora=r.editora_id,

                    defaults={"preco": r.preco, "estoque":r.estoque, "desconto":r.desconto, "disponivel":r.disponivel}
                )

                criados += int(created)
                atualizados += (not created)
            
            self.stdout.write(self.style.SUCCESS(f'Criados: {criados} | Atualizados: {atualizados}'))

        else:
            objs = [Livro(
                titulo=r.titulo, subtitulo=r.subtitulo, isbn=r.isbn, descricao=r.descricao, paginas=r.paginas, ano=r.ano, preco=r.preco, estoque=r.estoque, desconto=r.desconto, disponivel=r.disponivel, dimensoes=r.dimensoes, peso=r.peso, idioma=r.idioma, 
                autor=r.autor_id, 
                editora=r.editora_id,
            ) for r in df.itertuples(index=False)]
            
            Livro.objects.bulk_create(objs, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))