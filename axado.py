# coding: utf-8

import csv
import sys

def main():
    axado = Axado()
    print 'Teste ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4]


class Axado(object):

    def __init__(self):
        self.tabela = Tabela()
        self.tabela2 = Tabela2()

class TabelaBase(object):
    
    PRECO_POR_KG_CSV = 'preco_por_kg.csv'
    ROTAS_CSV = 'rotas.csv'

    def __init__(self, diretorio):
        self.preco_kg = self.carrega_csv(diretorio+self.PRECO_POR_KG_CSV)
        self.rotas = self.carrega_csv(diretorio+self.ROTAS_CSV)

    def carrega_csv(self, url):
        with open(url) as arquivo:
            leitor = csv.DictReader(arquivo)
        return leitor


class Tabela(TabelaBase):

    DIRETORIO = 'tabela/'

    def __init__(self):
        super(Tabela, self).__init__(self.DIRETORIO) 


class Tabela2(TabelaBase):

    DIRETORIO = 'tabela2/'

    def __init__(self):
        super(Tabela2, self).__init__(self.DIRETORIO) 


if __name__ == "__main__":
    main()
