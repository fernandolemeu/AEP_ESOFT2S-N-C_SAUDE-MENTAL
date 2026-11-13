# PSE em Ação — AEP UniCesumar 2026

**Segunda entrega — implementação e apresentação**  
Engenharia de Software — ESOFT2S-N-C — UniCesumar

O **PSE em Ação** é uma aplicação desenvolvida em linguagem C e executada no terminal para apoiar o cadastro e o acompanhamento de ações coletivas do Programa Saúde na Escola (PSE).

O sistema reúne informações de cada atividade, permite acompanhar sua situação e apresenta um resumo das participações previstas e efetivas.

## Integrantes

- Fernando Leme Origuela
- Lucas Fontes Telles
- Lucas Gabriel

## Objetivo e escopo

O sistema foi desenvolvido para auxiliar um operador da equipe responsável pelo planejamento das ações coletivas do Programa Saúde na Escola.

São utilizados dados fictícios e informações coletivas. O programa não cadastra estudantes individualmente, não armazena prontuários ou dados clínicos e não realiza diagnósticos ou atendimentos de saúde.

Os registros são armazenados temporariamente na memória durante a execução. Ao encerrar o programa, os dados são descartados.

## Funcionalidades implementadas

1. **Cadastrar ação:** registra código, escola, tema, data prevista, público-alvo, responsável e participações previstas.
2. **Listar ações:** exibe todos os registros cadastrados durante a execução atual.
3. **Pesquisar ações:** permite pesquisar por código, escola ou tema, inclusive utilizando trechos de texto.
4. **Atualizar situação:** permite alterar uma ação para planejada, realizada ou cancelada.
5. **Registrar participações efetivas:** permite informar a quantidade efetiva de participações quando uma ação é marcada como realizada.
6. **Gerar resumo geral:** apresenta totais por situação, participações previstas e efetivas e o percentual de participação das ações realizadas.

O menu permanece ativo até que o usuário selecione a opção `0 - Sair`.

## Regras e limites do sistema

- Capacidade máxima de 100 ações por execução.
- Código inteiro entre 1 e 999999, sem repetição.
- Participações previstas e efetivas entre 0 e 10000.
- Data no formato DD/MM/AAAA, respeitando a existência da data no calendário e os anos bissextos.
- Campos de texto obrigatórios, com limite de 80 caracteres.
- Toda ação começa com a situação **Planejada** e zero participações efetivas.
- Ao confirmar uma alteração para Planejada ou Cancelada, as participações efetivas são zeradas.
- A pesquisa por escola e tema utiliza `strstr`, diferenciando letras maiúsculas, minúsculas e acentos.
- O percentual considera somente as participações previstas das ações realizadas. Quando essa previsão é zero, o cálculo não é efetuado.

## Tecnologias utilizadas

- Linguagem C.
- Dev-C++ como ambiente de desenvolvimento.
- GCC/MinGW para compilação.
- Git e GitHub para versionamento e organização do projeto.
- Vetores, estruturas (`struct`), funções, estruturas condicionais e laços de repetição.

## Ambiente e compilação

O arquivo-fonte principal está localizado em:

`src/main.c`

**Importante:** mantenha a extensão `.c` para que o arquivo seja compilado como linguagem C.

### Compilação pelo Dev-C++ (Windows)

1. Abra o Dev-C++.
2. Selecione **Arquivo > Abrir**.
3. Localize e abra o arquivo `src/main.c`.
4. Confira se o arquivo está identificado como C.
5. Selecione **Executar > Compilar e Executar**.
6. O terminal será aberto com o menu principal do PSE em Ação.

### Compilação pelo GCC/MinGW (Windows)

Na pasta principal do repositório, execute:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -O2 src/main.c -o pse_em_acao.exe
```

Para executar pelo PowerShell:

```powershell
.\pse_em_acao.exe
```

Também está disponível o arquivo `compilar_e_executar_windows.bat`, que automatiza a compilação e a execução quando o GCC/MinGW está instalado e configurado no PATH.

### Compilação pelo GCC (Linux)

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -O2 src/main.c -o pse_em_acao
./pse_em_acao
```

## Testes funcionais

A versão `src/main.c` foi compilada em C11 com GCC 14.2.0, utilizando as opções `-Wall -Wextra -Wpedantic -O2`, sem erros ou avisos no ambiente de verificação utilizado.

A suíte de testes funcionais contém **29 cenários**, todos aprovados nessa verificação.

Os testes verificam situações como:

- Cadastro e listagem de ações.
- Código duplicado.
- Campos vazios e textos muito longos.
- Validação de números e datas.
- Pesquisa por código, escola e tema.
- Atualização de situação e participações efetivas.
- Geração do resumo geral.
- Limite de armazenamento de 100 ações.
- Encerramento e reinicialização do programa.

Para executar novamente os testes, é necessário ter Python 3 e GCC disponíveis no PATH.

Na pasta principal do repositório, execute:

```bash
python tests/testes_funcionais.py
```

O script compila o código-fonte, executa os cenários e atualiza os arquivos de resultados:

- `tests/resultados_testes.json` — resultados detalhados.
- `tests/RELATORIO_TESTES.md` — relatório dos cenários executados.

Também foi realizada uma verificação complementar com AddressSanitizer e UndefinedBehaviorSanitizer em um cenário representativo de cadastro, atualização e resumo, sem alertas nesse cenário.

**Observação:** a compilação e os testes foram verificados no ambiente utilizado para esta revisão. A equipe deve realizar a conferência final no Dev-C++ instalado no computador Windows utilizado na disciplina.

## Organização do repositório

```text
PSE-em-Acao/
│
├── README.md
├── .gitignore
├── compilar_e_executar_windows.bat
│
├── src/
│   └── main.c
│
├── docs/
│   ├── AEP_PSE_em_Acao_Segunda_Entrega.pdf
│   ├── AEP_PSE_em_Acao_Segunda_Entrega.docx
│   ├── Manual_de_Usuario_PSE_em_Acao.pdf
│   ├── Primeira_Entrega_Original.pdf
│   ├── casos_de_uso.md
│   ├── requisitos_atualizados.md
│   └── roteiro_video.md
│
├── Diagramas e Fluxogramas/
│   ├── diagrama_casos_uso.png
│   ├── diagrama_casos_uso.dot
│   ├── fluxograma_geral_primeira_entrega.png
│   └── fluxograma_cadastro_primeira_entrega.png
│
├── Prints/
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   ├── 5.png
│   ├── 6.png
│   └── 7.png
│
└── tests/
    ├── testes_funcionais.py
    ├── resultados_testes.json
    ├── RELATORIO_TESTES.md
    ├── README_TESTES.md
    └── VERIFICACAO_SANITIZADORES.md
```

## Documentação e apresentação

O projeto possui os seguintes documentos complementares:

- **Documento técnico da segunda entrega:** `docs/AEP_PSE_em_Acao_Segunda_Entrega.pdf`.
- **Documento editável:** `docs/AEP_PSE_em_Acao_Segunda_Entrega.docx`.
- **Manual do usuário:** `docs/Manual_de_Usuario_PSE_em_Acao.pdf`.
- **Primeira entrega:** `docs/Primeira_Entrega_Original.pdf`.
- **Casos de uso:** `docs/casos_de_uso.md`.
- **Requisitos atualizados:** `docs/requisitos_atualizados.md`.
- **Roteiro de apresentação:** `docs/roteiro_video.md`.

Os diagramas, fluxogramas e capturas de tela também estão disponíveis nas respectivas pastas do repositório.

O vídeo de apresentação deve ser disponibilizado com acesso liberado para avaliação e respeitar a duração máxima de 7 minutos estabelecida no enunciado da AEP.

---

**Projeto acadêmico — UniCesumar — Engenharia de Software — 2º semestre de 2026.**
