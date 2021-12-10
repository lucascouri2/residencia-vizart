import pandas as pd
from pandas.core.frame import DataFrame
import plotly.graph_objects as go
#from colormap import rgb2hex, hex2rgb, rgb2hsv
from PIL import ImageColor

class Paleta2Vis:

    def __init__(self):
        self.selecaoAtiva = False
        self.ano = 0
    

    # Carrega dados e retorn o dataframe para a visualizacao
    def loadData(self,nomeArtista):
        df = pd.read_csv(f'paletas/final_artistas/paleta_anos_{nomeArtista}.csv')
        df['selecionado'] = False
        return df


    def calcularCordenadas(self, dfPaletaAnos):
        x = list(range(1, 11)) * len(dfPaletaAnos['completitionYear'].unique())
        dfPaletaAnos['ordemVis'] = x
        return list(dfPaletaAnos[['completitionYear','ordemVis','hex','selecionado']].to_records(index=False))


    def calculateCordenadasSelecao(self, dfPaletaAnos, ano):
        copyDf = pd.DataFrame(dfPaletaAnos)
        x = list(range(1, 11)) * len(copyDf['completitionYear'].unique())
        copyDf['ordemVis'] = x

        copyDf.loc[copyDf['completitionYear'] == ano, 'selecionado'] = True
        retorno = list(copyDf[['completitionYear','ordemVis','hex','selecionado']].to_records(index=False))
        #print(retorno)
        return retorno

    # Cria a visualizacao do plotly
    def getPaletaPorAno(self, nomeArtista):
        dfPaletaAnos = self.loadData(nomeArtista)
        coordenadas = self.calcularCordenadas(dfPaletaAnos)
        return self.gerarFigura(coordenadas)

    #Criar visualizacao com click
    def getPaletaPorAnoSelected(self,nomeArtista, ano):
        print("1------>",self.selecaoAtiva)
        dfPaletaAnos = self.loadData(nomeArtista)
        self.ano = ano
        if(self.selecaoAtiva):
            coordenadas = self.calculateCordenadasSelecao(dfPaletaAnos, ano)
        else:
            coordenadas = self.calcularCordenadas(dfPaletaAnos)
            
        return self.gerarFigura(coordenadas)


    def gerarFigura(self,coordenadas):
        fig = go.Figure()
        for x, y, color, selecionado in coordenadas:
            
            cor_rgb = ImageColor.getcolor(color, "RGB")
            opacity = 1
            if(self.selecaoAtiva):
                opacity = 1 if selecionado else .4

            fig.add_trace(
                go.Scatter(
                    name = '',
                    mode='markers',
                    x=[x],
                    y=[y],
                    hovertemplate = 'Ano: %{x}<br>RGB: %{text}',#'Ano: %{x}<br>RGB: %{cor}',
                    text = [cor_rgb], #se quiser o hexa é só usar [color]
                    #text = ['Custom text {}'.format(i + 1) for i in range(5)],
                    marker_symbol='square',
                    marker=dict(
                        color= color,
                        size=21,
                        opacity=opacity,
                    ),
                    showlegend=False
                )
            )

        titulo='Paleta de cores ao longo dos anos'
        eixox='Ano'
        eixoy='Cores'
        fig.update_layout(
            title=titulo,
            xaxis_title=eixox,
            yaxis_title=eixoy,
            #yaxis_visible=False, 
            yaxis_showticklabels=False,
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )

        return fig
