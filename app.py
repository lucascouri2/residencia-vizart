# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import generoVis 
import paleta2Vis
import paleta1Vis
import json

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

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
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
                value='genero'
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
    if(dropdown_visualizacao == 'paleta2'):
        if(clickData is None):
            return paleta2Vis.getPaletaPorAno(dropdown_artista)
        else:
            print(clickData)
            return paleta2Vis.getPaletaPorAnoSelected(dropdown_artista, clickData['points'][0]['x'])
    # elif(dropdown_visualizacao == 'estilo'):
        # return 
    elif(dropdown_visualizacao == 'genero'):
        return generoVis.func_genero(dropdown_artista)


@app.callback(
    Output('hover-data', 'children'),
    Input('visualizacao', 'clickData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


# @app.callback(
#     Output('visualizacao', 'figure'),
#     Input('visualizacao', 'clickData'),
#     Input('dropdown_artista', 'value'))
# def update_graph_onclick(clickData, dropdown_artista):
#     return paleta2Vis.getPaletaPorAnoSelected(dropdown_artista, clickData.x)

if __name__ == '__main__':
    app.run_server(debug=True)