from rest_framework import serializers
from escola.models import Estudante, Curso, Matricula
from escola.validators import nome_invalido, cpf_invalido, celular_invalido

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id','nome','email','cpf','data_nascimento','celular']
    def validate(self, data):
        if nome_invalido(data["nome"]):
            raise serializers.ValidationError({"nome": "Certifique-se de que o nome tem apenas letras."})
        if cpf_invalido(data["cpf"]):
            raise serializers.ValidationError({"cpf": "Certifique-se que o CPF segue o modelo oficial brasileiro."})
        if celular_invalido(data["celular"]):
            raise serializers.ValidationError({"celular": "Certifique-se que o celular segue exatamente este formato de exemplo, respeitando traços e espaços: (51) 99881-3018."})
        return data
    
class EstudanteSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id','nome','email','celular']
    def validate(self, data):
        if nome_invalido(data["nome"]):
            raise serializers.ValidationError({"nome": "Certifique-se de que o nome tem apenas letras."})
        if celular_invalido(data["celular"]):
            raise serializers.ValidationError({"celular": "Certifique-se que o celular segue exatamente este formato de exemplo, respeitando traços e espaços: (51) 99881-3018."})
        return data

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []

class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.descricao')
    periodo = serializers.SerializerMethodField()
    class Meta:
        model = Matricula
        fields = ['curso','periodo']
    def get_periodo(self,obj):
        return obj.get_periodo_display()

class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.ReadOnlyField(source = 'estudante.nome')
    class Meta:
        model = Matricula
        fields = ['estudante_nome']
        
        