# -*- coding: utf-8 -*-
"""
motor.py - logica "pura" do jogo da cobrinha (sem interface grafica).

Cuida do estado da cobra, do movimento, da comida e da deteccao de colisao.
Nao abre janelas e nao faz nada com o sistema operacional: e so o jogo.
"""

import random
from jogo import config


class MotorSnake:
    """Guarda e atualiza o estado de uma partida."""

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        """Prepara uma nova partida: cobra no centro, indo para a direita."""
        meio_x = config.LARGURA_CELULAS // 2
        meio_y = config.ALTURA_CELULAS // 2
        self.cobra = [
            (meio_x - 1, meio_y),
            (meio_x, meio_y),
            (meio_x + 1, meio_y),
        ]
        self.direcao = (1, 0)
        self.proxima_direcao = (1, 0)
        self.pontos = 0
        self.viva = True
        self.alimento = self._novo_alimento()

    def definir_direcao(self, dx, dy):
        """Troca a direcao, sem permitir inverter 180 graus sobre o corpo."""
        if (dx, dy) == (-self.direcao[0], -self.direcao[1]):
            return
        self.proxima_direcao = (dx, dy)

    def verificar_colisao(self, posicao):
        """Retorna True se 'posicao' bate na parede ou no proprio corpo."""
        x, y = posicao
        if x < 0 or x >= config.LARGURA_CELULAS:
            return True
        if y < 0 or y >= config.ALTURA_CELULAS:
            return True
        if posicao in self.cobra:
            return True
        return False

    def passo(self):
        """
        Avanca um passo do jogo. Retorna:
          'morreu' -> houve colisao (fim de partida)
          'comeu'  -> a cobra comeu o alimento neste passo
          'ok'     -> movimento normal
        """
        self.direcao = self.proxima_direcao
        cabeca_x, cabeca_y = self.cobra[-1]
        nova_cabeca = (cabeca_x + self.direcao[0], cabeca_y + self.direcao[1])

        if self.verificar_colisao(nova_cabeca):
            self.viva = False
            return "morreu"

        self.cobra.append(nova_cabeca)

        if nova_cabeca == self.alimento:
            self.pontos += 1
            self.alimento = self._novo_alimento()
            return "comeu"

        # Nao comeu: remove a cauda para manter o tamanho.
        self.cobra.pop(0)
        return "ok"

    def _novo_alimento(self):
        """Sorteia uma celula livre (que nao esteja sobre a cobra)."""
        livres = [
            (x, y)
            for x in range(config.LARGURA_CELULAS)
            for y in range(config.ALTURA_CELULAS)
            if (x, y) not in self.cobra
        ]
        if not livres:
            # Tabuleiro cheio (vitoria tecnica): mantem a ultima posicao.
            return self.cobra[-1]
        return random.choice(livres)
