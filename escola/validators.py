# validators
from validate_docbr import CPF
import re

def cpf_invalido(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return True
    
def validar_cpf(num_cpf):
    cpf = CPF()
    cpf_invalido = cpf.validate(num_cpf)
    return cpf_invalido

def nome_invalido(nome):
    return not nome.replace(" ", "").isalpha()

def celular_invalido(celular):
    return len(celular) != 13

def celular_modelo_invalido(celular):
    modelo = f'[0-9]{2} [0-9]{5}-[0-9]{4}'
    resposta = re.findall(modelo,celular)
    print(resposta)
    if not resposta:
        return True
    return False