import pandas as pd
import plotly_express as px
#import plotly.graph_objects as go

def preprocessoDados():

    dfList = []
    dfList.append(pd.read_json('dataset_artistas/andy-warhol.json', orient='records'))
    dfList.append(pd.read_json('dataset_artistas/frida-kahlo.json', orient='records'))
    dfList.append(pd.read_json('dataset_artistas/sandro-botticelli.json', orient='records'))
    dfList.append(pd.read_json('dataset_artistas/vincent-van-gogh.json', orient='records'))
    dfList.append(pd.read_json('dataset_artistas/pablo-picasso.json', orient='records'))
    dfList.append(pd.read_json('dataset_artistas/piet-mondrian.json', orient='records'))

    df = pd.concat(dfList, ignore_index=True)
    df[df.duplicated(['artistName'], keep=False)]
    df = df[df['genre']!='sketch and study']
    df = df[df['tags'].notna()]
    df = df[df['completitionYear'].notna()]
    df = df[df['genre'].notna()]
    df = df[df['style'].notna()]
    
    return df


def func_estilo(artista = 'van Gogh Vincent '):
    df = preprocessoDados()

    dfVis = pd.DataFrame({'count' :  df[df['artistName']==artista].groupby(['style','completitionYear'])['style'].size()}).reset_index()

    fig = px.bar(dfVis, x="completitionYear", y="count", color="style",labels={
                     "completitionYear": "Ano",
                     "count": "Quantidade",
                     "style": "Estilo"
                 },
                title="Estilo ao longo dos anos")

    fig.update_layout(
    #font_family="Courier New, monospace",
    font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    
    return fig
    # fig.update_layout(yaxis_range=(0, 100))
    # fig.show()