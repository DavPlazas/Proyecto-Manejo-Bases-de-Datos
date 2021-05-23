import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import requests
import psycopg2
import json
import plotly.graph_objects as go

class Connection:
    
    def __init__(self):
        self.connection = None
    
    def openConnection(self):
        try:
            self.connection = psycopg2.connect(user="postgres",
                                               password="Veneno2003",
                                               database="proyecto",
                                               host="localhost", 
                                               port="5432")
        except Exception as e:
            print (e)

    def closeConnection(self):
        self.connection.close()
    
#Colores para el bg y el texto dash
colors = {
    'background': '#cce6ff',
    'text': ' #001133'
}

repo_url='https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'


co_regions_geo=requests.get(repo_url).json()
query2=''' select avg(x.puntaje_ingles)::real as promingles, d.nombre_d as departamento from ((((examen x inner join estudiante e on x.id_estudiante=e.id_estudiante)
inner join colegio c on c.codigo=e.codigo_colegio)inner join municipio m on m.codigo_m=c.codigo_m_municipio)
inner join departamento d on d.codigo_d=m.codigo_d_departamento) where x.puntaje_ingles is not null group by d.nombre_d;'''

con = Connection()
con.openConnection()
queryt = pd.read_sql_query(query2, con.connection)
dfIngles = pd.DataFrame(queryt, columns=["promingles", "departamento"])
fig=px.choropleth(data_frame=dfIngles,
                  geojson=co_regions_geo,
                  locations='departamento',
                  featureidkey='properties.NOMBRE_DPT',
                  color='promingles',
                  color_continuous_scale="burg")
fig.update_geos(showcountries=True,showcoastlines=True,showland=False,fitbounds="locations")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']




query1=''' select nombre_d from departamento order by nombre_d asc; '''
queryx=pd.read_sql_query(query1,con.connection)
prueba=queryx['nombre_d'].tolist()
listafinal=[i for i in range (34)]
for i in range(0,len(prueba)):
    listafinal[i]={'label':prueba[i],'value':prueba[i]}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


con = Connection()
con.openConnection()
query4=''' select e.sexo,avg(x.puntaje_c_naturales)::real as promNaturales,
avg(x.puntaje_matematicas)::real as promMatematicas,
avg(x.puntaje_sociales)::real as promSociales,
avg(x.puntaje_ingles)::real as promIngles,
avg(x.puntaje_lectura_critica)::real as promLectura 
from examen x inner join estudiante e on e.id_estudiante=x.id_estudiante group by e.sexo having e.sexo<>'-' and e.sexo='M';'''

query5=''' select e.sexo,avg(x.puntaje_c_naturales)::real as promNaturales,
avg(x.puntaje_matematicas)::real as promMatematicas,
avg(x.puntaje_sociales)::real as promSociales,
avg(x.puntaje_ingles)::real as promIngles,
avg(x.puntaje_lectura_critica)::real as promLectura 
from examen x inner join estudiante e on e.id_estudiante=x.id_estudiante group by e.sexo having e.sexo<>'-' and e.sexo='F';'''
queryt2 = pd.read_sql_query(query4, con.connection)
queryt3=pd.read_sql_query(query5, con.connection)

#DataFrame
# dfSexo=pd.DataFrame(queryt, columns=["sexo", "promnaturales","prommatematicas",
#                                      "promsociales","promingles","promlectura"])

materias=["promnaturales","prommatematicas","promsociales","promingles","promlectura"]
primera=True
for i in materias:
    if primera:
        y1=queryt2[i].tolist()
        y2=queryt3[i].tolist()
        primera=False
    y1.append((queryt2[i].tolist())[0])
    y2.append((queryt3[i].tolist())[0])
    

# x1=['PromNatu','PromMate','PromSociales','PromIngles','PromLectura']

fig2=go.Figure(data=[
    go.Bar(name='Hombres',x=materias,y=y1),
    go.Bar(name='Mujeres',x=materias,y=y2),
    ])

fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

app.layout = html.Div(style={'backgroundColor':colors['background']},children=[
    html.H1(children="Análisis Resultados Icfes",
             style={'font-family':'"Times New Roman", Times, serif',
                    'font-weight':'bold','textAlign': 'center',
                    'color':colors['text']}),
    html.Div('Seleccione un departamento', 
              style={'fontSize': 20,
                    'text-align':'left','color':colors['text']}),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[i for i in listafinal],
        placeholder="seleccione un departamento",
        value='Ninguno',
        clearable=True,
        style={
                'text-align':'left',
                'width': '400px',
                'background-color': '#d1d1e0',
                'color':colors['text']}),
    html.Div(id='dd-output-container',style={'fontSize': 20,
                    'text-align':'left','color':colors['text']}),
    dcc.Graph(id='indicator-graphic'),
    html.H3(children="Promedio Puntaje Ingles por departamento"),
    dcc.Graph(
        id='PuntajeInglesPromedio',
        figure=fig ),
    html.H3(children="Hombres vs mujeres"),
    dcc.Graph(
        id='MenvsWoman',
        figure=fig2)
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    #dash.dependencies.Output('indicator-graphic', 'figure')
    dash.dependencies.Input('demo-dropdown', 'value'))
    # dash.dependencies.Input('demo-dropdown', 'value'))
def update_output(value):
    return 'Has seleccionado "{}"'.format(value)
# def update_output(value):
#     query6=''' select nombre_d,numero_evaludados_d as num from departamento where
#     nombre_d='{0}'''.format(value)
#     queryt=pd.read_sql_query(query6,con.connection())
#     dfPrueba=pd.DataFrame(queryt,columns=[value,'num'])
#     fig=px.bar(dfPrueba,x=value,y='num')
#     return fig,


if __name__ == '__main__':
    app.run_server(debug=True)
    


#-----PARTE DAVID--------------
#
#
#
#
#
#
#

#----PARTE SANTIAGO------------
#
#
#
#
#

#----PARTE JOSE -----------
#
#
#
#

    
