# -*- coding: utf-8 -*-
"""
registro.py - registro de eventos REAIS e benignos do jogo.

Grava no arquivo historico_execucao.log apenas o que REALMENTE aconteceu
(inicio do jogo, inicio da partida, pontuacao final, etc.), sempre marcado
com [REAL]. Isso permite, na investigacao, diferenciar um evento real de um
evento apenas simulado (que esta nos arquivos ficticios criados pelo payload).

Este arquivo nao abre o Bloco de Notas e nao faz nada "inesperado".
"""

import os
import datetime
from jogo import config


def caminho_pasta_lab():
    """Caminho de Documentos\\SnakeTrojanLab (sem privilegios de admin)."""
    documentos = os.path.join(os.path.expanduser("~"), "Documents")
    if not os.path.isdir(documentos):
        documentos = os.path.expanduser("~")
    return os.path.join(documentos, config.NOME_PASTA_LAB)


def caminho_artefatos():
    """Subpasta 'artefatos' dentro da pasta de laboratorio."""
    return os.path.join(caminho_pasta_lab(), "artefatos")


def inicializar():
    """Garante que a pasta e o arquivo de historico existam."""
    try:
        os.makedirs(caminho_artefatos(), exist_ok=True)
        historico = os.path.join(caminho_artefatos(), "historico_execucao.log")
        if not os.path.exists(historico):
            agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(historico, "w", encoding="utf-8") as f:
                f.write("# historico_execucao.log - eventos REAIS e benignos do jogo\n")
                f.write("# Linhas marcadas com [REAL] realmente aconteceram.\n")
                f.write("[{0}] [REAL] arquivo de historico criado\n".format(agora))
    except Exception as erro:
        print("Aviso: nao foi possivel inicializar o registro:", erro)


def registrar_evento(mensagem):
    """Acrescenta um evento REAL ao historico, com data e hora."""
    try:
        os.makedirs(caminho_artefatos(), exist_ok=True)
        historico = os.path.join(caminho_artefatos(), "historico_execucao.log")
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(historico, "a", encoding="utf-8") as f:
            f.write("[{0}] [REAL] {1}\n".format(agora, mensagem))
    except Exception as erro:
        print("Aviso: nao foi possivel registrar evento:", erro)
