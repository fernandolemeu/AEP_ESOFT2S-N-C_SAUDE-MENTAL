#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes funcionais do PSE em Ação, sem GCC.

O script NÃO compila o programa. Ele executa o arquivo .exe já existente,
envia os dados pelo terminal e verifica se as mensagens esperadas aparecem.

Estrutura esperada:
    PSE-em-Acao/
    |-- src/
    |   |-- codigo principal.exe
    |-- tests/
        |-- testar_codigo.py

Requisitos:
    - Windows
    - Python 3
    - codigo principal.exe já compilado

Como executar, na pasta principal do projeto:
    python tests/testar_codigo.py

Também é possível informar outro caminho:
    python tests/testar_codigo.py --exe "C:\\caminho\\codigo principal.exe"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass


ROOT = Path(__file__).resolve().parents[1]
EXECUTAVEL_PADRAO = ROOT / "src" / "codigo principal.exe"


@dataclass
class Resultado:
    nome: str
    aprovado: bool
    detalhe: str = ""


def cadastro(
    codigo: int,
    escola: str = "Escola Horizonte",
    tema: str = "Saude mental",
    data: str = "15/09/2026",
    publico: str = "Alunos do Ensino Medio",
    responsavel: str = "Equipe de Saude Escolar",
    previstos: int = 30,
) -> str:
    """Monta a entrada necessária para cadastrar uma ação."""
    return (
        "1\n"
        f"{codigo}\n"
        f"{escola}\n"
        f"{tema}\n"
        f"{data}\n"
        f"{publico}\n"
        f"{responsavel}\n"
        f"{previstos}\n"
    )


def executar(executavel: Path, entrada: str, timeout: int = 12) -> str:
    """
    Executa o .exe sem compilar.

    errors='replace' evita que caracteres acentuados do terminal do Windows
    interrompam a leitura da saída.
    """
    processo = subprocess.run(
        [str(executavel)],
        input=entrada,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        cwd=str(executavel.parent),
    )
    return processo.stdout


def verificar(
    nome: str,
    executavel: Path,
    entrada: str,
    esperados: list[str],
    resultados: list[Resultado],
    timeout: int = 12,
) -> None:
    try:
        saida = executar(executavel, entrada, timeout)
        faltantes = [texto for texto in esperados if texto not in saida]

        if faltantes:
            resultados.append(
                Resultado(
                    nome,
                    False,
                    "Não encontrou: " + " | ".join(faltantes),
                )
            )
        else:
            resultados.append(Resultado(nome, True))

    except subprocess.TimeoutExpired:
        resultados.append(
            Resultado(nome, False, "O programa demorou demais para responder.")
        )
    except OSError as erro:
        resultados.append(
            Resultado(nome, False, f"Não foi possível executar o .exe: {erro}")
        )


def executar_testes(executavel: Path) -> list[Resultado]:
    resultados: list[Resultado] = []
    sair = "0\n"

    # 01 — Cadastro válido e listagem.
    entrada = cadastro(101) + "2\n" + sair
    verificar(
        "01 - Cadastro e listagem",
        executavel,
        entrada,
        [
            "Acao cadastrada com sucesso",
            "Codigo: 101",
            "Situacao: Planejada",
            "Participacoes efetivas: 0",
        ],
        resultados,
    )

    # 02 — Código repetido deve ser recusado; o segundo código é aceito.
    entrada = (
        cadastro(201)
        + "1\n201\n202\nEscola Nova\nSaude mental\n15/09/2026\n"
          "Alunos do Ensino Medio\nEquipe Escolar\n20\n"
        + "2\n0\n"
    )
    verificar(
        "02 - Recusa de código duplicado",
        executavel,
        entrada,
        [
            "Este codigo ja esta cadastrado",
            "Codigo: 202",
            "Escola: Escola Nova",
        ],
        resultados,
    )

    # 03 — Campo de texto vazio.
    entrada = (
        "1\n301\n\nEscola Valida\nSaude mental\n15/09/2026\n"
        "Turma A\nEquipe Escolar\n10\n2\n0\n"
    )
    verificar(
        "03 - Validação de campo vazio",
        executavel,
        entrada,
        [
            "Este campo nao pode ficar vazio",
            "Escola: Escola Valida",
        ],
        resultados,
    )

    # 04 — Texto acima do limite de 80 caracteres.
    texto_longo = "X" * 81
    entrada = (
        f"1\n302\n{texto_longo}\nEscola Curta\nSaude mental\n15/09/2026\n"
        "Turma A\nEquipe Escolar\n10\n2\n0\n"
    )
    verificar(
        "04 - Validação de tamanho de texto",
        executavel,
        entrada,
        [
            "O texto deve ter no maximo 80 caracteres",
            "Escola: Escola Curta",
        ],
        resultados,
    )

    # 05 — Data impossível seguida de data válida.
    entrada = (
        "1\n303\nEscola Data\nSaude mental\n31/02/2026\n"
        "01/03/2026\nTurma A\nEquipe Escolar\n10\n2\n0\n"
    )
    verificar(
        "05 - Recusa de data inexistente",
        executavel,
        entrada,
        [
            "Data invalida. Verifique o dia, o mes e o ano.",
            "Data prevista: 01/03/2026",
        ],
        resultados,
    )

    # 06 — Formato incorreto seguido de data válida.
    entrada = (
        "1\n304\nEscola Formato\nSaude mental\n2\n"
        "04/05/2026\nTurma A\nEquipe Escolar\n10\n2\n0\n"
    )
    verificar(
        "06 - Validação do formato da data",
        executavel,
        entrada,
        [
            "Data invalida. Verifique o dia, o mes e o ano.",
            "Data prevista: 04/05/2026",
        ],
        resultados,
    )

    # 07 — Ano bissexto: 29/02/2024 é uma data válida.
    entrada = cadastro(305, data="29/02/2024") + "2\n0\n"
    verificar(
        "07 - Aceitação de data em ano bissexto",
        executavel,
        entrada,
        [
            "Acao cadastrada com sucesso",
            "Data prevista: 29/02/2024",
        ],
        resultados,
    )

    # 08 — Código não numérico seguido de valor válido.
    entrada = (
        "1\nabc\n306\nEscola Numero\nSaude mental\n15/09/2026\n"
        "Turma A\nEquipe Escolar\n10\n2\n0\n"
    )
    verificar(
        "08 - Validação de entrada numérica",
        executavel,
        entrada,
        [
            "Valor invalido. Digite um numero entre 1 e 999999.",
            "Codigo: 306",
        ],
        resultados,
    )

    # 09 — Quantidade prevista acima do limite e depois valor válido.
    entrada = (
        "1\n307\nEscola Quantidade\nSaude mental\n15/09/2026\n"
        "Turma A\nEquipe Escolar\n10001\n15\n2\n0\n"
    )
    verificar(
        "09 - Limite de participações previstas",
        executavel,
        entrada,
        [
            "Valor invalido. Digite um numero entre 0 e 10000.",
            "Participacoes previstas: 15",
        ],
        resultados,
    )

    # 10 — Pesquisa por código existente.
    entrada = cadastro(401) + "3\n1\n401\n0\n"
    verificar(
        "10 - Pesquisa por código existente",
        executavel,
        entrada,
        [
            "Codigo: 401",
            "Escola: Escola Horizonte",
        ],
        resultados,
    )

    # 11 — Pesquisa por código inexistente.
    entrada = cadastro(402) + "3\n1\n999\n0\n"
    verificar(
        "11 - Pesquisa por código inexistente",
        executavel,
        entrada,
        ["Acao nao encontrada."],
        resultados,
    )

    # 12 — Pesquisa textual por parte do nome da escola.
    entrada = (
        cadastro(403, escola="Escola Municipal Aurora")
        + "3\n2\nAurora\n0\n"
    )
    verificar(
        "12 - Pesquisa por trecho da escola",
        executavel,
        entrada,
        [
            "Escola: Escola Municipal Aurora",
            "Total de acoes encontradas: 1",
        ],
        resultados,
    )

    # 13 — Pesquisa textual por parte do tema.
    entrada = (
        cadastro(404, tema="Promocao da saude mental")
        + "3\n3\nsaude\n0\n"
    )
    verificar(
        "13 - Pesquisa por trecho do tema",
        executavel,
        entrada,
        [
            "Tema: Promocao da saude mental",
            "Total de acoes encontradas: 1",
        ],
        resultados,
    )

    # 14 — Pesquisa sem correspondência.
    entrada = cadastro(405) + "3\n3\nVacinação\n0\n"
    verificar(
        "14 - Pesquisa sem resultados",
        executavel,
        entrada,
        ["Nenhuma acao encontrada."],
        resultados,
    )

    # 15 — Atualização para realizada com 8 participações.
    entrada = (
        cadastro(501)
        + "4\n501\n2\n8\n1\n"
        + "2\n0\n"
    )
    verificar(
        "15 - Atualização para realizada",
        executavel,
        entrada,
        [
            "Acao atualizada com sucesso.",
            "Situacao: Realizada",
            "Participacoes efetivas: 8",
        ],
        resultados,
    )

    # 16 — Cancelamento da confirmação mantém os dados anteriores.
    entrada = (
        cadastro(502)
        + "4\n502\n2\n12\n0\n"
        + "2\n0\n"
    )
    verificar(
        "16 - Cancelamento da confirmação",
        executavel,
        entrada,
        [
            "Alteracao cancelada. Os dados anteriores foram mantidos.",
            "Situacao: Planejada",
            "Participacoes efetivas: 0",
        ],
        resultados,
    )

    # 17 — Atualização para cancelada.
    entrada = (
        cadastro(503)
        + "4\n503\n3\n1\n"
        + "2\n0\n"
    )
    verificar(
        "17 - Atualização para cancelada",
        executavel,
        entrada,
        [
            "Acao atualizada com sucesso.",
            "Situacao: Cancelada",
            "Participacoes efetivas: 0",
        ],
        resultados,
    )

    # 18 — Atualização de ação inexistente.
    entrada = cadastro(504) + "4\n999\n0\n"
    verificar(
        "18 - Atualização de código inexistente",
        executavel,
        entrada,
        ["Acao nao encontrada."],
        resultados,
    )

    # 19 — Resumo e percentual de 60%.
    entrada = (
        cadastro(601, previstos=50)
        + "4\n601\n2\n30\n1\n"
        + "5\n0\n"
    )
    verificar(
        "19 - Resumo com percentual de 60%",
        executavel,
        entrada,
        [
            "Total de acoes cadastradas: 1",
            "Acoes realizadas: 1",
            "Participacoes previstas (acoes realizadas): 50",
            "Participacoes efetivas (acoes realizadas): 30",
            "Percentual de participacao nas acoes realizadas: 60.00%",
        ],
        resultados,
    )

    # 20 — Resumo sem registros: não deve dividir por zero.
    entrada = "5\n0\n"
    verificar(
        "20 - Resumo sem registros",
        executavel,
        entrada,
        [
            "Total de acoes cadastradas: 0",
            "Percentual nao calculavel",
        ],
        resultados,
    )

    # 21 — Previsão zero numa ação realizada: não deve dividir por zero.
    entrada = (
        cadastro(701, previstos=0)
        + "4\n701\n2\n0\n1\n"
        + "5\n0\n"
    )
    verificar(
        "21 - Resumo com previsão zero",
        executavel,
        entrada,
        [
            "Participacoes previstas (acoes realizadas): 0",
            "Percentual nao calculavel",
        ],
        resultados,
    )

    # 22 — Tentativa de ultrapassar a capacidade de 100 ações.
    entrada = "".join(
        cadastro(i, escola=f"Escola {i}", previstos=1)
        for i in range(1, 101)
    )
    entrada += "1\n5\n0\n"
    verificar(
        "22 - Limite máximo de 100 ações",
        executavel,
        entrada,
        [
            "Limite de 100 acoes atingido.",
            "Total de acoes cadastradas: 100",
        ],
        resultados,
        timeout=30,
    )

    # 23 — Opção inválida no menu.
    entrada = "9\n0\n"
    verificar(
        "23 - Validação da opção do menu",
        executavel,
        entrada,
        [
            "Valor invalido. Digite um numero entre 0 e 5.",
            "Encerrando o sistema.",
        ],
        resultados,
    )

    # 24 — Os dados não persistem ao encerrar e abrir uma nova execução.
    primeira = executar(executavel, cadastro(901) + "0\n")
    segunda = executar(executavel, "2\n5\n0\n")
    esperados = [
        "Acao cadastrada com sucesso.",
        "Nenhuma acao cadastrada.",
        "Total de acoes cadastradas: 0",
    ]
    faltantes = [item for item in esperados if item not in primeira + segunda]
    resultados.append(
        Resultado(
            "24 - Registros temporários entre execuções",
            not faltantes,
            "Não encontrou: " + " | ".join(faltantes) if faltantes else "",
        )
    )

    return resultados


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Executa testes funcionais no .exe existente do PSE em Ação. Não usa GCC."
    )
    parser.add_argument(
        "--exe",
        type=Path,
        default=EXECUTAVEL_PADRAO,
        help="Caminho do executável já compilado.",
    )
    args = parser.parse_args()

    executavel = args.exe.expanduser().resolve()

    print("=" * 66)
    print("TESTES FUNCIONAIS — PSE EM AÇÃO (SEM GCC)")
    print("=" * 66)

    if not executavel.is_file():
        print("\nERRO: não encontrei o executável.")
        print(f"Caminho procurado: {executavel}")
        print("\nColoque 'codigo principal.exe' em src ou informe o caminho:")
        print('python tests/testar_codigo.py --exe "C:\\caminho\\programa.exe"')
        return 2

    resultados = executar_testes(executavel)

    for resultado in resultados:
        status = "APROVADO" if resultado.aprovado else "FALHOU"
        print(f"[{status}] {resultado.nome}")
        if resultado.detalhe:
            print(f"          {resultado.detalhe}")

    aprovados = sum(r.aprovado for r in resultados)
    total = len(resultados)
    reprovados = total - aprovados

    print("\n" + "=" * 66)
    print(f"RESULTADO: {aprovados}/{total} testes aprovados")
    print(f"Reprovados: {reprovados}")
    print(f"Executável testado: {executavel}")
    print("=" * 66)

    return 0 if reprovados == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
