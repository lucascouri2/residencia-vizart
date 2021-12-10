import pandas as pd
from pandas.core.frame import DataFrame
import plotly.graph_objects as go

# Carrega dados e retorn o dataframe para a visualizacao
def loadData(nomeArtista):
    return pd.read_csv(f'paletas/final_artistas/paleta_anos_{nomeArtista}.csv')


def calcularCordenadas(dfPaletaAnos):
    x = list(range(1, 11)) * len(dfPaletaAnos['completitionYear'].unique())
    dfPaletaAnos['ordemVis'] = x
    return list(dfPaletaAnos[['completitionYear','ordemVis','hex']].to_records(index=False))


def calculateCordenadasSelecao(dfPaletaAnos, ano):
    copyDf = pd.DataFrame(dfPaletaAnos)
    x = list(range(1, 11)) * len(copyDf['completitionYear'].unique())
    copyDf['ordemVis'] = x
    copyDf.loc[copyDf['completitionYear'] == ano, 'hex'] = '#000000'
    retorno = list(copyDf[['completitionYear','ordemVis','hex']].to_records(index=False))
    print(retorno)
    return retorno

# Cria a visualizacao do plotly
def getPaletaPorAno(nomeArtista):
    dfPaletaAnos = loadData(nomeArtista)

    coordenadas = calcularCordenadas(dfPaletaAnos)
    fig = go.Figure()
    for x, y, color in coordenadas:
        fig.add_trace(
            go.Scatter(
                mode='markers',
                x=[x],
                y=[y],
                marker_symbol='square',
                marker=dict(
                    color= color,
                    size=21,
                    # line=dict(
                    #     color='grey',
                    #     width=1
                    # )
                ),
                showlegend=False
            )
        )

    return fig

def getPaletaPorAnoSelected(nomeArtista, ano):
    dfPaletaAnos = loadData(nomeArtista)
    coordenadas = calculateCordenadasSelecao(dfPaletaAnos, ano)
    fig = go.Figure()
    for x, y, color in coordenadas:

        fig.add_trace(
            go.Scatter(
                mode='markers',
                x=[x],
                y=[y],
                marker_symbol='square',
                marker=dict(
                    color= color,
                    size=21,
                    # line=dict(
                    #     color='grey',
                    #     width=1
                    # )
                ),
                showlegend=False
            )
        )

    return fig