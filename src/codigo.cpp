#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAPACIDADE 100
#define TAM_TEXTO 81
#define TAM_DATA 11
#define TAM_LINHA 200

typedef struct {
    int codigo;
    char escola[TAM_TEXTO];
    char tema[TAM_TEXTO];
    char dataPrevista[TAM_DATA];
    char publicoAlvo[TAM_TEXTO];
    char responsavel[TAM_TEXTO];
    int previstos;
    int situacao;
    int efetivos;
} Acao;

/* Le um numero inteiro e verifica se ele esta dentro do intervalo. */
int lerInteiro(char mensagem[], int minimo, int maximo) {
    int valor;
    int resultado;
    int caractere;
    int entradaInvalida;

    while (1) {
        printf("%s: ", mensagem);
        resultado = scanf("%d", &valor);

        if (resultado == EOF) {
            printf("\nEntrada encerrada. Finalizando o programa.\n");
            exit(0);
        }

        entradaInvalida = 0;

        while ((caractere = getchar()) != '\n' && caractere != EOF) {
            if (caractere != ' ' && caractere != '\t' && caractere != '\r') {
                entradaInvalida = 1;
            }
        }

        if (resultado == 1 && entradaInvalida == 0 &&
            valor >= minimo && valor <= maximo) {
            return valor;
        }

        printf("Valor invalido. Digite um numero entre %d e %d.\n",
               minimo, maximo);
    }
}

/* Le um texto e verifica se o campo nao esta vazio. */
void lerTexto(char mensagem[], char destino[], int tamanho) {
    char linha[TAM_LINHA];
    int i;
    int temLetra;
    int caractere;

    while (1) {
        printf("%s: ", mensagem);

        if (fgets(linha, TAM_LINHA, stdin) == NULL) {
            printf("\nEntrada encerrada. Finalizando o programa.\n");
            exit(0);
        }

        if (strchr(linha, '\n') == NULL && !feof(stdin)) {
            while ((caractere = getchar()) != '\n' && caractere != EOF) {
            }

            printf("Texto muito longo. Tente novamente.\n");
            continue;
        }

        linha[strcspn(linha, "\n")] = '\0';

        temLetra = 0;

        for (i = 0; linha[i] != '\0'; i++) {
            if (linha[i] != ' ' && linha[i] != '\t' && linha[i] != '\r') {
                temLetra = 1;
            }
        }

        if (temLetra == 0) {
            printf("Este campo nao pode ficar vazio.\n");
        } else if ((int)strlen(linha) >= tamanho) {
            printf("O texto deve ter no maximo %d caracteres.\n", tamanho - 1);
        } else {
            strcpy(destino, linha);
            return;
        }
    }
}

/* Verifica se a data existe no calendario. */
int dataValida(char data[]) {
    int dia, mes, ano;
    int diasNoMes;
    int i;

    if (strlen(data) != 10 || data[2] != '/' || data[5] != '/') {
        return 0;
    }

    for (i = 0; i < 10; i++) {
        if (i != 2 && i != 5 && (data[i] < '0' || data[i] > '9')) {
            return 0;
        }
    }

    dia = (data[0] - '0') * 10 + (data[1] - '0');
    mes = (data[3] - '0') * 10 + (data[4] - '0');

    ano = (data[6] - '0') * 1000 +
          (data[7] - '0') * 100 +
          (data[8] - '0') * 10 +
          (data[9] - '0');

    if (ano < 1900 || ano > 9999 || mes < 1 || mes > 12 || dia < 1) {
        return 0;
    }

    if (mes == 4 || mes == 6 || mes == 9 || mes == 11) {
        diasNoMes = 30;
    } else if (mes == 2) {
        diasNoMes = 28;

        if (ano % 400 == 0 || (ano % 4 == 0 && ano % 100 != 0)) {
            diasNoMes = 29;
        }
    } else {
        diasNoMes = 31;
    }

    if (dia > diasNoMes) {
        return 0;
    }

    return 1;
}

/* Procura uma acao pelo codigo. */
int localizarCodigo(Acao acoes[], int total, int codigo) {
    int i;

    for (i = 0; i < total; i++) {
        if (acoes[i].codigo == codigo) {
            return i;
        }
    }

    return -1;
}

/* Mostra os dados de uma acao. */
void mostrarAcao(Acao acao) {
    printf("\n----------------------------------------\n");
    printf("Codigo: %d\n", acao.codigo);
    printf("Escola: %s\n", acao.escola);
    printf("Tema: %s\n", acao.tema);
    printf("Data prevista: %s\n", acao.dataPrevista);
    printf("Publico-alvo: %s\n", acao.publicoAlvo);
    printf("Responsavel: %s\n", acao.responsavel);
    printf("Participacoes previstas: %d\n", acao.previstos);

    if (acao.situacao == 1) {
        printf("Situacao: Planejada\n");
    } else if (acao.situacao == 2) {
        printf("Situacao: Realizada\n");
    } else {
        printf("Situacao: Cancelada\n");
    }

    printf("Participacoes efetivas: %d\n", acao.efetivos);
    printf("----------------------------------------\n");
}

/* Cadastra uma nova acao. */
int cadastrar(Acao acoes[], int total) {
    Acao nova;

    if (total >= CAPACIDADE) {
        printf("Limite de 100 acoes atingido.\n");
        return total;
    }

    while (1) {
        nova.codigo = lerInteiro("Codigo (1 a 999999)", 1, 999999);

        if (localizarCodigo(acoes, total, nova.codigo) == -1) {
            break;
        }

        printf("Este codigo ja esta cadastrado. Digite outro.\n");
    }

    lerTexto("Escola ficticia", nova.escola, TAM_TEXTO);
    lerTexto("Tema da acao", nova.tema, TAM_TEXTO);

    while (1) {
        lerTexto("Data prevista (DD/MM/AAAA)", nova.dataPrevista, TAM_DATA);

        if (dataValida(nova.dataPrevista)) {
            break;
        }

        printf("Data invalida. Verifique o dia, o mes e o ano.\n");
    }

    lerTexto("Publico-alvo coletivo", nova.publicoAlvo, TAM_TEXTO);
    lerTexto("Equipe ou funcao responsavel", nova.responsavel, TAM_TEXTO);

    nova.previstos = lerInteiro("Participacoes previstas (0 a 10000)", 0, 10000);

    nova.situacao = 1;
    nova.efetivos = 0;

    acoes[total] = nova;

    printf("Acao cadastrada com sucesso. Situacao inicial: Planejada.\n");

    return total + 1;
}

/* Mostra todas as acoes cadastradas. */
void listar(Acao acoes[], int total) {
    int i;

    if (total == 0) {
        printf("Nenhuma acao cadastrada.\n");
        return;
    }

    for (i = 0; i < total; i++) {
        mostrarAcao(acoes[i]);
    }
}

/* Pesquisa uma acao por codigo, escola ou tema. */
void pesquisar(Acao acoes[], int total) {
    int tipo;
    int codigo;
    int posicao;
    int i;
    int encontrados = 0;
    char termo[TAM_TEXTO];

    if (total == 0) {
        printf("Nenhuma acao cadastrada para pesquisa.\n");
        return;
    }

    printf("\n1 - Pesquisar por codigo\n");
    printf("2 - Pesquisar por escola\n");
    printf("3 - Pesquisar por tema\n");

    tipo = lerInteiro("Escolha o tipo de pesquisa", 1, 3);

    if (tipo == 1) {
        codigo = lerInteiro("Digite o codigo", 1, 999999);

        posicao = localizarCodigo(acoes, total, codigo);

        if (posicao == -1) {
            printf("Acao nao encontrada.\n");
        } else {
            mostrarAcao(acoes[posicao]);
        }

        return;
    }

    if (tipo == 2) {
        lerTexto("Digite o nome ou parte do nome da escola", termo, TAM_TEXTO);
    } else {
        lerTexto("Digite o tema ou parte do tema", termo, TAM_TEXTO);
    }

    for (i = 0; i < total; i++) {
        if (tipo == 2 && strstr(acoes[i].escola, termo) != NULL) {
            mostrarAcao(acoes[i]);
            encontrados++;
        } else if (tipo == 3 && strstr(acoes[i].tema, termo) != NULL) {
            mostrarAcao(acoes[i]);
            encontrados++;
        }
    }

    if (encontrados == 0) {
        printf("Nenhuma acao encontrada.\n");
    } else {
        printf("Total de acoes encontradas: %d\n", encontrados);
    }
}

/* Atualiza a situacao de uma acao. */
void atualizar(Acao acoes[], int total) {
    int codigo;
    int posicao;
    int novaSituacao;
    int novosEfetivos = 0;
    int confirmar;

    if (total == 0) {
        printf("Nenhuma acao cadastrada para atualizar.\n");
        return;
    }

    codigo = lerInteiro("Digite o codigo da acao", 1, 999999);

    posicao = localizarCodigo(acoes, total, codigo);

    if (posicao == -1) {
        printf("Acao nao encontrada.\n");
        return;
    }

    mostrarAcao(acoes[posicao]);

    printf("1 - Planejada\n");
    printf("2 - Realizada\n");
    printf("3 - Cancelada\n");

    novaSituacao = lerInteiro("Escolha a nova situacao", 1, 3);

    if (novaSituacao == 2) {
        novosEfetivos = lerInteiro("Quantidade de participacoes efetivas (0 a 10000)", 0, 10000);
    } else {
        printf("Ao confirmar, a quantidade efetiva sera alterada para zero.\n");
    }

    confirmar = lerInteiro("Confirmar alteracao? (1 - Sim / 0 - Nao)", 0, 1);

    if (confirmar == 1) {
        acoes[posicao].situacao = novaSituacao;
        acoes[posicao].efetivos = novosEfetivos;

        printf("Acao atualizada com sucesso.\n");
    } else {
        printf("Alteracao cancelada. Os dados anteriores foram mantidos.\n");
    }
}

/* Gera o resumo geral das acoes cadastradas. */
void resumir(Acao acoes[], int total) {
    int i;
    int planejadas = 0;
    int realizadas = 0;
    int canceladas = 0;
    int previstosGeral = 0;
    int previstosRealizadas = 0;
    int efetivos = 0;
    double percentual;

    for (i = 0; i < total; i++) {
        previstosGeral = previstosGeral + acoes[i].previstos;

        if (acoes[i].situacao == 1) {
            planejadas++;
        } else if (acoes[i].situacao == 2) {
            realizadas++;

            previstosRealizadas = previstosRealizadas + acoes[i].previstos;
            efetivos = efetivos + acoes[i].efetivos;
        } else if (acoes[i].situacao == 3) {
            canceladas++;
        }
    }

    printf("\n========== RESUMO GERAL ==========\n");

    printf("Total de acoes cadastradas: %d\n", total);
    printf("Acoes planejadas: %d\n", planejadas);
    printf("Acoes realizadas: %d\n", realizadas);
    printf("Acoes canceladas: %d\n", canceladas);

    printf("Participacoes previstas (todas as acoes): %d\n", previstosGeral);
    printf("Participacoes previstas (acoes realizadas): %d\n", previstosRealizadas);
    printf("Participacoes efetivas (acoes realizadas): %d\n", efetivos);

    if (previstosRealizadas > 0) {
        percentual = (efetivos * 100.0) / previstosRealizadas;

        printf("Percentual de participacao nas acoes realizadas: %.2f%%\n",
               percentual);
    } else {
        printf("Percentual nao calculavel: nao ha previsao nas acoes realizadas.\n");
    }

    printf("==================================\n");
}

/* Mostra o menu principal. */
void mostrarMenu(void) {
    printf("\n========== PSE EM ACAO ==========\n");
    printf("1 - Cadastrar acao\n");
    printf("2 - Listar acoes\n");
    printf("3 - Pesquisar acao\n");
    printf("4 - Atualizar situacao\n");
    printf("5 - Gerar resumo geral\n");
    printf("0 - Sair\n");
    printf("=================================\n");
}

int main(void) {
    Acao acoes[CAPACIDADE];
    int total = 0;
    int opcao;

    do {
        mostrarMenu();

        opcao = lerInteiro("Escolha uma opcao", 0, 5);

        switch (opcao) {
            case 1:
                total = cadastrar(acoes, total);
                break;

            case 2:
                listar(acoes, total);
                break;

            case 3:
                pesquisar(acoes, total);
                break;

            case 4:
                atualizar(acoes, total);
                break;

            case 5:
                resumir(acoes, total);
                break;

            case 0:
                printf("Encerrando o sistema. Os registros serao apagados.\n");
                break;
        }

    } while (opcao != 0);

    return 0;
}
