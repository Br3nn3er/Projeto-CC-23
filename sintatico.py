import numpy as np
import csv
import lexico as lex

# csv_filename = 'my_file.csv'
# with open(csv_filename) as f:
#     reader = csv.reader(f)
#     lst = list(reader)
# table = np.array(lst)


class Sintatico:
    def __init__(self, filename):
        self.table = {}
        with open(filename, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                non_terminal = row[0]
                self.table[non_terminal] = {}
                for i in range(1, len(row)):
                    terminal = headers[i]
                    production = row[i]
                    self.table[non_terminal][terminal] = production

    def parse(self, expression):
        # self.lexico = Lexico(expression)
        self.stack = []
        self.stack.append("$")
        self.stack.append("S")  # Símbolo inicial da gramática
        self.current_token = lex.get_nex_token(expression)

        while len(self.stack) > 0:
            top = self.stack[-1]
            if top in self.table and self.current_token in self.table[top]:
                production = self.table[top][self.current_token]
                self.stack.pop()
                if production != "epsilon":
                    production_symbols = production.split()[::-1]
                    self.stack.extend(production_symbols)
            elif top == self.current_token:
                self.stack.pop()
                self.current_token = lex.get_nex_token(expression)
            else:
                raise Exception("Erro de sintaxe. Token inesperado: " + self.current_token)

        if self.current_token is None:
            print("Análise sintática concluída com sucesso.")
        else:
            raise Exception("Erro de sintaxe. Fim inesperado da expressão.")


# Exemplo de uso
filename = "tabela_analise.csv"
expression = "a + b * c"

parser = Sintatico(filename)
parser.parse(expression)