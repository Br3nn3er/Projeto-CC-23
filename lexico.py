from collections import namedtuple
from pprint import pprint

pos = 0
line = 1
table = {}


def is_eof(data: str):
    global pos
    return pos > len(data)


def verifica_letra(caractere):
    if caractere.isalpha():
        return True
    else:
        return False


def verifica_espaco(caractere):
    if caractere.isspace():
        return True
    else:
        return False


def verifica_numero(caractere):
    if caractere.isdigit():
        return True
    else:
        return False


def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
        if conteudo is None:
            print('Arquivo vazio')
        return conteudo
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None


def get_nex_token(info):
    Token = namedtuple("Token", ["type", "value", "sint"])
    state = 0

    global pos, c
    global line
    global table

    tk_value = ''

    if is_eof(info):
        return None

    while len(info):
        if is_eof(info):
            return None
        # if info[-1] == c:
        #     return None

        if len(info) != pos:
            c = info[pos]
        pos += 1
        match state:
            case 0:
                if c == 's':
                    state = 69
                    tk_value += c
                elif c == 'e':
                    state = 41
                    tk_value += c
                elif c == 'i':
                    state = 54
                    tk_value += c
                elif c == 'f':
                    state = 76
                    tk_value += c
                elif c == 'c':
                    state = 58
                    tk_value += c
                elif c == 'a':
                    state = 63
                    tk_value += c
                elif c == '+':
                    state = 1
                    tk_value += c
                elif c == '-':
                    state = 2
                    tk_value += c
                elif c == '/':
                    state = 4
                    tk_value += c
                elif c == '*':
                    state = 3
                    tk_value += c
                elif c == '^':
                    state = 9
                    tk_value += c
                elif c == ';':
                    state = 10
                    tk_value += c
                elif c == ',':
                    state = 11
                    tk_value += c
                elif c == ':':
                    state = 12
                    tk_value += c
                elif c == '[':
                    state = 13
                    tk_value += c
                elif c == ']':
                    state = 14
                    tk_value += c
                elif c == ')':
                    state = 15
                    tk_value += c
                elif c == '(':
                    state = 16
                    tk_value += c
                elif c == '=':
                    state = 17
                    tk_value += c
                elif c == '>':
                    state = 18
                    tk_value += c
                elif c == '<':
                    state = 21
                    tk_value += c
                elif c == '{':
                    state = 25
                    tk_value += c
                elif c == '}':
                    state = 26
                    tk_value += c
                elif c == '\'':
                    state = 27
                    tk_value += c
                elif verifica_letra(c):
                    state = 67
                    tk_value += c
                elif verifica_numero(c):
                    state = 32
                    tk_value += c
                elif verifica_espaco(c):
                    if c == '\n':
                        line += 1
                    state = 30
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 1:
                tk = Token('MAIS', tk_value, '+')
                pos -= 1
                return tk
            case 2:
                tk = Token('MENOS', tk_value, '-')
                pos -= 1
                return tk
            case 3:
                tk = Token('MULT', tk_value, '*')
                pos -= 1
                return tk
            case 4:
                if c == '*':
                    state = 6
                    tk_value += c
                elif verifica_letra(c) or verifica_numero(c):
                    state = 5
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 5:
                tk_value = tk_value[:-1]
                tk = Token('DIV', tk_value, '/')
                pos -= 2
                return tk
            case 6:
                if verifica_letra(c) or verifica_numero(c):
                    state = 6
                    tk_value += c
                elif c == '*':
                    state = 7
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 7:
                if c == '/':
                    state = 8
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 8:
                tk = Token('COMENTARIO', tk_value, 'comment')
                pos -= 1
                # return tk
                state = 0
            case 9:
                tk = Token('EXPO', tk_value, '^')
                pos -= 1
                return tk
            case 10:
                tk = Token('PONTO_VIRG', tk_value, ';')
                pos -= 1
                return tk
            case 11:
                tk = Token('VIRGULA', tk_value, ',')
                pos -= 1
                return tk
            case 12:
                tk = Token('DOIS_PONTOS', tk_value, ':')
                pos -= 1
                return tk
            case 13:
                tk = Token('ABRE_COLCHETE', tk_value, '[')
                pos -= 1
                return tk
            case 14:
                tk = Token('FECHA_COLCHETE', tk_value, ']')
                pos -= 1
                return tk
            case 15:
                tk = Token('FECHA_PARENTESE', tk_value, ')')
                pos -= 1
                return tk
            case 16:
                tk = Token('ABRE_PARENTESE', tk_value, '(')
                pos -= 1
                return tk
            case 17:
                tk = Token('IGUAL', tk_value, '=')
                pos -= 1
                return tk
            case 18:
                if c == '=':
                    state = 20
                    tk_value += c
                elif c != '=':
                    state = 19
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 19:
                tk_value = tk_value[:-1]
                tk = Token('MAIOR', tk_value, '>')
                pos -= 2
                return tk
            case 20:
                tk = Token('MAIOR_IGUAL', tk_value, '>=')
                pos -= 1
                return tk
            case 21:
                if c == '=':
                    state = 24
                    tk_value += c
                elif c == '<':
                    state = 23
                    tk_value += c
                elif c != '<' and c != '=':
                    state = 22
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 22:
                tk_value = tk_value[:-1]
                tk = Token('MENOR', tk_value, '<')
                pos -= 2
                return tk
            case 23:
                tk = Token('DIFF', tk_value, '!=')
                pos -= 1
                return tk
            case 24:
                tk = Token('MENOR_IGUAL', tk_value, '<=')
                pos -= 1
                return tk
            case 25:
                tk = Token('ABRE_CHAVE', tk_value, '{')
                pos -= 1
                return tk
            case 26:
                tk = Token('FECHA_CHAVE', tk_value, '}')
                pos -= 1
                return tk
            case 27:
                if verifica_letra(c) or verifica_numero(c):
                    state = 28
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 28:
                if c == '\'':
                    state = 28
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 29:
                tk_value = tk_value[:-1]
                tk = Token('CARACTERE', tk_value, 'caracter')
                pos -= 2
                table[tk.value] = tk.type
                return tk
            case 30:
                if verifica_espaco(c):
                    if c == '\n':
                        line += 1
                    state = 30
                    tk_value += c
                elif not verifica_espaco(c):
                    state = 31
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 31:
                tk_value = tk_value[:-1]
                tk = Token('WS', tk_value, 'ws')
                pos -= 2
                tk_value = ''
                state = 0
                # return tk
            case 32:
                if verifica_numero(c):
                    state = 32
                    tk_value += c
                elif c == 'E':
                    state = 37
                    tk_value += c
                elif c == '.':
                    state = 34
                    tk_value += c
                elif not verifica_numero(c) and c != 'E' and c != '.':
                    state = 33
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 33:
                tk_value = tk_value[:-1]
                tk = Token('INTEIRO', tk_value, 'numero')
                pos -= 2
                table[tk.value] = tk.type
                return tk
            case 34:
                if verifica_numero(c):
                    state = 35
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 35:
                if verifica_numero(c):
                    state = 35
                    tk_value += c
                elif c == 'E':
                    state = 37
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 36:
                tk_value = tk_value[:-1]
                tk = Token('DECIMAL', tk_value, 'numero')
                pos -= 2
                table[tk.value] = tk.type
                return tk
            case 37:
                if c == '+' or c == '-':
                    state = 38
                    tk_value += c
                elif verifica_numero(c):
                    state = 39
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 38:
                if verifica_numero(c):
                    state = 39
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 39:
                if verifica_numero(c):
                    state = 39
                    tk_value += c
                elif not verifica_numero(c):
                    state = 40
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 40:
                tk_value = tk_value[:-1]
                tk = Token('CIENTIFICO', tk_value, 'numero')
                pos -= 2
                table[tk.value] = tk.type
                return tk
            case 41:
                if c == 'n':
                    state = 42
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 42:
                if c == 'q':
                    state = 43
                    tk_value += c
                elif c == 't':
                    state = 50
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 43:
                if c == 'u':
                    state = 44
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 44:
                if c == 'a':
                    state = 45
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 45:
                if c == 'n':
                    state = 46
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 46:
                if c == 't':
                    state = 47
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 47:
                if c == 'o':
                    state = 48
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 48:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 49
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 49:
                tk_value = tk_value[:-1]
                tk = Token('ENQUANTO', tk_value, 'enquanto')
                pos -= 2
                return tk
            case 50:
                if c == 'a':
                    state = 51
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 51:
                if c == 'o':
                    state = 52
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 52:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 53
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 53:
                tk_value = tk_value[:-1]
                tk = Token('ENTAO', tk_value, 'entao')
                pos -= 2
                return tk
            case 54:
                if c == 'n':
                    state = 55
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 55:
                if c == 't':
                    state = 56
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 56:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 57
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")

            case 57:
                tk_value = tk_value[:-1]
                tk = Token('INT', tk_value, 'int')
                pos -= 2
                return tk
            case 58:
                if c == 'h':
                    state = 59
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 59:
                if c == 'a':
                    state = 60
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 60:
                if c == 'r':
                    state = 61
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 61:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 62
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 62:
                tk_value = tk_value[:-1]
                tk = Token('CHAR', tk_value, 'char')
                pos -= 2
                return tk
            case 63:
                if c == 't':
                    state = 64
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif verifica_espaco(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 64:
                if c == 'e':
                    state = 65
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 65:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 66
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 66:
                tk_value = tk_value[:-1]
                tk = Token('ATE', tk_value, 'ate')
                pos -= 2
                return tk
            case 67:
                if verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 68:
                tk_value = tk_value[:-1]
                tk = Token('ID', tk_value, 'id')
                pos -= 2
                table[tk.value] = tk.type
                return tk
            case 69:
                if c == 'e':
                    state = 70
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 70:
                if c == 'n':
                    state = 72
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 71
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 71:
                tk_value = tk_value[:-1]
                tk = Token('SE', tk_value, 'se')
                pos -= 2
                return tk
            case 72:
                if c == 'a':
                    state = 73
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 73:
                if c == 'o':
                    state = 73
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 74:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 75
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 75:
                tk_value = tk_value[:-1]
                tk = Token('SENAO', tk_value, 'senao')
                pos -= 2
                return tk
            case 76:
                if c == 'u':
                    state = 77
                    tk_value += c
                elif c == 'a':
                    state = 85
                    tk_value += c
                elif c == 'l':
                    state = 89
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 77:
                if c == 'n':
                    state = 78
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 78:
                if c == 'c':
                    state = 79
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 79:
                if c == 't':
                    state = 80
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 80:
                if c == 'i':
                    state = 81
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 81:
                if c == 'o':
                    state = 82
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 82:
                if c == 'n':
                    state = 83
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 83:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 84
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 84:
                tk_value = tk_value[:-1]
                tk = Token('FUNCTION', tk_value, 'function')
                pos -= 2
                return tk
            case 85:
                if c == 'c':
                    state = 86
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 86:
                if c == 'a':
                    state = 87
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 87:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 88
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 88:
                tk_value = tk_value[:-1]
                tk = Token('FACA', tk_value, 'faca')
                pos -= 2
                return tk
            case 89:
                if c == 'o':
                    state = 90
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 90:
                if c == 'a':
                    state = 91
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 91:
                if c == 't':
                    state = 92
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 92:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 93
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 93:
                tk_value = tk_value[:-1]
                tk = Token('FLOAT', tk_value, 'float')
                pos -= 2
                return tk
            case 94:
                if c == 'e':
                    state = 95
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 95:
                if c == 'p':
                    state = 96
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 96:
                if c == 'i':
                    state = 97
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 97:
                if c == 't':
                    state = 98
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 98:
                if c == 'a':
                    state = 92
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                elif not verifica_numero(c) or not verifica_letra(c):
                    state = 68
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 99:
                if not verifica_numero(c) or not verifica_letra(c):
                    state = 100
                    tk_value += c
                elif verifica_numero(c) or verifica_letra(c):
                    state = 67
                    tk_value += c
                else:
                    raise Exception(f"Lexical Exception: Illegal character at line {line}: {c}")
            case 100:
                tk_value = tk_value[:-1]
                tk = Token('REPITA', tk_value, 'repita')
                pos -= 2
                return tk



# info = '7I7'
# # while True:
# lex = Lexico()
# test = get_nex_token(info)
# pprint(test)
