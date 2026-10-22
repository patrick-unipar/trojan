# -*- coding: utf-8 -*-
"""
============================================================================
 ESTE E O ARQUIVO DO "TROJAN" (PAYLOAD) - SIMULACAO EDUCACIONAL
============================================================================

Em uma investigacao real, ESTE seria o arquivo "malicioso" escondido no meio
de um projeto de jogo de aparencia normal. Note que:

  - o NOME ('update_service') parece o de um servico legitimo de atualizacao;
  - o LOCAL (pasta 'servicos/') parece o de um modulo auxiliar comum;
  - mas o CONTEUDO faz algo que nao tem relacao com um jogo.

O jogo (em jogo/interface.py) importa este modulo e chama executar_payload()
no momento em que o jogador morre. Separar o payload em um arquivo proprio
deixa a simulacao parecida com casos reais, em que a carga maliciosa costuma
ser um componente separado que o programa principal aciona.

IMPORTANTE - este payload e EDUCACIONAL e INOFENSIVO. Tudo o que ele faz:
  1. Cria arquivos FICTICIOS dentro de Documentos\\SnakeTrojanLab\\artefatos
     (para os alunos investigarem);
  2. Abre o Bloco de Notas uma vez com uma mensagem de aviso.

Ele NAO rouba dados, NAO acessa a internet, NAO cria persistencia, NAO oculta
nada e NAO altera configuracoes do Windows.
============================================================================
"""

import os
import sys
import datetime
import subprocess


# ---------------------------------------------------------------------------
# OPCAO DO PROFESSOR: qual "papagaio dancando" usar ao fim da partida.
#   True  -> versao ONLINE real (curl parrot.live). Faz uma CONEXAO DE REDE.
#            Otimo para a aula: o aluno pode DETECTAR essa conexao inesperada
#            (ex.: com 'netstat'). Mostra, na pratica, que ate um "jogo" pode
#            contatar a internet - um indicador de comportamento suspeito.
#   False -> versao OFFLINE (servicos/papagaio.py). Nao usa a internet.
# ---------------------------------------------------------------------------
USAR_PARROT_ONLINE = True


# ---------------------------------------------------------------------------
# Localizacao da pasta de laboratorio.
# (Repetida aqui de proposito, para que este arquivo seja autossuficiente e
#  possa ser lido e entendido sozinho durante a investigacao.)
# ---------------------------------------------------------------------------
def _pasta_lab():
    documentos = os.path.join(os.path.expanduser("~"), "Documents")
    if not os.path.isdir(documentos):
        documentos = os.path.expanduser("~")
    return os.path.join(documentos, "SnakeTrojanLab")


def _pasta_artefatos():
    return os.path.join(_pasta_lab(), "artefatos")


def _escrever(caminho, conteudo):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)


# ---------------------------------------------------------------------------
# FUNCAO PRINCIPAL DO PAYLOAD
# ---------------------------------------------------------------------------
def executar_payload(pontuacao=0):
    """
    Executa a demonstracao do trojan: cria os artefatos ficticios e abre o
    Bloco de Notas. Chamada pelo jogo (jogo/interface.py) ao fim da partida.
    """
    _dropar_artefatos_ficticios()
    _abrir_bloco_de_notas(pontuacao)
    _abrir_papagaio_dancando()


# ---------------------------------------------------------------------------
# 1) "Dropar" (criar) os arquivos ficticios da investigacao
# ---------------------------------------------------------------------------
def _dropar_artefatos_ficticios():
    """Cria os arquivos FICTICIOS marcados [SIMULADO] para a investigacao."""
    pasta_art = _pasta_artefatos()
    os.makedirs(pasta_art, exist_ok=True)

    _escrever(os.path.join(pasta_art, "trojan_simulado.txt"),
        "[SIMULADO] trojan_simulado.txt\n"
        "==============================\n\n"
        "Artefato DIDATICO. Nao contem codigo executavel e nao e um Trojan\n"
        "de verdade. Representa, numa investigacao simulada, a presenca de um\n"
        "componente 'suspeito'. Encontrar um arquivo de nome assustador nao\n"
        "prova, sozinho, que ele seja malicioso - avalie sempre o contexto.\n")

    _escrever(os.path.join(pasta_art, "update_service.log"),
        "[SIMULADO] update_service.log\n"
        "=============================\n"
        "Registros FICTICIOS. O nome 'update_service' parece legitimo de\n"
        "proposito: um nome comum NAO garante que o conteudo seja confiavel.\n\n"
        "2026-01-05 09:12:03 update_service: verificando versao (ficticio)\n"
        "2026-01-05 09:12:04 update_service: nenhuma atualizacao (ficticio)\n"
        "2026-01-05 09:40:17 update_service: rotina agendada (ficticio)\n")

    _escrever(os.path.join(pasta_art, "persistencia_simulada.txt"),
        "[SIMULADO] persistencia_simulada.txt\n"
        "====================================\n\n"
        "DESCREVE, so para estudo, como um malware real PODERIA se manter apos\n"
        "uma reinicializacao. ESTE PROGRAMA NAO IMPLEMENTA NADA DISSO.\n\n"
        "Tecnicas que um malware real poderia usar (NAO usadas aqui):\n"
        "  - pasta Inicializar (Startup) do Windows;\n"
        "  - chave Run no Registro;\n"
        "  - Tarefa Agendada;\n"
        "  - Servico do Windows.\n\n"
        "Como VERIFICAR (defensivo e seguro):\n"
        "  Get-CimInstance Win32_StartupCommand\n")

    _escrever(os.path.join(pasta_art, "atividade_rede_simulada.log"),
        "[SIMULADO] atividade_rede_simulada.log\n"
        "======================================\n"
        "Eventos FICTICIOS. Este programa NAO fez comunicacao de rede.\n"
        "Nenhum dado saiu deste computador.\n\n"
        "2026-01-05 09:12:10 [ficticio] conexao simulada 203.0.113.10:443\n"
        "2026-01-05 09:12:11 [ficticio] envio simulado de 0 bytes (exemplo)\n\n"
        "203.0.113.0/24 e faixa reservada para documentacao (RFC 5737); nao\n"
        "corresponde a nenhum servidor real.\n")


# ---------------------------------------------------------------------------
# 2) Abrir o Bloco de Notas com a mensagem (o efeito "visivel" do trojan)
# ---------------------------------------------------------------------------
def _abrir_bloco_de_notas(pontuacao):
    """Escreve a mensagem e abre o Bloco de Notas uma vez (sem travar o jogo)."""
    mensagem = (
        "VOCE FOI HACKEADO!\n"
        "\n"
        "...ou sera que foi mesmo?\n"
        "\n"
        "Esta foi uma simulacao educacional de ciberseguranca.\n"
        "Nenhum dado foi roubado ou enviado. Nada foi instalado e nenhuma\n"
        "configuracao do Windows foi alterada.\n"
        "\n"
        "O que aconteceu: ao detectar que voce perdeu (pontuacao {0}), o jogo\n"
        "chamou um arquivo separado chamado 'servicos/update_service.py'.\n"
        "Esse arquivo - e nao o jogo em si - abriu o Bloco de Notas e criou os\n"
        "arquivos da pasta 'Documentos\\SnakeTrojanLab'.\n"
        "\n"
        "Essa diferenca entre a FINALIDADE APARENTE (um jogo) e o COMPORTAMENTO\n"
        "REAL (um 'servico' que faz outra coisa) e a ideia por tras de um\n"
        "Trojan (cavalo de Troia). Investigue os arquivos para entender mais.\n"
    ).format(pontuacao)

    try:
        os.makedirs(_pasta_lab(), exist_ok=True)
        arquivo_msg = os.path.join(_pasta_lab(), "MENSAGEM_DO_LAB.txt")
        _escrever(arquivo_msg, mensagem)
    except Exception as erro:
        print("Aviso: nao foi possivel salvar a mensagem:", erro)
        arquivo_msg = None

    try:
        if sys.platform.startswith("win") and arquivo_msg:
            # Abre o Bloco de Notas num processo separado (nao trava o jogo).
            subprocess.Popen(["notepad.exe", arquivo_msg])
        elif arquivo_msg:
            print("[DEMO] (fora do Windows) mensagem salva em:", arquivo_msg)
    except Exception as erro:
        print("Aviso: nao foi possivel abrir o Bloco de Notas:", erro)


# ---------------------------------------------------------------------------
# 3) Abrir o "papagaio dancando" em uma nova janela de terminal
# ---------------------------------------------------------------------------
def _abrir_papagaio_dancando():
    """
    Abre um terminal com o papagaio dancando.

    Se USAR_PARROT_ONLINE for True, roda 'curl parrot.live': o curl BAIXA um
    fluxo de animacao do servidor publico parrot.live e o terminal apenas o
    EXIBE. Isso faz uma conexao de rede real (observavel com 'netstat') - um
    bom ponto de discussao: um "jogo" nao deveria acessar a internet.
    Observacao: curl so EXIBE o fluxo; ele NAO executa codigo baixado.

    Se for False (ou fora do Windows), roda a versao OFFLINE papagaio.py,
    que anima um papagaio em ASCII localmente, sem internet.
    """
    # Flag que faz o novo processo abrir em uma JANELA de console separada,
    # para nao travar o jogo.
    nova_janela = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)

    try:
        if sys.platform.startswith("win") and USAR_PARROT_ONLINE:
            # 'cmd /k' mantem a janela aberta mostrando a animacao do parrot.live.
            # (curl.exe ja vem no Windows 10/11.)
            #   --no-buffer (-N): mostra o fluxo em tempo real (sem isto, o curl
            #                     segura os dados e a janela fica "vazia");
            #   -L            : segue o redirecionamento de http:// para https://.
            subprocess.Popen(["cmd", "/k", "curl --no-buffer -L https://parrot.live"],
                             creationflags=nova_janela)
        else:
            # Versao offline: executa o script local papagaio.py.
            papagaio = os.path.join(os.path.dirname(__file__), "papagaio.py")
            subprocess.Popen([sys.executable, papagaio],
                             creationflags=nova_janela)
    except Exception as erro:
        print("Aviso: nao foi possivel abrir o papagaio:", erro)
