# -*- coding: utf-8 -*-
"""
config.py - configuracoes gerais do jogo (tamanhos, velocidade e cores).

Arquivo totalmente inofensivo. Faz parte do jogo "legitimo".
"""

# Dimensoes do tabuleiro (em celulas) e tamanho de cada celula (em pixels).
LARGURA_CELULAS = 28
ALTURA_CELULAS = 28
TAMANHO_CELULA = 32

# Intervalo entre movimentos, em milissegundos (menor = mais rapido).
VELOCIDADE_MS = 110

# Paleta de cores da interface.
COR_FUNDO = "#0d1b2a"
COR_GRADE = "#15263b"
COR_COBRA_CABECA = "#4ade80"
COR_COBRA_CORPO = "#22c55e"
COR_ALIMENTO = "#f87171"
COR_TEXTO = "#e5e7eb"
COR_SECUNDARIA = "#94a3b8"

# Nome da pasta de laboratorio criada dentro de "Documentos".
# (Usado tanto pelo registro de eventos reais quanto pelo payload simulado.)
NOME_PASTA_LAB = "SnakeTrojanLab"
