#!/usr/bin/env python3
"""Testes de caixa-preta do PSE em Ação. Executa o binário C por entrada padrão."""
from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Resultado:
    id: str
    funcionalidade: str
    entrada: str
    esperado: str
    obtido: str
    status: str
    observacoes: str = ""


ROOT = Path(__file__).resolve().parents[1]


def cadastro(codigo: int, escola: str = "Escola Horizonte", tema: str = "Saúde mental",
             data: str = "15/09/2026", publico: str = "Alunos do 8º ano",
             responsavel: str = "Equipe CodeSaúde", previstos: int = 30) -> str:
    return (f"1\n{codigo}\n{escola}\n{tema}\n{data}\n{publico}\n"
            f"{responsavel}\n{previstos}\n")


def executar(binario: Path, entradas: str, expectativas: list[str],
             funcionalidade: str, descricao_entrada: str, id_teste: str,
             observacoes: str = "") -> Resultado:
    proc = subprocess.run([str(binario)], input=entradas, text=True,
                          capture_output=True, timeout=5, encoding="utf-8")
    saida = proc.stdout + proc.stderr
    faltantes = [item for item in expectativas if item not in saida]
    ok = proc.returncode == 0 and not faltantes
    obtido = "; ".join(faltantes) if faltantes else "Todas as mensagens/valores esperados foram encontrados."
    return Resultado(id_teste, funcionalidade, descricao_entrada,
                     "Encontrar: " + " | ".join(expectativas), obtido,
                     "APROVADO" if ok else "FALHOU", observacoes)



def executar_reinicio(binario: Path) -> Resultado:
    primeira = subprocess.run([str(binario)], input=cadastro(901) + "0\n", text=True,
                              capture_output=True, timeout=5, encoding="utf-8")
    segunda = subprocess.run([str(binario)], input="2\n5\n0\n", text=True,
                             capture_output=True, timeout=5, encoding="utf-8")
    saida = primeira.stdout + primeira.stderr + "\n--- NOVA EXECUÇÃO ---\n" + segunda.stdout + segunda.stderr
    esperados = ["Ação cadastrada com sucesso", "Encerrando o sistema",
                 "--- NOVA EXECUÇÃO ---", "Nenhuma ação cadastrada",
                 "Total de ações cadastradas: 0"]
    faltantes = [item for item in esperados if item not in saida]
    ok = primeira.returncode == 0 and segunda.returncode == 0 and not faltantes
    return Resultado("T24", "Memória e encerramento",
                     "Cadastrar ação, encerrar o primeiro processo e abrir um segundo processo",
                     "Primeiro processo registra e encerra; segundo processo inicia com zero registros",
                     "; ".join(faltantes) if faltantes else "A segunda execução iniciou sem os registros da primeira.",
                     "APROVADO" if ok else "FALHOU")


def executar_todos(binario: Path) -> list[Resultado]:
    r: list[Resultado] = []
    sair = "0\n"

    r.append(executar(binario, cadastro(101) + "2\n" + sair,
        ["Ação cadastrada com sucesso", "Código: 101", "Situação: Planejada", "Participações efetivas: 0"],
        "Cadastro e listagem", "Cadastro de uma ação válida e listagem", "T01"))

    r.append(executar(binario, cadastro(201) + "1\n201\n202\nEscola Nova\nSaúde mental\n15/09/2026\nAlunos do 8º ano\nEquipe CodeSaúde\n30\n2\n" + sair,
        ["Código já cadastrado", "Código: 201", "Escola: Escola Horizonte"],
        "Validação de código", "Repetição do código 201 seguida de novo cadastro", "T02",
        "O segundo registro com código repetido deve ser recusado."))

    r.append(executar(binario, "1\n301\n\nEscola Válida\nSaúde mental\n15/09/2026\nTurma A\nEquipe X\n10\n2\n0\n",
        ["O campo não pode ficar vazio", "Escola: Escola Válida"],
        "Validação de texto", "Escola vazia seguida de valor válido", "T03"))

    r.append(executar(binario, "1\n302\n   \nEscola Espaços\nSaúde mental\n15/09/2026\nTurma A\nEquipe X\n10\n2\n0\n",
        ["O campo não pode ficar vazio", "Escola: Escola Espaços"],
        "Validação de texto", "Escola contendo somente espaços seguida de valor válido", "T04"))

    r.append(executar(binario, "1\n303\nEscola N\nSaúde mental\n15/09/2026\nTurma A\nEquipe X\n-5\n15\n2\n0\n",
        ["Valor inválido", "Participações previstas: 15"],
        "Validação numérica", "Quantidade prevista negativa seguida de 15", "T05"))

    r.append(executar(binario, "1\nabc\n304\nEscola N\nSaúde mental\n15/09/2026\nTurma A\nEquipe X\n15\n2\n0\n",
        ["Valor inválido", "Código: 304"],
        "Validação numérica", "Letras no campo código seguidas de inteiro válido", "T06"))

    r.append(executar(binario, "1\n305\nEscola Data\nSaúde mental\n31/02/2026\n01/03/2026\nTurma A\nEquipe X\n10\n2\n0\n",
        ["Data inválida", "Data prevista: 01/03/2026"],
        "Validação de data", "31/02/2026 recusada e 01/03/2026 aceita", "T07"))

    r.append(executar(binario, cadastro(306, data="29/02/2024") + "2\n0\n",
        ["Ação cadastrada com sucesso", "Data prevista: 29/02/2024"],
        "Validação de data", "Data válida em ano bissexto (29/02/2024)", "T08"))

    r.append(executar(binario, cadastro(401) + "3\n1\n401\n0\n",
        ["Código: 401", "Escola: Escola Horizonte"],
        "Pesquisa", "Pesquisa por código existente", "T09"))

    r.append(executar(binario, cadastro(402) + "3\n1\n999\n0\n",
        ["Ação não encontrada"], "Pesquisa", "Pesquisa por código inexistente", "T10"))

    r.append(executar(binario, cadastro(403, escola="Escola Municipal Aurora") + "3\n2\nAurora\n0\n",
        ["Escola: Escola Municipal Aurora", "Total de ações encontradas: 1"],
        "Pesquisa", "Pesquisa textual por trecho do nome da escola", "T11"))

    r.append(executar(binario, cadastro(404, tema="Promoção da saúde mental") + "3\n3\nmental\n0\n",
        ["Tema: Promoção da saúde mental", "Total de ações encontradas: 1"],
        "Pesquisa", "Pesquisa textual por trecho do tema", "T12"))

    r.append(executar(binario, cadastro(405) + "3\n3\nVacinação\n0\n",
        ["Nenhum resultado encontrado"], "Pesquisa", "Pesquisa sem resultados", "T13"))

    r.append(executar(binario, cadastro(501) + "4\n501\n2\n8\n1\n2\n0\n",
        ["Ação atualizada com sucesso", "Situação: Realizada", "Participações efetivas: 8"],
        "Atualização", "Alteração para realizada e registro de 8 participações", "T14"))

    r.append(executar(binario, cadastro(502) + "4\n502\n2\n12\n1\n4\n502\n1\n1\n2\n0\n",
        ["Atenção: ao confirmar", "Ação atualizada com sucesso", "Situação: Planejada", "Participações efetivas: 0"],
        "Atualização", "Ação realizada com 12 participações retorna para planejada", "T15"))

    r.append(executar(binario, cadastro(503) + "4\n503\n2\n12\n1\n4\n503\n3\n1\n2\n0\n",
        ["Atenção: ao confirmar", "Ação atualizada com sucesso", "Situação: Cancelada", "Participações efetivas: 0"],
        "Atualização", "Ação realizada com 12 participações passa para cancelada", "T16"))

    r.append(executar(binario, cadastro(504) + "4\n999\n0\n",
        ["Ação não encontrada. Nenhum registro foi alterado."],
        "Atualização", "Tentativa de atualizar ação inexistente", "T17"))

    entradas18 = (cadastro(601, previstos=10) +
                  cadastro(602, previstos=20) + "4\n602\n2\n16\n1\n" +
                  cadastro(603, previstos=15) + "4\n603\n3\n1\n" +
                  "5\n0\n")
    r.append(executar(binario, entradas18,
        ["Total de ações cadastradas: 3", "Ações planejadas: 1", "Ações realizadas: 1",
         "Ações canceladas: 1", "Participações previstas (todas as ações): 45",
         "Participações previstas (ações realizadas): 20", "Participações efetivas (ações realizadas): 16",
         "Percentual de participação nas ações realizadas: 80.00%"],
        "Resumo", "Resumo com ações planejada, realizada e cancelada", "T18"))

    r.append(executar(binario, "5\n0\n",
        ["Total de ações cadastradas: 0", "Ações planejadas: 0", "Percentual não calculável"],
        "Resumo", "Resumo sem registros", "T19"))

    r.append(executar(binario, cadastro(701, previstos=0) + "5\n0\n",
        ["Participações previstas (ações realizadas): 0", "Percentual não calculável"],
        "Resumo", "Nenhuma ação realizada com previsão positiva; evita divisão por zero", "T20"))

    r.append(executar(binario, cadastro(702, previstos=20) + "4\n702\n2\n25\n1\n5\n0\n",
        ["Participações previstas (ações realizadas): 20", "Participações efetivas (ações realizadas): 25",
         "Percentual de participação nas ações realizadas: 125.00%"],
        "Resumo", "Participação efetiva superior à previsão", "T21"))

    entradas22 = "".join(cadastro(i, escola=f"Escola {i}", previstos=1) for i in range(1, 101))
    entradas22 += "1\n5\n0\n"
    r.append(executar(binario, entradas22,
        ["Limite de 100 ações atingido", "Total de ações cadastradas: 100"],
        "Limite de armazenamento", "Cadastro de 100 ações seguido de tentativa da 101ª", "T22"))

    entradas23 = (cadastro(101, escola="Escola A", tema="Saúde mental", previstos=40) +
                  cadastro(102, escola="Escola B", tema="Saúde mental", previstos=30) +
                  "4\n102\n2\n24\n1\n" +
                  cadastro(103, escola="Escola C", tema="Vacinação", previstos=20) +
                  "4\n103\n2\n22\n1\n" +
                  cadastro(104, escola="Escola D", tema="Saúde bucal", previstos=25) +
                  "4\n104\n3\n1\n5\n0\n")
    r.append(executar(binario, entradas23,
        ["Total de ações cadastradas: 4", "Ações planejadas: 1", "Ações realizadas: 2",
         "Ações canceladas: 1", "Participações previstas (todas as ações): 115",
         "Participações previstas (ações realizadas): 50", "Participações efetivas (ações realizadas): 46",
         "Percentual de participação nas ações realizadas: 92.00%"],
        "Cenário de referência", "Cenário fictício de quatro ações definido na primeira entrega", "T23"))

    r.append(executar_reinicio(binario))

    r.append(executar(binario, "1\n801\nEscola Bissexto\nSaúde mental\n29/02/2025\n28/02/2025\nTurma B\nEquipe X\n1\n2\n0\n",
        ["Data inválida", "Data prevista: 28/02/2025"],
        "Validação de data", "29/02/2025 recusada por não ser ano bissexto", "T25"))

    r.append(executar(binario, cadastro(802) + "4\n802\n2\n9\n0\n2\n0\n",
        ["Alteração não confirmada", "Situação: Planejada", "Participações efetivas: 0"],
        "Atualização", "Usuário cancela confirmação de atualização", "T26"))

    r.append(executar(binario, "9\n0\n",
        ["Valor inválido. Informe um inteiro entre 0 e 5", "Encerrando o sistema"],
        "Validação do menu", "Opção 9 inexistente seguida da opção válida 0", "T27"))

    texto_longo = "X" * 81
    entradas28 = (f"1\n803\n{texto_longo}\nEscola Curta\nSaúde mental\n15/09/2026\nTurma C\nEquipe X\n10\n2\n0\n")
    r.append(executar(binario, entradas28,
        ["O texto ultrapassa o limite de 80 bytes", "Escola: Escola Curta"],
        "Validação de tamanho", "Campo escola com 81 caracteres seguido de valor válido", "T28"))

    r.append(executar(binario, "1\n804\nEscola N\nSaúde mental\n15/09/2026\nTurma A\nEquipe X\n10001\n10\n2\n0\n",
        ["Valor inválido", "Participações previstas: 10"],
        "Validação numérica", "Quantidade prevista acima do máximo (10000) seguida de 10", "T29"))

    return r


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, default=ROOT / "pse_em_acao")
    parser.add_argument("--json", type=Path, default=ROOT / "tests" / "resultados_automatizados.json")
    args = parser.parse_args()

    if not args.binary.exists():
        raise SystemExit(f"Binário não encontrado: {args.binary}. Compile src/main.c primeiro.")

    resultados = executar_todos(args.binary.resolve())
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps([asdict(x) for x in resultados], ensure_ascii=False, indent=2), encoding="utf-8")

    for item in resultados:
        print(f"{item.id}: {item.status} — {item.funcionalidade} — {item.obtido}")
    aprovados = sum(x.status == "APROVADO" for x in resultados)
    print(f"\nResultado: {aprovados}/{len(resultados)} testes aprovados.")
    print(f"Relatório JSON: {args.json}")
    return 0 if aprovados == len(resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
