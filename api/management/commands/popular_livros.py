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
        df = pd.read_csv(o["arquivo"], encoding="utf-8-sig")
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]

        if o["truncate"]:
            Livro.objects.all().delete()

        df["titulo"] = df["titulo"].astype(str).str.strip()
        df["subtitulo"] = df["subtitulo"].astype(str).str.strip()
        df["isbn"] = df["isbn"].astype(str).str.strip()
        df["descricao"] = df["descricao"].astype(str).str.strip()
        df["idioma"] = df["idioma"].astype(str).str.strip()
        df["ano"] = pd.to_datetime(df["ano"], errors="coerce", format="%Y-%m-%d").dt.year
        df["paginas"] = df["paginas"].astype(int)
        df["preco"] = df["preco"].astype(float)
        df["estoque"] = df["estoque"].astype(int)
        df["desconto"] = df["desconto"].astype(float)
        df["disponivel"] = df["disponivel"].astype(bool)
        df["dimensoes"] = df["dimensoes"].astype(str).str.strip().replace({"": "Desconhecido"})
        df["peso"] = df["peso"].astype(str).str.strip().replace({"": "Desconhecido"})

        # Buscar os autores e editoras no banco
        autores_busca = {autor.nome.strip().lower(): autor.id for autor in Autor.objects.all()}
        editoras_busca = {editora.nome.strip().lower(): editora.id for editora in Editora.objects.all()}

        # Mapear IDs
        df["autor_id"] = df["autor"].str.strip().str.lower().map(autores_busca)
        df["editora_id"] = df["editora"].str.strip().str.lower().map(editoras_busca)

        df = df.dropna(subset=["titulo", "isbn", "autor", "editora"])
        df = df.query("preco >= 0")

        if o["update"]:
            criados = atualizados = 0
            for r in df.itertuples(index=False):
                _, created = Livro.objects.update_or_create(
                    titulo=r.titulo, subtitulo=r.subtitulo, isbn=r.isbn, descricao=r.descricao, paginas=r.paginas, ano=r.ano, preco=r.preco, estoque=r.estoque, desconto=r.desconto, disponivel=r.disponivel, dimensoes=r.dismensoes, peso=r.peso, idioma=r.idioma, 
                    autor=r.autor_id, 
                    editora=r.editora_id,
                )

                criados += int(created)
                atualizados += (not created)
            
            self.stdout.write(self.style.SUCCESS(f'Criados: {criados} | Atualizados: {atualizados}'))

        else:
            objs = [Livro(
                titulo=r.titulo, subtitulo=r.subtitulo, isbn=r.isbn, descricao=r.descricao, paginas=r.paginas, ano=r.ano, preco=r.preco, estoque=r.estoque, desconto=r.desconto, disponivel=r.disponivel, dimensoes=r.dismensoes, peso=r.peso, idioma=r.idioma, 
                autor=r.autor_id, 
                editora=r.editora_id,
            ) for r in df.itertuples(index=False)]
            
            Livro.objects.bulk_create(objs, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))