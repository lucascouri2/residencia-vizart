import pandas as pd
import plotly.graph_objects as go

# Carrega dados e retorn o dataframe para a visualizacao
def loadData(nomeArtista):
    return pd.read_csv(f'paletas/final_artistas/paleta_anos_{nomeArtista}.csv')


def calculateCordenadas(dfPaletaAnos):
    x = list(range(1, 11)) * len(dfPaletaAnos['completitionYear'].unique())
    dfPaletaAnos['ordemVis'] = x
    return list(dfPaletaAnos[['completitionYear','ordemVis','hex']].to_records(index=False))


# Cria a visualizacao do plotly
def getPaletaPorAno(nomeArtista):
    dfPaletaAnos = loadData(nomeArtista)

    coordenadas = calculateCordenadas(dfPaletaAnos)
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