from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)
    data_nascimento = models.DateField(null = True, blank = True)
    nacao = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
class Editora(models.Model):
    editora = models.CharField(max_length=100, unique=True)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    endereço = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    site = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.editora

class Livro(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100, null=True, blank=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=50)
    descricao = models.TextField()
    paginas = models.IntegerField()
    ano = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disponivel = models.BooleanField(default=True)
    dimensoes = models.CharField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    idioma = models.CharField(default="Português")


# models = características da tabela
# Model = a tabela em si
# models.Charfield = campo de caracteres
# null true - valor será nulo no banco, caso o campo fique em branco no formulário
# blank = permite deixar o campo branco no formulário
# TextField não tem limite de caracteres
# unique = não pode ter outro igual na tabela
