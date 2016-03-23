# coding: utf-8

import csv
import sys

def main():
    if validar_entrada():
        axado = Axado()
        axado.tabela.exibir_resultado()
        axado.tabela2.exibir_resultado()

# Valida se todos os parâmetros foram passados e se os campos de nota fiscal e peso
# são valores numéricos
def validar_entrada():
    if len(sys.argv) != 5:
        print u'\n Atenção! O formato de entrada deve ser: <origem> <destino> <nota_fiscal> <peso>\n'
        return False
    try:
        nota = float(sys.argv[3])
    except:
        print u'\n Atenção! O valor referente à nota fiscal deve ser um valor numérico.\n'
        return False
    try:
        peso = float(sys.argv[4])
    except:
        print u'\n Atenção! O valor referente ao peso deve ser um valor numérico.\n'
        return False
    return True

# Classe para agrupar os objetos das tabelas
class Axado(object):

    def __init__(self):
        self.tabela = Tabela()
        self.tabela2 = Tabela2()

# Classe base com informações comuns às duas tabelas
class TabelaBase(object):
    
    ORIGEM = sys.argv[1]
    DESTINO = sys.argv[2]
    NOTA_FISCAL = 0
    PESO = 0
    PRECO_POR_KG_CSV = 'preco_por_kg.csv'
    ROTAS_CSV = 'rotas.csv'

    def __init__(self, diretorio):
        self.NOTA_FISCAL = self.formata_valor(sys.argv[3])
        self.PESO = self.formata_valor(sys.argv[4])
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
               inicial <= self.PESO and
               (final > self.PESO or final == 0))

    def busca_rota(self):
        url = self.DIRETORIO + self.ROTAS_CSV
        with open(url) as arquivo:
            rotas = csv.DictReader(arquivo)
            for rota in rotas:
                if rota['origem'] == self.ORIGEM and rota['destino'] == self.DESTINO:
                    return rota

    def calcula_seguro(self):
        seguro_rota = self.formata_valor(self.rota['seguro'])
        seguro = self.NOTA_FISCAL * seguro_rota / 100
        return seguro

    def calcula_kg(self):
        pkg_rota = self.formata_valor(self.preco_kg_rota)
        kg = pkg_rota * self.PESO
        return kg

    def formata_valor(self, valor):
        try:
            return round(float(valor),2)
        except:
            return 0

# Classe responsável por operar informações da tabela
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


# Classe responsável por operar informações da tabela2
class Tabela2(TabelaBase):

    DIRETORIO = 'tabela2/'

    def __init__(self):
        super(Tabela2, self).__init__(self.DIRETORIO) 

    def limite_aceitavel(self):
        limite = self.formata_valor(self.rota['limite'])
        if limite and self.PESO > limite:
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
