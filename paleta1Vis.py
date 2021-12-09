import pandas as pd
import plotly.graph_objects as go

# Carrega dados e retorn o dataframe para a visualizacao
def loadData(nomeArtista):
    return pd.read_csv(f'dataset_visualizacoes/{nomeArtista}-area.csv')

def loadPaletaCores(nomeArtista):
    return pd.read_csv(f'paletas/final_artistas/paleta_{nomeArtista}.csv')


# Cria a visualizacao do plotly
def getPaletaGeral(nomeArtista):
    dfVis = loadData(nomeArtista)
    paletaCores = loadPaletaCores(nomeArtista)

    x=dfVis.columns
    fig = go.Figure()

    freqAnosArray = dfVis.values

    for index in range(len(freqAnosArray)):

        fig.add_trace(go.Scatter(
            x=x, y=freqAnosArray[index],
            mode='lines',
            line=dict(width=0.5, color=paletaCores['hex'][index]),
            fillcolor = paletaCores['hex'][index],
            stackgroup='one',
            groupnorm='percent' # sets the normalization for the sum of the stackgroup
        ))


    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    return fig