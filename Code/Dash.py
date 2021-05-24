#----------VERSION PARCIAL PARA EL DASHBOARD---------------------------



import ProyectSQL as sql
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


external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"]


#Colores para el bg y el texto dash
colors = {
    'background': '#cce6ff',
    'text': ' #001133'
}


#--------------------------GRAFICA CHOROPLETH----------------------------------------------
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

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
#     )


#-----------------------DEPARTAMENTOS PARA EL DROP-DOWN-----------------------------------

query1=''' select nombre_d from departamento order by nombre_d asc; '''
queryx=pd.read_sql_query(query1,con.connection)
prueba=queryx['nombre_d'].tolist()
listafinal=[i for i in range (34)]
for i in range(0,len(prueba)):
    listafinal[i]={'label':prueba[i],'value':prueba[i]}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#---------------------HOMBRES VS MUJERES-----------------------------------------------
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
    

fig2=go.Figure(data=[
    go.Bar(name='Hombres',x=materias,y=y1),
    go.Bar(name='Mujeres',x=materias,y=y2),
    ])

# fig2.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
#     )


#---------------------------COLEGIOS PRIVADOS VS PUBLICOS---------------------------
con=Connection()
con.openConnection()

queryt4=pd.read_sql_query(sql.avgPromediosTipoColegio(),con.connection)  

con.closeConnection() 
df1=pd.DataFrame(queryt4, columns=["naturaleza", "puntaje_global"])

#Gráfico de barras
figBar1 = px.bar(df1, x="naturaleza", y="puntaje_global",width=450, height=450) 

# figBar1.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
#     )

#---------------------------PROMEDIO PUNTAJE GLOBAL POR ESTRATO---------------------
con = Connection()
con.openConnection()
queryt5 = pd.read_sql_query(sql.PuntajeByEstrato(), con.connection)
con.closeConnection()
dfCases = pd.DataFrame(queryt5, columns=["promedio_puntaje", "estrato"])
figBarPuntajeEstrato = px.bar(dfCases.head(7), x="estrato", y="promedio_puntaje",color='promedio_puntaje')

# figBarPuntajeEstrato.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
#     )


#----------------------------Pie distribucion de estratos--------------------------------
con = Connection()
con.openConnection()
queryt6 = pd.read_sql_query(sql.CuantosPorEstrato(), con.connection)
con.closeConnection()
dfestrato = pd.DataFrame(queryt6, columns=["estrato", "many"])
figPieEstrato = px.pie(dfestrato, values="many", names="estrato",
                     title='Distribución de los estratos de los estudiantes')

# figPieEstrato.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
#     )

#-----------------------------Grafico horizontal mejor colegios Colombia-----------------

con = Connection()
con.openConnection()
queryt7 = pd.read_sql_query(sql.RankingMejoresColegiosBogota(), con.connection)
dfranking = pd.DataFrame(queryt7, columns=["colegio", "puntaje"])
figBarRanking = px.bar(dfranking.head(10), y="colegio",x="puntaje" , orientation = 'h',color='puntaje')

# figBarRanking.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
#     )


#---------------------------APP PRINCIPAL------------------------------------------------

#

app.layout = html.Div(style={'backgroundColor':colors['background']},
    children=[
    html.H1(children="Análisis Resultados Icfes",
              style={'font-family':'"Times New Roman", Times, serif',
                    'font-weight':'bold','textAlign': 'center',
                    'color':colors['text']}),
    html.Div(className='container-fluid',children=[
        #row
        html.Div(className='row',children=[
            #full col
            html.Div(className='col',children=[
                #card for drop-down
                html.Div(className='card',children=[
                    html.Div(className='card-header',children=[
                        html.H2(children='Mejores colegios por departamento'),
                        ]),
                    html.Div(className='card-body',children=[
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
                        html.Div(id='dd-output-container',
                                 style={'fontSize': 20,
                                        'text-align':'left','color':colors['text']}),
                        dcc.Graph(id='indicator-graphic'),
                    ])
                ])
            ])
        ])
    ]),
    html.Div(className='container-fluid',children=[
    #row
    html.Div(className='row',children=[
        #full col
        html.Div(className='col',children=[
            #card for drop-down
            html.Div(className='card',children=[
                html.Div(className='card-header',children=[
                    html.H2(children='Promedio puntaje por estrato'),
                    ]),
                html.Div(className='card-body',children=[
                    html.Div(id='dd-output-slider',
                                 style={'fontSize': 20,
                                        'text-align':'left','color':colors['text']}),
                    dcc.Graph(id='graph-with-slider'),
                    html.Div('Slider', 
                             style={'fontSize': 20
                                    ,'color':colors['text']}),
                    dcc.Slider(
                        id='estrato-slider',
                        min=1,
                        max=6,
                        value=1,
                        marks={1:'Estrato 1',2:'Estrato 2',3:'Estrato 3',
                               4:'Estrato 4',5:'Estrato 5',6:'Estrato 6'},
                        step=None
                        ),
                    ])
                ])
            ])
        ])
    ]),
    html.Div(className="container-fluid",children=[
        #Row
        html.Div(className="row",children=[
            html.Div(className="col-12 col-xl-5",children=[
                #Card por choropleth
                html.Div(className="card",children=[
                    #titulo de la tarjeta
                    html.Div(className="card-header",children=[
                        html.H2(children="Puntaje promedio Ingles"),
                        ]),
                    html.Div(className="card-body",children=[
                        #Grafica Choropleth
                        dcc.Graph(
                            id='PuntajeInglesPromedio',
                            figure=fig
                            ),
                        ])
                    ])
                ]),
            html.Div(className='col-12 col-xl-5',children=[
                #card for pie
                html.Div(className="card",children=[
                    #titulo de la tarjeta
                    html.Div(className='card-header',children=[
                        html.H2(children="Distribucion de estratos"),
                        ]),
                    html.Div(className="card-body",children=[
                        #grafica pie
                        dcc.Graph(
                            id="DistribucionEstratos",
                            figure=figPieEstrato
                            ),
                        ])
                    ])
                ]),
            html.Div(className='col-12 col-xl-5',children=[
                #card for promedio total por estratos
                html.Div(className="card",children=[
                    #titulo de la tarjeta
                    html.Div(className='card-header',children=[
                        html.H2(children="Promedio Puntaje Global por estratos"),
                        ]),
                    html.Div(className="card-body",children=[
                        #grafica bar estratos promedio global
                        dcc.Graph(
                            id="GlobalEstratos",
                            figure=figBarPuntajeEstrato
                            ),
                        ])
                    ])
                ]),
            html.Div(className='col-12 col-xl-5',children=[
                #card for grafico horizontal mejores colegios Colombia
                html.Div(className="card",children=[
                    #titulo de la tarjeta
                    html.Div(className='card-header',children=[
                        html.H2(children="Mejores Colegios de Colombia"),
                        ]),
                    html.Div(className="card-body",children=[
                        #grafica bar mejores colegios Colombia
                        dcc.Graph(
                            id="MejoresColegios",
                            figure=figBarRanking
                            ),
                        ])
                    ])
                ]),
              html.Div(className='col-12 col-xl-5',children=[
                #card for grafico privados vs publicos
                html.Div(className="card",children=[
                    #titulo de la tarjeta
                    html.Div(className='card-header',children=[
                        html.H2(children="Puntaje global colegios privados-publicos"),
                        ]),
                    html.Div(className="card-body",children=[
                        #grafica bar privados vs publicos
                        dcc.Graph(
                            id="PrivadosPublicos",
                            figure=figBar1
                            ),
                        ])
                    ])
                ]),
            
            html.Div(className="col-12 col-xl-5",children=[
                #card for hombres vs mujeres
                html.Div(className="card",children=[
                    html.Div(className="card-header",children=[
                        html.H2(children="Promedio por Asignatura Hombres-Mujeres"),
                        ]),
                    html.Div(className="card-body",children=[
                        dcc.Graph(
                            id='MenvsWoman',
                            figure=fig2
                            ),
                        ])
                    ])
                ])
            ]),
        ])
    # html.Div('Seleccione un departamento', 
    #           style={'fontSize': 20,
    #                 'text-align':'left','color':colors['text']}),
    # dcc.Dropdown(
    #     id='demo-dropdown',
    #     options=[i for i in listafinal],
    #     placeholder="seleccione un departamento",
    #     value='Ninguno',
    #     clearable=True,
    #     style={
    #             'text-align':'left',
    #             'width': '400px',
    #             'background-color': '#d1d1e0',
    #             'color':colors['text']}),
    # html.Div(id='dd-output-container',style={'fontSize': 20,
    #                 'text-align':'left','color':colors['text']}),
    # dcc.Graph(id='indicator-graphic'),
    # html.Div('Slider', 
    #           style={'fontSize': 20
    #                 ,'color':colors['text']}),
    # dcc.Graph(id='graph-with-slider'),
    # dcc.Slider(
    #     id='estrato-slider',
    #     min=1,
    #     max=6,
    #     value=1,
    #     marks={1:'Estrato 1',2:'Estrato 2',3:'Estrato 3',
    #            4:'Estrato 4',5:'Estrato 5',6:'Estrato 6'},
    #     step=None
    # ),
    
    # html.H3(children="Promedio Puntaje Ingles por departamento"),
    # dcc.Graph(
    #     id='PuntajeInglesPromedio',
    #     figure=fig ),
    # html.H3(children="Hombres vs mujeres"),
    # dcc.Graph(
    #     id='MenvsWoman',
    #     figure=fig2)
])



@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    dash.dependencies.Input('demo-dropdown', 'value'))
def update_output(value):
    return 'Has seleccionado "{}"'.format(value)
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    dash.dependencies.Input('demo-dropdown', 'value'))
def figure_output(value):
    query6='''select c.nombre_colegio as colegio ,avg(x.puntaje_global)::real as puntaje from (((departamento d inner join municipio m on d.codigo_d=m.codigo_d_departamento)
    inner join colegio c on c.codigo_m_municipio=m.codigo_m)inner join estudiante e 
    on e.codigo_colegio=c.codigo) inner join examen x on x.id_estudiante=e.id_estudiante
    where d.nombre_d='{0}' group by c.nombre_colegio order by puntaje desc limit 7;'''.format(value)
    queryt=pd.read_sql_query(query6,con.connection)
    dfPrueba=pd.DataFrame(queryt,columns=['colegio','puntaje'])
    fig=px.bar(dfPrueba,x='colegio',y='puntaje',color='puntaje',color_discrete_sequence= px.colors.sequential.Plasma)  #,width=800,height=500, ,color_discrete_sequence= px.colors.sequential.Plasma

    # fig.update_layout(
    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
    return fig

@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    dash.dependencies.Input('estrato-slider', 'value'))
def figure2_outuput(estrato):
    query7=''' select avg(x.puntaje_c_naturales)::real as promNaturales,
    avg(x.puntaje_matematicas)::real as promMatematicas,
    avg(x.puntaje_sociales)::real as promSociales,
    avg(x.puntaje_ingles)::real as promIngles,
    avg(x.puntaje_lectura_critica)::real as promLectura 
    from examen x inner join estudiante e on e.id_estudiante=x.id_estudiante
    where e.estrato='{0}' group by e.estrato having e.estrato<>-1;'''.format(estrato)
    queryt4=pd.read_sql_query(query7,con.connection)
    # dfSlider=pd.DataFrame(queryt4,columns=materias)
    primera=True
    for i in materias:
        if primera:
            y3=queryt4[i].tolist()
            primera=False
        y3.append((queryt4[i].tolist())[0])
    figs=go.Figure(data=[
        go.Bar(name='Promedio',x=materias,y=y3)
        ])
    # figs.update_layout(
    #     barmode='group',
    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
    
    return figs
@app.callback(
    dash.dependencies.Output('dd-output-slider', 'children'),
    dash.dependencies.Input('estrato-slider', 'value'))
def update_text(value):
    return 'Estrato seleccionado: "{}"'.format(value)
    
    

if __name__ == '__main__':
    app.run_server(debug=True)
    



    
