from django.db import models
from django.core.validators import MinLengthValidator # Importa o validador de tamanho mínimo

class Estudante(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=False, blank=False, unique=True)
    data_nascimento = models.DateField(null=False, blank=False)
    celular = models.CharField(max_length=14)
    
    def __str__(self):
        return self.nome
    
class Curso(models.Model):
    NIVEL = [
        ('B', 'Básico'),
        ('I', 'Intermediário'),
        ('A', 'Avançado')
    ]
    
    codigo = models.CharField(max_length=10, null=False, blank=False, unique=True, validators=[MinLengthValidator(3)]) # O MinLengthValidator é um validador de tamanho mínimo, que recebe como parâmetro o tamanho mínimo que o campo deve ter
    descricao = models.TextField(null=False, blank=False)
    nivel = models.CharField(max_length=1, choices=NIVEL, default='B', null=False, blank=False)
    
    def __str__(self):
        return self.codigo
    
class Matricula(models.Model):
    PERIODO = [
        ('M', 'Matutino'),
        ('V', 'Vespertino'),
        ('N', 'Noturno'),
    ]
    
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=1, blank=False, null=False, choices=PERIODO, default='M')
    
    def __str__(self):
        return 'Matrícula de: ' + self.estudante.nome + ' no curso ' + self.curso.codigo