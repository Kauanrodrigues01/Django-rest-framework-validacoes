from escola.models import Estudante, Curso, Matricula
from escola.serializers import EstudanteSerializer, CursoSerializer, MatriculaSerializer, ListaMatriculasCursoSerializer, ListaMatriculasEstudanteSerializer, EstudanteSerializerV2

from rest_framework import viewsets, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# IsAdminUser: Só quem é admin pode acessar
# IsAuthenticatedOrReadOnly: Qualquer usuário autenticado pode acessar para leitura(GET), mas só quem é admin pode acessar para(POST, PUT, DELETE)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class EstudanteViewSet(viewsets.ModelViewSet):
    #O método get_serializer_class() é usado para retornar um serializer diferente dependendo da versão da API.
    
    queryset = Estudante.objects.all()
    # serializer_class = EstudanteSerializer # Comentado para usar o método get_serializer_class()
    
    # filtros
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter] # OrderingFilter: Ordena os resultados, SearchFilter: Faz busca
    ordering_fields = ['nome',] # Ordena por nome
    search_fields = ['nome', 'cpf'] # Faz busca por nome e cpf
    
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return EstudanteSerializerV2
        return EstudanteSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    
class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    
class ListaMatriculaEstudante(generics.ListAPIView):
    
    def get_queryset(self):
        queryset = Matricula.objects.filter(estudante_id=self.kwargs['pk_estudante'])
        return queryset
    
    serializer_class = ListaMatriculasEstudanteSerializer
    
class ListaMatriculaCurso(generics.ListAPIView):
    
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs['pk_curso'])
        return queryset
        
    serializer_class = ListaMatriculasCursoSerializer