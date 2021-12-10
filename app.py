# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import generoVis 
import estiloVis
import paleta2Vis
import paleta1Vis
import funcoes
import json
import base64

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

listaArtistas = ['van Gogh Vincent ', 'Picasso Pablo', 'Mondrian Piet', 'Kahlo Frida ', 'Warhol Andy', 'Botticelli Sandro ']

listaVisualizacoes = ['paleta1', 'paleta2', 'estilo', 'genero']

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )


def renderImages(listImages):
    divList = []
    for img in listImages:
        print(img)
        encoded_image = base64.b64encode(open(img, 'rb').read())
        divList.append(html.Div([html.Img(src='data:image/jpg;base64,{}'.format(encoded_image.decode()), className = 'image-workart')],
         className = 'div-image'))
    return divList

app.layout = html.Div(children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='dropdown_artista',
                options=[{'label': i, 'value': i} for i in listaArtistas],
                value='van Gogh Vincent '
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='dropdown_visualizacao',
                options=[{'label': i, 'value': i} for i in listaVisualizacoes],
                value='genero'#value='paleta1'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    html.Div([html.Pre(id='hover-data')], style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='visualizacao'
        #figure=generoVis.func_genero()
    ),

    html.Div(id = 'image-container',
        children = [
            html.Div(id='titulo-imagem-container'),
            html.Div(id='image-sub-container')]
    )
    
])






@app.callback(
    Output('visualizacao', 'figure'),
    Input('dropdown_artista', 'value'),
    Input('dropdown_visualizacao', 'value'),
    Input('visualizacao', 'clickData'))
def update_graph(dropdown_artista, dropdown_visualizacao, clickData):

    if(dropdown_visualizacao == 'paleta1'):
        return paleta1Vis.getPaletaGeral(dropdown_artista)
    elif(dropdown_visualizacao == 'paleta2'):
        if(clickData is None):
            return paleta2Vis.getPaletaPorAno(dropdown_artista)
        else:
            print(clickData)
            return paleta2Vis.getPaletaPorAnoSelected(dropdown_artista, clickData['points'][0]['x'])
    elif(dropdown_visualizacao == 'estilo'):
        if(clickData is None):
            return estiloVis.func_estilo(dropdown_artista)
        else:
            print(clickData)
            return estiloVis.func_estilo(dropdown_artista)
    elif(dropdown_visualizacao == 'genero'):
        if(clickData is None):
            return generoVis.func_genero(dropdown_artista)
        else:
            print(clickData)
            return generoVis.func_genero(dropdown_artista)


@app.callback(
    Output('image-sub-container', 'children'),
    Input('visualizacao', 'clickData'),
    Input('dropdown_artista', 'value'))
def display_images(clickData, dropdown_artista):
    if(clickData is None):
        return []
    else:
        listPaths = funcoes.getPaths(dropdown_artista, clickData['points'][0]['x'])
        return renderImages(listPaths)

@app.callback(
    Output('titulo-imagem-container', 'children'),
    Input('visualizacao', 'clickData'))
def display_titulo_imagens(clickData):
    if(clickData is None):
        return []
    else:
        ano = clickData['points'][0]['x']
        return html.H1(id='titulo-imagem',
        children= ano
        )


# @app.callback(
#     Output('visualizacao', 'figure'),
#     Input('visualizacao', 'clickData'),
#     Input('dropdown_artista', 'value'))
# def update_graph_onclick(clickData, dropdown_artista):
#     return paleta2Vis.getPaletaPorAnoSelected(dropdown_artista, clickData.x)

if __name__ == '__main__':
    app.run_server(debug=True)