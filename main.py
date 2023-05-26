import sys
import lexico
from pprint import pprint


def main():
    info = lexico.ler_arquivo('teste.txt')
    try:
        test = lexico.get_nex_token(info)
        pprint(test)
        test = lexico.get_nex_token(info)
        pprint(test)
        test = lexico.get_nex_token(info)
        pprint(test)
    except Exception as ve:
        return str(ve)


# class Main:
#     def __init__(self):
#         scanner = lexico.ler_arquivo('teste_lexico.txt')
#         lex = lexico.Lexico()


if __name__ == "__main__":
    sys.exit(main())
