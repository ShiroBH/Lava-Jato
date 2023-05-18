from django.db import models

# Create your models here.
class Dados(models.Model):
    cpf=models.CharField(primary_key=True,max_length=11)
    email=models.EmailField(max_length=50)
    DataN=models.DateField(max_length=20)
    nome=models.CharField(max_length=50)
    cargo=models.CharField(max_length=35)
    foto=models.ImageField(upload_to="img/%y")

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nome, self.cargo)