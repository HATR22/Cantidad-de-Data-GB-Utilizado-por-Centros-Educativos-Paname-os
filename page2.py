# DATA POR DISTRITO
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(_name_)
server = app.server

colorscales = px.colors.named_colorscales()

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# Importa el dataset
read_file = pd.read_excel("aig-data-transferida-en-abril-2020-07_04_2020-06_05_2020.xlsx")
read_file.to_csv(r'aig_escuelas.csv', index=None, header=True)
df = pd.read_csv('aig_escuelas.csv')

escuelas_map = gpd.read_file("Escuelas.shp")
escuelas = escuelas_map.merge(df, left_on="NOMBRE", right_on="Nombre")

px.set_mapbox_access_token("pk.eyJ1IjoiY3lja2VzIiwiYSI6ImNrcnEyM2E5Mzh0Mngybm1uYWJqOHFrZ28ifQ.VSLRkPl5GJRRurmUNzsycw")
geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

# Obtener nombres de las provincias
province = df['Provincia'].unique()
province.sort()

# Generar la lista de opciones (diccionario)
options = [{'label': c, 'value': c} for c in province]

# Nuevo DF con los valores de la Data

dfValues = df['Data (GB)']

# General la lista de valores de la Data (diccionario)
marks = {c: str(c) for c in range(dfValues.min(), dfValues.max(), 50)}

px.set_mapbox_access_token("pk.eyJ1IjoiY3lja2VzIiwiYSI6ImNrcnEyM2E5Mzh0Mngybm1uYWJqOHFrZ28ifQ.VSLRkPl5GJRRurmUNzsycw")
geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

# fig2.show()

# fig2 = go.Figure()

# Use the following function when accessing the value of 'my-range-slider'
# in callbacks to transform the output value to logarithmic


app.layout = html.Div([
    html.H1('Proyecto Semestral - Tópicos Especiales II',
            style={'text-align': 'center', 'font-family': 'verdana', 'color': 'Ivory',
                   'background': 'black', 'border': '1px solid black', 'margin': '0px'}),

    html.H2('Visualización de la Cantidad de Data (GB) Utilizado por Centros Educativos Panameños',
            style={'text-align': 'center', 'font-family': 'verdana', 'color': 'black',
                   'background': 'antiquewhite', 'border': '1px solid antiquewhite', 'margin': '0px'}),

    html.H3('Parte 1 - Mapeo de Uso de Datos en GB por Centro Educativo',
            style={'text-align': 'center', 'font-family': 'verdana', 'color': 'black',
                   'background': 'linen', 'border': '1px linen', 'margin': '0px'}),
    html.Div([
        dcc.Graph(id='Map1')
    ]),

    html.H3('Parte 2 - Gráfica Interactiva de Uso de Datos en GB por Provincia y Cantidad de Datos (GB)',
            style={'text-align': 'center', 'font-family': 'verdana', 'color': 'black',
                   'background': 'linen', 'border': '1px antiquewhite', 'margin': '0px'}),
    html.Div([
        dcc.Graph(id='GraphSlider')
    ]),

    html.Div([
        html.Label(['Seleccione el rango de Data(GB) y la Provincia'],
                   style={'font-weight': 'bold', 'font-family': 'verdana', 'color': '#1b222e'}),
        html.P(),
        dcc.RangeSlider(
            id='RangeData',  # any name you'd like to give it
            min=0,
            max=1241,
            step=None,
            marks=marks,
            value=[0, 50],
        ),
        html.Div(dcc.Dropdown(
            id='province_opt',  # identificador del Dropdown
            options=options,
            value='Panamá'  # valor inicial de la opción
        ), style={'width': '35%', 'font-family': 'verdana'}),
    ]),

    html.H3('Grupo formado por:',
            style={'text-align': 'center', 'font-family': 'verdana', 'color': '#1b222e',
                   'padding': '20px'}),
    html.P('Ervis Alain',
           style={'text-align': 'center', 'font-family': 'verdana', 'color': '#1b222e'}),
    html.P('Fernando Del Castillo',
           style={'text-align': 'center', 'font-family': 'verdana', 'color': '#1b222e'}),
    html.P('Daniella Ramos',
           style={'text-align': 'center', 'font-family': 'verdana', 'color': '#1b222e'}),
    html.P('Harold Torres',
           style={'text-align': 'center', 'font-family': 'verdana', 'color': '#1b222e'}),

])


# Callback para actualizar la grafica
@app.callback(
    [Output(component_id='Map1', component_property='figure'),
     Output(component_id='GraphSlider', component_property='figure')],
    [Input(component_id='RangeData', component_property='value'),
     Input(component_id='province_opt', component_property='value')]
)
# funcion para la grafica
def update_bar(selected_value, selected_opt):
    dfFiltered = df[
        (df.iloc[:, 7] >= selected_value[0]) & (df.iloc[:, 7] <= selected_value[1]) & (df['Provincia'] == selected_opt)]

    fig2 = px.scatter_mapbox(escuelas,
                             color='Data (GB)',
                             hover_data=['Provincia', 'Distrito', 'Corregimiento', 'Proveedor'],
                             lat=escuelas.geometry.y,
                             lon=escuelas.geometry.x,
                             hover_name="Nombre",
                             title='Cantidad de GB utilizados por Centros Educativos del País',
                             zoom=6.7)

    fig = px.bar(dfFiltered, x="Corregimiento", y="Data (GB)", barmode="group",
                 hover_data=["Provincia", "Corregimiento", "Nombre", "Proveedor"], color='Data (GB)')
    fig.update_traces(marker_line_width=2)
    fig.update_layout(autosize=True, width=1500, height=800, )

    return fig2, fig


if _name_ == '_main_':
    app.run_server(debug=True)