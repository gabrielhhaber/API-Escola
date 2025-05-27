from escola.models import Estudante,Curso, Matricula
from escola.serializers import EstudanteSerializer, EstudanteSerializerV2, CursoSerializer, MatriculaSerializer, ListaMatriculasEstudanteSerializer, ListaMatriculasCursoSerializer
from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as DjangoFilters
from escola.throttling import MatriculaAnonRateThrottle, MatriculaUserRateThrottle
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class EstudanteViewSet(viewsets.ModelViewSet):
    """
    Descrição do ViewSet:
    - Permite listar e gerenciar os estudantes da escola

    Campos de ordenação:
    - Nome: permite ordenar os resultados pelo nome do estudante

    Campos de pesquisa:
    - Nome: permite encontrar apenas os estudantes com aquele nome
    - cpf: permite encontrar apenas o estudante com determinado CPF

    Métodos permitidos: get, post, patch, put, delete, head, options

    Classes de serializer: EstudanteSerializer para v1 e EstudanteSerializerV2 para v2.
    """
    queryset = Estudante.objects.all().order_by("id")
    def get_serializer_class(self):
        if self.request.version == "v2":
            return EstudanteSerializerV2
        return EstudanteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["nome"]
    search_fields = ("nome", "cpf")
    

class CursoViewSet(viewsets.ModelViewSet):
    """
    Descrição do ViewSet:
    - Permite listar e gerenciar os cursos da escola

    Campos de ordenação:
    - Descricao: permite ordenar os resultados pela descrição do conteúdo do curso.
    Codigo: permite ordenar os resultados pelo código do curso.

    Campos de pesquisa:
    Descricao: permite pesquisar com base na descrição do conteúdo dos cursos.
    Codigo: permite encontrar apenas o curso que possui aquele código específico.

    Métodos permitidos: get, post, patch, put, delete, head, options
    """
    queryset = Curso.objects.all().order_by("id")
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["descricao", "codigo"]
    search_fields = ("descricao", "codigo")
    permission_classes = [IsAuthenticatedOrReadOnly]

class MatriculaViewSet(viewsets.ModelViewSet):
    """
    Descrição do ViewSet:
    - Permite listar e criar novas matrículas de alunos em determinados cursos.

    Métodos permitidos: get, post

    Throttle Classes:
    - MatriculaAnonRateThrottle: limite de requisições por segundo para usuários anônimos.
    MatriculaUserRateThrottle: limite de requisições por segundo para usuários registrados.
    """
    queryset = Matricula.objects.all().order_by("id")
    serializer_class = MatriculaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["estudante__nome", "curso__descricao"]
    throttle_classes = [MatriculaAnonRateThrottle, MatriculaUserRateThrottle]
    http_method_names = ["get", "post"]

class ListaMatriculaEstudante(generics.ListAPIView):
    """
    Descrição da View:
        - Lista Matriculas por id de Estudante
    Parâmetros:
    - pk (int): O identificador primário do objeto. Deve ser um número inteiro.
    """
    def get_queryset(self):
        queryset = Matricula.objects.filter(estudante_id=self.kwargs['pk'])
        return queryset
    serializer_class = ListaMatriculasEstudanteSerializer

class ListaMatriculaCurso(generics.ListAPIView):
    """
    Descrição da View:
    - Lista matriculas por id de curso
    Parâmetros:
    - pk (int): o identificador primário do objeto. Deve ser um número inteiro.
    """
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs['pk'])
        return queryset
    serializer_class = ListaMatriculasCursoSerializer