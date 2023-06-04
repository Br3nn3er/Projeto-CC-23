import numpy as np
import csv
import lexico as lex
from bigtree import list_to_tree, print_tree


class Sintatico:
    def __init__(self, predictive_table, productions_vector):
        self.table = {}
        self.vector = {}
        with open(predictive_table, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                non_terminal = row[0]
                self.table[non_terminal] = {}
                for i in range(1, len(row)):
                    terminal = headers[i]
                    production = row[i]
                    self.table[non_terminal][terminal] = production

        with open(productions_vector, mode='r') as infile:
            reader = csv.reader(infile, skipinitialspace=True)
            for row in reader:
                k, v = row
                self.vector[k] = v

    def parse(self, expression):
        la = ''
        self.stack = []
        self.stack.append("S")  # Símbolo inicial da gramática
        self.current_token = lex.get_nex_token(expression)
        lista = []
        while len(self.stack) > 0:
            top = self.stack[-1]

            if top in self.table and self.current_token.sint.lower() in self.table[top]:
                la = la + top + '/'
                production = self.table[top][self.current_token.sint.lower()]
                next_symbl = self.vector[production]
                self.stack.pop()
                # verifica vazio
                if production != "4":
                    production_symbols = next_symbl.split(' ')

                    for pd in production_symbols:
                        las = la + pd + '/'
                        lista.append(las[:-1])
                    production_symbols.reverse()
                    for production in production_symbols:
                        self.stack.append(production)

            elif top == self.current_token.sint.lower():
                self.stack.pop()
                self.current_token = lex.get_nex_token(expression)
            else:
                raise Exception(
                    "Syntactic Exception: Token inesperado: " + self.current_token.sint.lower() + ', para os caracteres: ' + self.current_token.value + ' na linha: ' + lex.line)

        if self.current_token is None:
            print("Análise sintática concluída com sucesso.")
            # print('\n Arvore Gerada \n')
            # root = list_to_tree(lista)
            # print_tree(root)
        else:
            raise Exception("Erro de sintaxe. Fim inesperado da expressão.")

