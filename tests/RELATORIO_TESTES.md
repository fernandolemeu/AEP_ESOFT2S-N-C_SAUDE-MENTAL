# Relatório de testes funcionais — PSE em Ação
**Método:** testes de caixa-preta com entradas simuladas no terminal e conferência das mensagens/valores produzidos.
**Resultado:** 29/29 aprovados; 0 falharam.

| ID | Funcionalidade | Cenário | Resultado |
|---|---|---|---|
| T01 | Cadastro/listagem | Cadastro válido e listagem | APROVADO |
| T02 | Código duplicado | Código repetido recusado e novo código aceito | APROVADO |
| T03 | Validação de texto | Campo escola vazio seguido de valor válido | APROVADO |
| T04 | Validação de texto | Campo contendo apenas espaços | APROVADO |
| T05 | Limite de texto | Texto com 81 caracteres recusado | APROVADO |
| T06 | Validação numérica | Letras no campo código recusadas | APROVADO |
| T07 | Validação numérica | Código fora da faixa recusado | APROVADO |
| T08 | Validação de data | Data 31/02/2026 recusada | APROVADO |
| T09 | Validação de data | 29/02 em ano não bissexto recusado | APROVADO |
| T10 | Validação de data | 29/02 em ano bissexto aceito | APROVADO |
| T11 | Listagem | Listar sem registros | APROVADO |
| T12 | Pesquisa por código | Código existente encontrado | APROVADO |
| T13 | Pesquisa por código | Código inexistente não encontrado | APROVADO |
| T14 | Pesquisa por escola | Busca por parte do nome da escola | APROVADO |
| T15 | Pesquisa por tema | Busca por parte do tema | APROVADO |
| T16 | Pesquisa | Pesquisa textual sem correspondência | APROVADO |
| T17 | Atualização | Atualizar para realizada e registrar efetivos | APROVADO |
| T18 | Atualização | Código inexistente ao atualizar | APROVADO |
| T19 | Atualização | Cancelar confirmação mantém os dados anteriores | APROVADO |
| T20 | Atualização | De realizada para planejada zera efetivos | APROVADO |
| T21 | Atualização | De realizada para cancelada zera efetivos | APROVADO |
| T22 | Resumo | Resumo com ações planejada, realizada e cancelada | APROVADO |
| T23 | Resumo | Resumo sem registros | APROVADO |
| T24 | Resumo | Previsão zero evita divisão por zero | APROVADO |
| T25 | Resumo | Participações efetivas maiores que previsão | APROVADO |
| T26 | Limite de armazenamento | 101º cadastro é recusado após 100 ações | APROVADO |
| T27 | Validação do menu | Opção 9 inválida e opção 0 encerra | APROVADO |
| T28 | Validação numérica | Previsão acima de 10000 é recusada | APROVADO |
| T29 | Memória/encerramento | Nova execução começa sem registros da execução anterior | APROVADO |

Os testes são reproduzíveis executando `python tests/testes_funcionais.py` a partir da pasta raiz do projeto.
O relatório JSON detalhado é gerado em `tests/resultados_testes.json`.
