from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)
    data_nascimento = models.DateField(null = True, blank = True)
    nacao = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"



# models = características da tabela
# Model = a tabela em si
# models.Charfield = campo de caractere
# null true - valor será nulo no banco, caso o campo fique em branco no formulário
# blank = permite deixar o campo branco no formulário
# TextField não tem limite de caracteres
