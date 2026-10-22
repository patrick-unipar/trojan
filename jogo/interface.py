# -*- coding: utf-8 -*-
"""
interface.py - interface grafica (Tkinter) e laco principal do jogo.

Aqui mora a janela do jogo, o desenho, o teclado, a tela de fim de jogo e o
reinicio. Este arquivo tambem contem o PONTO DE LIGACAO com o payload:
quando o jogador morre, o jogo CHAMA o arquivo separado
'servicos/update_service.py'. O payload em si NAO esta aqui.
"""

import tkinter as tk

from jogo import config
from jogo import registro
from jogo.motor import MotorSnake

# >>> IMPORTACAO DO MODULO SEPARADO QUE CONTEM O "TROJAN" <<<
# Repare: o comportamento inesperado nao e definido neste arquivo. Ele vem de
# um modulo externo, importado como se fosse um "servico" qualquer do jogo.
from servicos import update_service


class JanelaJogo:
    """Janela principal do Snake Trojan Lab."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Snake Trojan Lab")
        self.raiz.resizable(False, False)
        self.raiz.configure(bg=config.COR_FUNDO)

        self.motor = MotorSnake()
        self.loop_id = None
        self.payload_executado = False  # garante chamada UNICA por partida

        largura_px = config.LARGURA_CELULAS * config.TAMANHO_CELULA
        altura_px = config.ALTURA_CELULAS * config.TAMANHO_CELULA

        topo = tk.Frame(self.raiz, bg=config.COR_FUNDO)
        topo.pack(fill="x", padx=10, pady=(10, 0))
        self.label_pontos = tk.Label(
            topo, text="Pontos: 0", font=("Consolas", 14, "bold"),
            fg=config.COR_TEXTO, bg=config.COR_FUNDO
        )
        self.label_pontos.pack(side="left")
        tk.Label(
            topo, text="Simulador educacional", font=("Consolas", 10),
            fg=config.COR_SECUNDARIA, bg=config.COR_FUNDO
        ).pack(side="right")

        self.canvas = tk.Canvas(
            self.raiz, width=largura_px, height=altura_px,
            bg=config.COR_FUNDO, highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        self.label_info = tk.Label(
            self.raiz, text="Use as setas para mover. Coma o alimento vermelho.",
            font=("Consolas", 10), fg=config.COR_SECUNDARIA, bg=config.COR_FUNDO
        )
        self.label_info.pack(pady=(0, 10))

        self.raiz.bind("<Up>", lambda e: self.motor.definir_direcao(0, -1))
        self.raiz.bind("<Down>", lambda e: self.motor.definir_direcao(0, 1))
        self.raiz.bind("<Left>", lambda e: self.motor.definir_direcao(-1, 0))
        self.raiz.bind("<Right>", lambda e: self.motor.definir_direcao(1, 0))
        self.raiz.bind("<space>", lambda e: self._tecla_espaco())
        self.raiz.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        # Prepara o historico de eventos reais e registra o inicio.
        registro.inicializar()
        registro.registrar_evento("jogo iniciado (janela aberta)")

        self.iniciar_jogo()

    # -----------------------------------------------------------------------
    def iniciar_jogo(self):
        """Inicia (ou reinicia) uma partida."""
        self.motor.reiniciar()
        self.payload_executado = False
        self._atualizar_pontos()
        self.label_info.config(text="Use as setas para mover. Coma o alimento vermelho.")
        registro.registrar_evento("nova partida iniciada")
        if self.loop_id is not None:
            self.raiz.after_cancel(self.loop_id)
        self._loop()

    def reiniciar_jogo(self):
        """Reinicia a partida (tecla ESPACO na tela de fim de jogo)."""
        registro.registrar_evento("reinicio de partida solicitado pelo jogador")
        self.iniciar_jogo()

    # -----------------------------------------------------------------------
    def _loop(self):
        """Laco principal: avanca um passo e reagenda a si mesmo."""
        resultado = self.motor.passo()
        if resultado == "morreu":
            self.finalizar_partida()
            return
        if resultado == "comeu":
            self._atualizar_pontos()
        self._desenhar()
        self.loop_id = self.raiz.after(config.VELOCIDADE_MS, self._loop)

    # -----------------------------------------------------------------------
    def finalizar_partida(self):
        """
        Fim de partida. Registra a pontuacao e, UMA UNICA VEZ, CHAMA o modulo
        externo 'update_service' que executa a demonstracao do trojan.
        """
        if self.loop_id is not None:
            self.raiz.after_cancel(self.loop_id)
            self.loop_id = None

        registro.registrar_evento(
            "partida encerrada - pontuacao final: {0}".format(self.motor.pontos)
        )

        if not self.payload_executado:
            self.payload_executado = True
            # Evento REAL: o jogo chamou o servico externo.
            registro.registrar_evento(
                "jogo chamou o servico externo 'servicos/update_service.py'"
            )
            # >>> AQUI O JOGO EXECUTA O ARQUIVO SEPARADO (O PAYLOAD) <<<
            update_service.executar_payload(self.motor.pontos)

        self._desenhar_game_over()

    # -----------------------------------------------------------------------
    def _tecla_espaco(self):
        if not self.motor.viva:
            self.reiniciar_jogo()

    def _ao_fechar(self):
        registro.registrar_evento("jogo encerrado (janela fechada)")
        self.raiz.destroy()

    def _atualizar_pontos(self):
        self.label_pontos.config(text="Pontos: {0}".format(self.motor.pontos))

    def _celula(self, x, y, cor):
        x1 = x * config.TAMANHO_CELULA
        y1 = y * config.TAMANHO_CELULA
        self.canvas.create_rectangle(
            x1, y1, x1 + config.TAMANHO_CELULA, y1 + config.TAMANHO_CELULA,
            fill=cor, outline=config.COR_FUNDO
        )

    def _desenhar(self):
        self.canvas.delete("all")
        for x in range(config.LARGURA_CELULAS):
            for y in range(config.ALTURA_CELULAS):
                if (x + y) % 2 == 0:
                    self._celula(x, y, config.COR_GRADE)
        self._celula(self.motor.alimento[0], self.motor.alimento[1], config.COR_ALIMENTO)
        for seg in self.motor.cobra[:-1]:
            self._celula(seg[0], seg[1], config.COR_COBRA_CORPO)
        cabeca = self.motor.cobra[-1]
        self._celula(cabeca[0], cabeca[1], config.COR_COBRA_CABECA)

    def _desenhar_game_over(self):
        self.canvas.delete("all")
        largura_px = config.LARGURA_CELULAS * config.TAMANHO_CELULA
        altura_px = config.ALTURA_CELULAS * config.TAMANHO_CELULA
        self.canvas.create_text(
            largura_px / 2, altura_px / 2 - 40, text="FIM DE JOGO",
            fill=config.COR_ALIMENTO, font=("Consolas", 28, "bold")
        )
        self.canvas.create_text(
            largura_px / 2, altura_px / 2,
            text="Pontuacao final: {0}".format(self.motor.pontos),
            fill=config.COR_TEXTO, font=("Consolas", 16)
        )
        self.canvas.create_text(
            largura_px / 2, altura_px / 2 + 40,
            text="Pressione ESPACO para jogar de novo",
            fill=config.COR_SECUNDARIA, font=("Consolas", 12)
        )
        self.label_info.config(
            text="Verifique o Bloco de Notas que abriu e a pasta SnakeTrojanLab."
        )
