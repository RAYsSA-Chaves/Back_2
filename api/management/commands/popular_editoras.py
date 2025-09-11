import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Editora

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Caminho do arquivo csv
        parser.add_argument("--arquivo", default="population/editoras.csv")
        # Parâmetro para passar ao rodar (apaga todos os registros antes)
        parser.add_argument("--truncate", action="store_true")
        # Parâmetro para passar ao rodar (verifica atualizações em todos os registros existentes)
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *a, **o):
        # Ler o csv
        df = pd.read_csv(o["arquivo"], encoding="utf-8-sig")
        # Normaliza nomes das colunas
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]

        # Se passado ao rodar, apaga todos os registros
        if o["truncate"]:
            Editora.objects.all().delete()

        # Padroniza os dados (remove espaços extras e corrige possíveis caracteres)
        df["editora"] = df["editora"].astype(str).str.strip()
        df["cnpj"] = df["cnpj"].astype(str).str.strip()
        df["endereço"] = df["endereço"].astype(str).str.strip()
        df["telefone"] = df["telefone"].astype(str).str.strip()
        df["email"] = df["email"].astype(str).str.strip()
        df["site"] = df["site"].astype(str).str.strip()

        # Atualiza ou cria registros
        if o["update"]:
            criados = atualizados = 0
            for r in df.itertuples(index=False):
                # Normaliza 'editora' (strip, caso tenha espaços extras)
                editora_nome = r.editora.strip()

                # Usa update_or_create para atualizar se já existir ou criar novo
                _, created = Editora.objects.update_or_create(
                    editora=editora_nome,
                    defaults={
                        "cnpj": r.cnpj,
                        "endereço": r.endereço,
                        "telefone": r.telefone,
                        "email": r.email,
                        "site": r.site
                    }
                )

                criados += int(created)  # SE foi criado
                atualizados += (not created)  # SE foi atualizado

            self.stdout.write(self.style.SUCCESS(f'Criados: {criados} | Atualizados: {atualizados}'))

        else:
            # Apenas cria
            objs = [
                Editora(
                    editora=r.editora, 
                    cnpj=r.cnpj, 
                    endereço=r.endereço, 
                    telefone=r.telefone, 
                    email=r.email, 
                    site=r.site,
                ) for r in df.itertuples(index=False)
            ]

            # Ignora conflitos (não cria registros duplicados)
            Editora.objects.bulk_create(objs, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))