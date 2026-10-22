# -*- coding: utf-8 -*-
"""
papagaio.py - animacao do "papagaio dancando" (party parrot), OFFLINE.

Este script e aberto em uma nova janela de terminal pelo payload
(servicos/update_service.py) como um dos efeitos visiveis da demonstracao.

IMPORTANTE: e uma recriacao LOCAL e INOFENSIVA do famoso 'curl parrot.live'.
  - NAO acessa a internet;
  - NAO baixa nada;
  - NAO executa comandos do sistema (so imprime texto colorido na tela).
O usuario pode fechar a janela a qualquer momento.
"""

import os
import time

# No Windows 10/11, esta chamada "vazia" liga o suporte a cores ANSI no console.
os.system("")

# Codigos de cor ANSI - o party parrot troca de cor o tempo todo (arco-iris).
CORES = [
    "\033[91m",  # vermelho
    "\033[93m",  # amarelo
    "\033[92m",  # verde
    "\033[96m",  # ciano
    "\033[94m",  # azul
    "\033[95m",  # magenta
]
RESET = "\033[0m"

# Desenho do papagaio em ASCII (uma unica pose).
PAPAGAIO = r"""
        .--.
      ./ o \.
     /   _   \
    |   (_)   |
     \       /
      |     |
    __|     |__
   /   |   |   \
  '    |   |    '
       '---'
"""

# A "danca" e feita deslocando o papagaio para os lados em cada quadro.
OFFSETS = [0, 2, 4, 2]


def desenhar_quadro(indice):
    """Limpa a tela e desenha o papagaio com uma cor e um deslocamento."""
    # Limpa o console (cls no Windows, clear nos demais).
    os.system("cls" if os.name == "nt" else "clear")

    cor = CORES[indice % len(CORES)]
    espacos = " " * OFFSETS[indice % len(OFFSETS)]

    linhas = PAPAGAIO.splitlines()
    print(cor)
    for linha in linhas:
        print(espacos + linha)
    print(RESET)
    print(espacos + "   ~ party parrot ~")


def main():
    print("Papagaio dancando (simulacao educacional). Feche a janela quando quiser.\n")
    time.sleep(1)

    # Dança por um numero fixo de quadros (uns 25 segundos).
    for i in range(160):
        desenhar_quadro(i)
        time.sleep(0.15)

    # Encerra com um aviso claro de que foi tudo brincadeira/educacional.
    os.system("cls" if os.name == "nt" else "clear")
    print("\033[92m")
    print("  VOCE FOI 'HACKEADO'... por um papagaio. :)")
    print(RESET)
    print("  Isto foi uma SIMULACAO EDUCACIONAL de ciberseguranca.")
    print("  Nenhum dado foi roubado, nada foi baixado e nada foi enviado.")
    print()
    try:
        input("  Pressione ENTER para fechar esta janela...")
    except Exception:
        pass


if __name__ == "__main__":
    main()
