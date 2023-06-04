import sys
import lexico
import sintatico
from pprint import pprint


def main():
    predictive_table = "tabelaAnalisePreditiva.csv"
    productions_vector = "producoes.csv"
    expression = lexico.ler_arquivo('teste.txt')

    parser = sintatico.Sintatico(predictive_table, productions_vector)

    parser.parse(expression)


if __name__ == "__main__":
    sys.exit(main())
