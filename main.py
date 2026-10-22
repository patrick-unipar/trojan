# -*- coding: utf-8 -*-
"""
Snake Trojan Lab - ponto de entrada do jogo.

Execute a partir desta pasta com:
    python main.py

Este arquivo apenas inicia a interface do jogo. Ele representa o "executavel
principal" de um projeto de jogo comum, que depende de varios outros arquivos.
"""

import tkinter as tk

from jogo.interface import JanelaJogo


def main():
    raiz = tk.Tk()
    JanelaJogo(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
