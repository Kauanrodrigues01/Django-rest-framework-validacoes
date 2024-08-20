from rest_framework import serializers
from escola.models import Estudante, Curso, Matricula

from escola.validators import validar_cpf, cpf_invalido, nome_invalido, celular_invalido, celular_modelo_invalido

class EstudanteSerializer(serializers.ModelSerializer):
    '''
    ➤ Validações de campos customizadas são feitas através do método validate_<nome_do_campo>.
    
    ➤ O método validate_<nome_do_campo> recebe o campo como parâmetro e se o campo for inválido, você deve lançar uma exceção serializers.ValidationError com a mensagem de erro. Se o campo for válido, você deve retornar o campo.
    
    ➤ O método validate() é chamado após todas as validações de campos individuais. Se você deseja fazer uma validação que envolva mais de um campo, você pode fazer isso no método validate().
    
    ➤ Já que ele não recebe um campo específico, no ValidationError você deve passar um dicionário com o campo que está com erro e a mensagem de erro.
    '''
    class Meta:
        model = Estudante
        fields = ['id', 'nome', 'email', 'cpf', 'data_nascimento', 'celular']
        
    def validate(self, dados):
        # Verificação do tamanho do CPF
        if cpf_invalido(dados['cpf']):
            raise serializers.ValidationError({'cpf': 'O CPF deve ter 11 dígitos!'})
        
        # Verficação dos CPF
        if not validar_cpf(dados['cpf']):
            raise serializers.ValidationError({'cpf': 'O CPF não é válido'})
        
        if nome_invalido(dados['nome']):
            raise serializers.ValidationError({'nome': 'O nome só pode conter letras e espaços!'})
        
        if celular_invalido(dados['celular']):
            raise serializers.ValidationError({'celular': 'O celular deve ter 13 dígitos e ser numérico!'})
        
        if celular_modelo_invalido(dados['celular']):
            raise serializers.ValidationError({'celular': 'O celular deve seguir este modelo: 86 99999-9999 (respeitando traços e espaços)'})

        return dados

class CursoSerializer(serializers.ModelSerializer):
    nivel = serializers.SerializerMethodField()
    class Meta:
        model = Curso
        fields = ['codigo', 'descricao', 'nivel']  # Pega todos os campos
        
    def get_nivel(self, obj):
        return obj.get_nivel_display()

# 1 - Serializer de Matricula
class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []  # Não exclui nenhum campo, ou seja, pega todos os campos
        
# 2 - Serializer de Matriculas por Estudante
class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    '''
    ➤ serializers.ReadOnlyField() diz para API que o campo é somente leitura, ou seja, não pode ser modificado.
    ➤ source='curso.descricao' é uma forma de acessar o campo descrição do curso, em vez de retornar o id do curso.
    
    ➤ O nome do método que será chamado pelo serializers.SerializerMethodField() segue essa convenção: get_ + nome da variável. Se a variável fosse chamada x, o método deveria ser get_x(self, obj).
    
    ➤ O obj é a instância do modelo Matricula.
    
    ➤ O método get_periodo_display() é uma função do Django que retorna o valor "por extenso" de um campo que utiliza escolhas (choices) no modelo.
    '''
    curso = serializers.ReadOnlyField(source='curso.descricao') 
    
    periodo = serializers.SerializerMethodField()
    
    class Meta:
        model = Matricula
        fields = ['curso', 'periodo']
    
    def get_periodo(self, obj):
        return obj.get_periodo_display()

# 3 - Serializer de Matriculas de Estudantes por Curso
class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.ReadOnlyField(source='estudante.nome')
    
    class Meta:
        model = Matricula
        fields = ['estudante_nome']
      
        
# Versionamento de serializers
class EstudanteSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id', 'nome', 'email', 'celular']
        
    def validate(self, dados):
        if nome_invalido(dados['nome']):
            raise serializers.ValidationError({'nome': 'O nome só pode conter letras e espaços!'})
        
        if celular_invalido(dados['celular']):
            raise serializers.ValidationError({'celular': 'O celular deve ter 13 dígitos e ser numérico!'})
        
        if celular_modelo_invalido(dados['celular']):
            raise serializers.ValidationError({'celular': 'O celular deve seguir este modelo: 86 99999-9999 (respeitando traços e espaços)'})

        return dados