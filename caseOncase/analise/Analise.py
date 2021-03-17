import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

class Analise(object):
    def __init__(self):
        self.arquivoDadosJson = f'{Path(__file__).parent.parent}/arquivos/dados.json'
        self.dirChart = f'{Path(__file__).parent.parent}/graficos'

    def convertToDataFrame(self):
        dfJson = pd.read_json(self.arquivoDadosJson)

        return dfJson

    def analiseStatus(self, arquivo):
        qtd_status = arquivo.groupby(['status']).count()

        eixox = [x for x in qtd_status.index]
        eixoy = [y for y in qtd_status['url']]

        return eixox, eixoy

    def statusBarChart(self, x, y):
        plt.figure()
        plt.bar(x, y)
        plt.xticks(rotation=25)
        plt.title('Distribuicao dos comentarios das noticias')
        plt.xlabel('Status')
        plt.ylabel('Quantidade')
        plt.subplots_adjust(bottom=0.2)
        plt.savefig(f'{self.dirChart}/statusComentario.png', dpi=200)
        plt.close()

    def analiseEvolution(self, arquivo):
        arquivo = arquivo[['ano', 'title']]
        titulos = [titulo for titulo in arquivo['title']]
        anos = [ano for ano in arquivo['ano']]

        dados = [f'{titulos[i]}|{anos[i]}' for i in range(0, len(titulos))]

        dados = list(set(dados))

        dados = [dado.split('|') for dado in dados]

        dados = pd.DataFrame(dados, columns=['qtd', 'ano'])
        dados = dados.groupby(['ano']).count()

        eixox = [x for x in dados.index]
        eixoy = [y for y in dados['qtd']]

        return eixox, eixoy

    def evolutionLineChart(self, x, y):

        plt.figure()
        plt.plot(x, y, marker='o')
        plt.title('Quantidade de noticias postadas ao ano')
        plt.xlabel('Anos')
        plt.ylabel('Quantidade')
        plt.savefig(f'{self.dirChart}/quantidadeNoticiaAno.png', dpi=200)
        plt.close()
        # plt.show()

    def analiseEvolutionYearMonth(self, arquivo):
        dados = arquivo[['ano', 'numero_mes', 'mes', 'title']]

        anos = [ano for ano in arquivo['ano']]
        numeros_meses = [numero_mes for numero_mes in arquivo['numero_mes']]
        meses = [mes for mes in arquivo['mes']]
        titulos = [titulo for titulo in arquivo['title']]

        dados = [f'{anos[i]}|{numeros_meses[i]}|{meses[i]}|{titulos[i]}' for i in range(0, len(titulos))]

        dados = list(set(dados))

        dados = [dado.split('|') for dado in dados]

        dados = pd.DataFrame(dados, columns=['ano', 'numero_mes', 'mes', 'title'])
        dados = dados.groupby(['ano', 'numero_mes', 'mes']).count()

        anos = [x[0] for x in dados.index]
        num_mes = [x[1] for x in dados.index]
        meses = [x[2] for x in dados.index]
        ano_mes = [f'{anos[i]}/{num_mes[i]}' for i in range(0, len(anos))]
        qtd = [y for y in dados['title']]

        anomes = pd.to_datetime(pd.to_datetime(ano_mes))

        dict_dados = {'anos': anos, 'meses': meses, 'anomes': anomes, 'qtd': qtd}

        dados = pd.DataFrame(dict_dados)

        dados = dados.sort_values(by='anomes')

        self.drillDownMonthYear(dados=dados)

    def drillDownMonthYear(self, dados):
        anos = list(set(dados['anos']))

        for i in anos:

            dataset, meses, qtd = [], [], []

            dataset = dados[dados['anos'] == i]
            meses = [x for x in dataset['meses']]
            qtd = [x for x in dataset['qtd']]

            # plt.figure()
            plt.plot(meses, qtd, marker='o')
            plt.xticks(rotation=35)
            plt.title(f'Quantidade de noticias postadas no ano de {i} - Total: {sum(qtd)}.')
            plt.xlabel('Meses')
            plt.ylabel('Quantidade')
            plt.subplots_adjust(bottom=0.2)
            plt.savefig(f'{self.dirChart}/quantidadeNoticiaEm_{i}.png', dpi=200)
            plt.close()

    def executar(self):
        # Conversão de arquivo JSON para CSV
        arquivo = self.convertToDataFrame()

        # Monta dados para bar chart
        eixox, eixoy = self.analiseStatus(arquivo=arquivo)
        self.statusBarChart(eixox, eixoy)

        # Monta dados para line chart
        eixox, eixoy = self.analiseEvolution(arquivo=arquivo)
        self.evolutionLineChart(x=eixox, y=eixoy)

        # Evolucao da categoria nos anos
        # Esse gráfico possue uma iteração com drilldown
        self.analiseEvolutionYearMonth(arquivo=arquivo)

if __name__ == '__main__':
    Analise().executar()
