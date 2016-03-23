# coding: utf-8

import csv
import sys

ORIGEM = sys.argv[1]
DESTINO = sys.argv[2]
NOTA_FISCAL = sys.argv[3]
PESO = sys.argv[4]

def main():
    if validar_entrada():
        axado = Axado()
        axado.tabela.exibir_resultado()
        axado.tabela2.exibir_resultado()

def validar_entrada():
    if not ORIGEM:
        print 'Por favor, digite a cidade de origem.'
        return False
    if not DESTINO:
        print 'Por favor, digite a cidade de destino.'
        return False
    if not NOTA_FISCAL:
        print 'Por favor, digite o valor da nota fiscal.'
        return False
    if not PESO:
        print 'Por favor, digite o valor do peso do produto.'
        return False
    return True

class Axado(object):

    def __init__(self):
        self.tabela = Tabela()
        self.tabela2 = Tabela2()

class TabelaBase(object):
    
    PRECO_POR_KG_CSV = 'preco_por_kg.csv'
    ROTAS_CSV = 'rotas.csv'

    def __init__(self, diretorio):
        self.diretorio = diretorio
        self.rota = self.busca_rota()
        self.preco_kg_rota = self.busca_preco_kg()

    def busca_preco_kg(self):
        url = self.diretorio + self.PRECO_POR_KG_CSV
        with open(url) as arquivo:
            preco_kg = csv.DictReader(arquivo)
            for pkg in preco_kg:
                if self.esta_no_intervalo(pkg):
                    return pkg['preco']

    def esta_no_intervalo(self, pkg):
        inicial = self.formata_valor(pkg['inicial'])
        final = self.formata_valor(pkg['final'])
        return (pkg['nome'] == self.rota['kg'] and
               inicial <= float(PESO) and
               (final > float(PESO) or pkg['final'] == ''))

    def busca_rota(self):
        url = self.DIRETORIO + self.ROTAS_CSV
        with open(url) as arquivo:
            rotas = csv.DictReader(arquivo)
            for rota in rotas:
                if rota['origem'] == ORIGEM and rota['destino'] == DESTINO:
                    return rota

    def calcula_seguro(self):
        seguro_rota = self.formata_valor(self.rota['seguro'])
        seguro = self.formata_valor(NOTA_FISCAL) * seguro_rota / 100
        return seguro

    def calcula_kg(self):
        pkg_rota = self.formata_valor(self.preco_kg_rota)
        kg = pkg_rota * float(PESO)
        return kg

    def formata_valor(self, valor):
        try:
            return round(float(valor),2)
        except:
            return 0


class Tabela(TabelaBase):

    DIRETORIO = 'tabela/'

    def __init__(self):
        super(Tabela, self).__init__(self.DIRETORIO) 

    def calcular_icms(self):
        return 6

    def calcular_frete(self):
        seguro = self.calcula_seguro()
        fixa = self.formata_valor(self.rota['fixa'])
        peso = self.calcula_kg()
        icms = self.calcular_icms()
        subtotal = seguro + fixa + peso
        total = subtotal / (self.formata_valor((100 - icms)) / 100)
        return total

    def exibir_resultado(self):
        frete = self.calcular_frete()
        frete = '%.2f' % frete
        prazo = self.rota['prazo']
        pasta = self.DIRETORIO.replace('/','')
        print pasta + ':' + prazo + ', ' + frete


class Tabela2(TabelaBase):

    DIRETORIO = 'tabela2/'

    def __init__(self):
        super(Tabela2, self).__init__(self.DIRETORIO) 

    def limite_aceitavel(self):
        limite = self.formata_valor(self.rota['limite'])
        if limite and float(PESO) > limite:
            return False
        return True

    def calcular_icms(self):
        return self.formata_valor(self.rota['icms'])

    def calcular_alfandega(self, subtotal):
        alfandega = subtotal * (self.formata_valor(self.rota['alfandega']) / 100)
        return alfandega

    def calcular_frete(self):
        seguro = self.calcula_seguro()
        peso = self.calcula_kg()
        icms = self.calcular_icms()
        subtotal = seguro + peso
        alfandega = self.calcular_alfandega(subtotal)
        subtotal = subtotal + alfandega
        total = subtotal / (self.formata_valor((100 - icms)) / 100)
        return total

    def exibir_resultado(self):
        if self.limite_aceitavel():
            frete = self.calcular_frete()
            frete = '%.2f' % frete
            prazo = self.rota['prazo']
        else:
            frete = '-'
            prazo = '-'
        pasta = self.DIRETORIO.replace('/','')
        print pasta + ':' + prazo + ', ' + frete


if __name__ == "__main__":
    main()
