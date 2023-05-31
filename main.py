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


if __name__ == "__main__":
    sys.exit(main())
