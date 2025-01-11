import os
from datetime import datetime

def escreve_no_arquivo(mensagem):
    """
    Escreve uma mensagem em um arquivo cujo nome é baseado na data atual.
    Se o arquivo não existir, ele será criado; caso contrário, a mensagem será adicionada.
    
    :param mensagem: Texto que será escrito no arquivo.
    """
    # Obtém a data atual
    hoje = datetime.now()
    nome_arquivo = f"teste - {hoje.day:02d}-{hoje.month:02d}-{hoje.year}.txt"

    # Verifica se o arquivo já existe
    if not os.path.exists(nome_arquivo):
        # Cria o arquivo se não existir
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write(f"Arquivo criado em {hoje.strftime('%d/%m/%Y %H:%M:%S')}\n")
            arquivo.write(mensagem + f" {hoje.strftime('%d/%m/%Y %H:%M:%S')}\n")
            print(f"Arquivo '{nome_arquivo}' criado e mensagem escrita.")
    else:
        # Adiciona a mensagem ao arquivo existente
        with open(nome_arquivo, "a") as arquivo:
            arquivo.write(mensagem + f" {hoje.strftime('%d/%m/%Y %H:%M:%S')}\n")
            print(f"Mensagem adicionada ao arquivo '{nome_arquivo}'.")