# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#Dash dependencies
import dash
from dash.dcc.Dropdown import Dropdown
from dash import dcc#import dash_core_components as dcc
from dash import html#import dash_html_components as html
from dash.dependencies import Input, Output

#Other libraries
import base64

#Visualization functions and classes
import generoVis 
import estiloVis
import paleta1Vis
import funcoes
from paleta2Vis import Paleta2Vis


# Variaveis do dash
app = dash.Dash(__name__)

listaArtistas = [ ['van Gogh Vincent ','Vincent van Gogh'], ['Picasso Pablo', 'Pablo Picasso '], ['Mondrian Piet', 'Piet Mondrian'], ['Kahlo Frida ','Frida Kahlo'], ['Warhol Andy','Andy Warhol'], ['Botticelli Sandro ', 'Sandro Botticelli']]
listaVisualizacoes = [ ['paleta1', 'Paleta de cores 1'], ['paleta2', 'Paleta de cores 2'] , ['estilo', 'Estilos das obras'], ['genero', 'Gêneros das obras']]

paleta2Vis = Paleta2Vis()


# Funcoes de apoio
def renderImages(listPaths, listTitles, listStyles, listGenre):
    divList = []
    for img, titulo, estilo, genero in zip(listPaths, listTitles, listStyles,listGenre):
       
        encoded_image = base64.b64encode(open(img, 'rb').read())
        divList.append(html.Div([
            html.Img(src='data:image/jpg;base64,{}'.format(encoded_image.decode()), className = 'image-workart', 
            title=f"Título: {titulo}\nEstilo: {estilo}\nGênero: {genero}"),
        ],
         className = 'div-image'))
    return divList


# Layout HTML do Dash
app.layout = html.Div(children=[
    html.Div([
        html.H1(
        children='VisArt',
        id = 'titulo'),
        html.H5(
        children='A EVOLUÇÃO DA ARTE',
        id = 'subtitulo')
        ], id = 'titulo-app'),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='dropdown_artista',
                #options=[{'label': i, 'value': i} for i in listaArtistas],
                options=[{'label': j, 'value': i} for i,j in listaArtistas],
                value='van Gogh Vincent '
            )
        ], style={'width': '48%', 'display': 'inline-block',  'font-family': '"Courier New", monospace'}),

        html.Div([
            dcc.Dropdown(
                id='dropdown_visualizacao',
                #options=[{'label': i, 'value': i} for i in listaVisualizacoes],
                options=[{'label': j, 'value': i} for i, j in listaVisualizacoes],
                value='genero'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'font-family': '"Courier New", monospace'})
    ]),

    dcc.Graph(
        id='visualizacao'
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
 
    # Reset controle das visualizacoes quando muda visualizacao
    mudouDropdown = False
    ctxt = dash.callback_context.triggered
    if(ctxt[0]['prop_id'] == 'dropdown_artista.value' or ctxt[0]['prop_id'] == 'dropdown_visualizacao.value'):
        mudouDropdown = True
        paleta2Vis.selecaoAtiva = False
        paleta2Vis.ano = 0

    if(dropdown_visualizacao == 'paleta1'):
        return paleta1Vis.getPaletaGeral(dropdown_artista)
        
    elif(dropdown_visualizacao == 'paleta2'):
        if(clickData is None or mudouDropdown):
            mudouDropdown = False
            return paleta2Vis.getPaletaPorAnoSelected(dropdown_artista,0)
        else:
            ano = clickData['points'][0]['x']
            if(paleta2Vis.ano == ano):
                paleta2Vis.selecaoAtiva = False
                return paleta2Vis.getPaletaPorAnoSelected(dropdown_artista,0)
            else:
                paleta2Vis.selecaoAtiva = True
                vis = paleta2Vis.getPaletaPorAnoSelected(dropdown_artista, clickData['points'][0]['x'])
                return vis

    elif(dropdown_visualizacao == 'estilo'):
        if(clickData is None):
            return estiloVis.func_estilo(dropdown_artista)
        else:
            return estiloVis.func_estilo(dropdown_artista)
    
    elif(dropdown_visualizacao == 'genero'):
        if(clickData is None):
            return generoVis.func_genero(dropdown_artista)
        else:
            return generoVis.func_genero(dropdown_artista)


@app.callback(
    Output('image-sub-container', 'children'),
    Input('visualizacao', 'clickData'),
    Input('dropdown_artista', 'value'),
    Input('dropdown_visualizacao', 'value'))
def display_images(clickData, dropdown_artista,dropdown_visualizacao):

    mudouDropdown = False
    ctxt = dash.callback_context.triggered
    if(ctxt[0]['prop_id'] == 'dropdown_artista.value' or ctxt[0]['prop_id'] == 'dropdown_visualizacao.value'):
        mudouDropdown = True

    if(clickData is None or mudouDropdown):
        mudouDropdown = False
        return []
    else:
        ano = clickData['points'][0]['x']
        if(paleta2Vis.ano == ano):
            return []
        else: 
            dfPaths = funcoes.getPaths(dropdown_artista, ano) #dfPaths tem titulo, estilo, genero e path
            listPaths = dfPaths['path'] #pega só o path
            listTitles = dfPaths['title']
            listStyles = dfPaths['style']
            listGenre = dfPaths['genre']
            return renderImages(listPaths, listTitles, listStyles, listGenre)


@app.callback(
    Output('titulo-imagem-container', 'children'),
    Input('visualizacao', 'clickData'),
    Input('dropdown_artista', 'value'),
    Input('dropdown_visualizacao', 'value'))
def display_titulo_imagens(clickData, dropdown_artista, dropdown_visualizacao):
    mudouDropdown = False
    ctxt = dash.callback_context.triggered
    if(ctxt[0]['prop_id'] == 'dropdown_artista.value' or ctxt[0]['prop_id'] == 'dropdown_visualizacao.value'):
        mudouDropdown = True

    if(clickData is None or mudouDropdown):
        mudouDropdown = False
        return []
    else:
        ano = clickData['points'][0]['x']
        if(paleta2Vis.ano == ano):
            return []
        else: 
            return html.H1(id='titulo-imagem',
            children= ano
        )


if __name__ == '__main__':
    app.run_server(debug=True)