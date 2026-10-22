# Snake Trojan Lab — Simulador Educacional de Cibersegurança

> **Aviso importante:** este é um **simulador educacional**. **Não** é um
> malware real. Ele demonstra, de forma **controlada e transparente**, como um
> projeto de jogo com vários arquivos pode esconder, no meio deles, um
> componente que faz algo inesperado. Nenhum dado é coletado, nada é enviado
> para a internet, nada é instalado e nenhuma configuração do Windows é alterada.

---

## 1. A ideia

Agora o projeto tem a cara de um **jogo real**: vários arquivos, organizados em
pastas (`jogo/`, `servicos/`, `assets/`). O jogo da cobrinha funciona
normalmente. Mas, no meio dos arquivos, existe **um** que é o **payload** (a
"carga" do trojan):

```
servicos/update_service.py
```

Quando o jogador **perde**, o jogo **chama esse arquivo separado**, que então:

1. cria arquivos **fictícios** em `Documentos\SnakeTrojanLab\artefatos`;
2. abre o **Bloco de Notas** com uma mensagem educacional;
3. abre um **terminal com o "papagaio dançando"** (party parrot).

> **Sobre o papagaio:** por padrão ele roda `curl parrot.live`, que **baixa e
> exibe** uma animação do servidor público `parrot.live`. Isso faz uma
> **conexão de rede real** — e é de propósito: um "jogo" acessando a internet
> é, por si só, um **indicador suspeito** que o aluno pode detectar com
> `netstat`. O `curl` apenas *exibe* o fluxo; ele **não executa** código
> baixado. Para rodar sem internet, abra `servicos/update_service.py` e troque
> `USAR_PARROT_ONLINE = True` para `False` (usa a animação local
> `servicos/papagaio.py`).

Essa separação imita casos reais, em que a parte maliciosa costuma ser um
**módulo à parte**, com nome inocente, que o programa principal aciona.

---

## 2. Requisitos

- **Windows 11** (funciona em outras versões do Windows).
- **Python 3** (o Tkinter já vem junto no Windows).
- **Sem** privilégios de administrador e **sem** dependências externas.

Confira o Python no PowerShell:

```bash
python --version
```

---

## 3. Como executar

Abra o **PowerShell dentro da pasta `SnakeTrojanLab`** e rode:

```bash
python main.py
```

Jogue com as **setas**. Ao perder, pressione **ESPAÇO** para reiniciar.
Na primeira derrota, o Bloco de Notas abre uma vez e a pasta
`Documentos\SnakeTrojanLab` é criada. Isso é esperado.

---

## 4. Estrutura de arquivos

### No projeto (o "jogo")

```
SnakeTrojanLab/
├── main.py                     # ponto de entrada (python main.py)
├── README.md                   # este arquivo
├── jogo/                       # <<< código LEGÍTIMO do jogo >>>
│   ├── __init__.py
│   ├── config.py               # cores, tamanhos, velocidade
│   ├── motor.py                # lógica da cobra, movimento e colisão
│   ├── interface.py            # janela (Tkinter), desenho e laço do jogo
│   └── registro.py             # grava eventos REAIS do jogo
├── servicos/
│   ├── __init__.py
│   ├── update_service.py       # <<< O PAYLOAD (o "trojan" simulado) >>>
│   └── papagaio.py             # animação local do papagaio (modo offline)
└── assets/
    └── sobre.txt               # recurso de "jogo real" (inofensivo)
```

### Criada em tempo de execução (quando o jogador perde)

```
Documentos\SnakeTrojanLab\
├── MENSAGEM_DO_LAB.txt             # a mensagem exibida no Bloco de Notas
└── artefatos\
    ├── historico_execucao.log       # [REAL]  eventos que realmente aconteceram
    ├── trojan_simulado.txt          # [SIMULADO] artefato fictício
    ├── update_service.log           # [SIMULADO] nome comum, conteúdo fictício
    ├── persistencia_simulada.txt    # [SIMULADO] descreve persistência (não a cria)
    └── atividade_rede_simulada.log  # [SIMULADO] eventos de rede fictícios
```

> `historico_execucao.log` (marcado `[REAL]`) é escrito pelo jogo e registra o
> que de fato aconteceu. Os demais (`[SIMULADO]`) são "dropados" pelo payload e
> servem só como pistas fictícias para a investigação.

---

## 5. Onde está o trojan e como ele é acionado

O trojan **não** está espalhado pelo jogo: ele é **um arquivo só**,
`servicos/update_service.py`. A ligação acontece em dois pontos:

1. **`jogo/interface.py`** importa o módulo no topo:

   ```python
   from servicos import update_service
   ```

2. Dentro de **`finalizar_partida()`** (também em `interface.py`), ao detectar
   a morte, o jogo chama o payload **uma única vez**:

   ```python
   if not self.payload_executado:
       self.payload_executado = True
       update_service.executar_payload(self.motor.pontos)   # <-- aqui
   ```

3. Em **`servicos/update_service.py`**, `executar_payload()` cria os arquivos
   fictícios e abre o Bloco de Notas.

Fluxo resumido:

```
main.py  →  jogo/interface.py  →  (ao morrer)  →  servicos/update_service.py
  jogo          jogo                                   PAYLOAD (trojan)
```

---

## 6. O que este programa **não** faz

- Não coleta senhas, cookies, tokens ou dados pessoais.
- Não captura teclas fora do próprio jogo.
- Não envia informações para servidores externos.
- Não executa comandos remotos nem baixa/executa arquivos adicionais.
- Não desativa antivírus nem altera configurações do Windows.
- Não cria persistência (inicialização automática, tarefas, serviços).
- Não oculta arquivos nem processos.
- Não impede o usuário de fechar a aplicação.

---

## 7. Encerrar o laboratório

Para apagar o que o jogo criou, basta remover a pasta
`Documentos\SnakeTrojanLab`. Pelo PowerShell:

```bash
Remove-Item -Recurse -Force "$HOME\Documents\SnakeTrojanLab"
```
