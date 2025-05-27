import re
from validate_docbr import CPF
def nome_invalido(nome):
    return not nome.isalpha()
def cpf_invalido(numero_cpf):
    cpf = CPF()
    return not cpf.validate(numero_cpf)
def celular_invalido(celular):
    modelo = "\([0-9]{2}\)\s[0-9]{5}-[0-9]{4}"
    resposta = re.findall(modelo, celular)
    return not resposta