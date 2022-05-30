from dash import Dash, dcc, html, Input, Output, dash_table
import dash_table.FormatTemplate as FormatTemplate
from numpy import size
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc


REMOTE_DATABASE_URI = 'postgresql+psycopg2://hpxywmetxvdawa:15a82606c74096ef3ae1c2155a224058e2676df9667b59a8e50b16939824e0b6@ec2-44-195-169-163.compute-1.amazonaws.com:5432/daf3hf8l7lq7rl'


app = Dash(__name__,title='Financial Insight Zambia Dashboard',meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server =app.server

engine = create_engine(REMOTE_DATABASE_URI)
df = pd.read_sql_table('luse', con=engine)

year_options = []
for year in df['year'].unique():
    year_options.append({'label':year,'value':year})

company_options = []
for company in df['instrument'].unique():
    company_options.append({'label':company,'value':company})

@app.callback(
    Output('line-graph', 'figure'),
    [Input('company-picker', 'value')]
)
def update_line(selected_company):
    
    df2 = df[df.instrument.isin([selected_company])]
    
    fig = px.bar(df2, x='eps', y='year',
             hover_data=['eps', 'revenue', 'profit'], color='profit',
             labels={'eps':'EPS','year':'Year','profit':'Profit','revenue':'Revenue'}, orientation='h')

    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                      )
    
    return fig

@app.callback(
    Output('bar-graph', 'figure'),
    [Input('company-picker-bar', 'value')]
)
def update_line(selected_company):
    bar_df = df[df.instrument.isin([selected_company])]
    trace1 = go.Bar(
    x=bar_df['year'], 
    y=bar_df['revenue'],
    name = 'Revenue $',
    marker=dict(color='#A020F0')
    )

    trace2 =go.Bar(
    x=bar_df['year'],
    y=bar_df['profit'],
    name='Profit $',
    marker=dict(color='#00FF00')

    )

    trace3 =go.Scatter(
            x=bar_df['year'],
            y=bar_df['revenue'],
            mode="markers+lines",
            name="Revenue Trend",
            line = dict(color='#FF0000'),
            marker = dict(symbol ='square')

        )

    trace4 =go.Scatter(
                x=bar_df['year'],
                y=bar_df['profit'],
                mode="markers+lines",
                name="Profit Trend",
                line = dict(color='#FFA500'),
                marker = dict(symbol ='circle')

            )

    data =[trace1, trace2, trace3, trace4]
    layout = go.Layout(
    xaxis = dict(title ='Year')
    ) 
    fig5 =go.Figure(data=data, layout=layout)

    return fig5


@app.callback(
    (Output('pie-graph', 'figure')),
    [Input('year-picker-pie', 'value')])
def update_pie(selected_year):
    filtered_df = df[df.year == selected_year]
    filtered_df.loc[df['revenue'] < 2.e4, 'company'] = 'Other companies'
    fig2 = px.pie(filtered_df, values='revenue', names='instrument',hole=0.5,hover_data=['company'], labels={'revenue':'Revenue','company':'Company','instrument':'Instrument','profit':'Profit'})
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(transition_duration=200)

    return fig2

@app.callback(
    Output('graph-with-dropdown', 'figure'),
    Input('year-picker-sc', 'value'))
def update_bubble(selected_year):
    filtered_df2 = df[df.year == selected_year]

    fig3 = px.scatter(filtered_df2, x="profit", y="revenue", 
                    labels={
                     "profit": "Profit",
                     "revenue": "Revenue",
                     'company':'Company',
                     'eps':'Earnings Per Share'
                 },
                 
                    size='eps',
                     color="company", hover_name="instrument",
                     log_x=True, log_y=True, size_max=55)

    fig3.update_layout(transition_duration=200)

    return fig3


curr_yr = df['year'].max()
prev_yr = str(int(curr_yr) - 1)
df3 = df[df.year == curr_yr]
df4 = df[df.year == prev_yr]
curr_rev = df3['revenue'].sum()
prev_rev = df4['revenue'].sum()

fig4 = go.Figure(go.Indicator(
        mode="number+delta",
        number = {'prefix': "$","font":{"size":50}},
        value=curr_rev,
        title=dict(text=str(curr_yr), font=dict(size=20)),
        delta = {'reference': prev_rev, 'relative': True, 'position' : "bottom", 'valueformat':'.0%',"font":{"size":30}}
        ))

    

if curr_rev >= prev_rev:
    fig4.update_traces(delta_increasing_color='green')
elif curr_rev < prev_rev:
    fig4.update_traces(delta_decreasing_color='red')




curr_yr = df['year'].max()
prev_yr = str(int(curr_yr) - 1)
df3 = df[df.year == curr_yr]
df4 = df[df.year == prev_yr]
curr_prf = df3['profit'].sum()
prev_prf = df4['profit'].sum()
fig5 = go.Figure(go.Indicator(
        mode="number+delta",
        number = {'prefix': "$","font":{"size":50}},
        value=curr_prf,
        title=dict(text=str(curr_yr), font=dict(size=20)),
        delta = {'reference': prev_prf, 'relative': True, 'position' : "bottom", 'valueformat':'.0%',"font":{"size":30}}
        ))
    
    

if curr_rev >= prev_rev:
    fig4.update_traces(delta_increasing_color='green')
elif curr_rev < prev_rev:
    fig4.update_traces(delta_decreasing_color='red')

   
markdown_text = '''
  ###### Welcome / Dashboard /[Home page](https://fizambia.com/)
'''
markdown_text2 = '''
  ###### **Revenue Share**
'''
markdown_text3 = '''
  ###### **EPS vs Profit**
'''
markdown_text4 = '''
  ###### **Revenue, Profit and EPS (Bubble size)**
'''
markdown_text5 = '''
  ###### **Lusaka Stock Exchange Listed Company Data Table**
'''
markdown_text6 = '''
  ###### &copy 2022 Financial Insight Zambia Web-app designed and developed by [Tim Chimfwembe](https://www.linkedin.com/in/timothychimfwembe/)
'''
markdown_text7 = '''
  #### **Total Revenue**
'''
markdown_text8 = '''
  #### **Total Profit**
'''
markdown_text9 = '''
  ###### **Profit and Revenue Trends**
'''

app.layout=html.Div([
dbc.Navbar(
    html.Div(
        [
            html.A(
                dbc.Row(
                    [   
                        

                        dbc.Col(html.Img(src='/assets/logo.png', height="45px")),
                        dbc.Col(dbc.NavbarBrand("Financial Insight Zambia", className="ms-2", style={'fontSize':30})),
                    ],
                    align="center",
                    className="g-0 nav2",
                ),
                href="https://fizambia.com/",
                style={"textDecoration": "none", 'margin-left':'True'},
            ),
                
          
                           
            
        ]
    , className='div'),
    color="dark",
    dark=True,

    
),

html.Div([
                            html.P(dcc.Markdown(children=markdown_text))
            ], className='div'),

html.Div([
                dbc.Row([
                           dbc.Col([
                                    

                                                dbc.Row([
                                                            dbc.Col([
                                                                        
                                                                                    dbc.Row([
                                                                                            dbc.Col([       
                                                                                                        dbc.Card([
                                                                                                                    dbc.CardHeader(dcc.Markdown(children=markdown_text7)),
                                                                                                                    dbc.CardBody([dcc.Graph(id='revenue', figure=fig4, style=dict(height='200px'))])
                                                                                                                ])
                                                                                                    ])
                                                                                                    
                                                                                           ]),

                                                                        
                                                                                    dbc.Row([
                                                                                            dbc.Col([       
                                                                                                        dbc.Card([
                                                                                                                    dbc.CardHeader(dcc.Markdown(children=markdown_text8)),
                                                                                                                    dbc.CardBody([dcc.Graph(id='profit', figure=fig5, style=dict(height='200px'))])
                                                                                                                ],className='div')
                                                                                                    ])
                                                                                            
                                                                                           ])
                                                                        

                                                                        

                                                                        ],
                                                                        width=5),
                                                                
                                                            dbc.Col([
                                                                        dbc.Card([
                                                                                    dbc.CardHeader(dcc.Markdown(children=markdown_text2)),
                                                                                    dbc.CardBody([dbc.Label('Select year:'),dcc.Dropdown(id='year-picker-pie',options=year_options,value=df['year'].max(),style={'width':'40%'}),dcc.Graph(id='pie-graph', className='plot-font')]),
                                                                                    
                                                                                    
                                                            ]),
                                                            ],width=7)
                                                ]),

                                                
                                                
                                                
                           
                          
                                    ]),
                           
                           ]) ,
                           

                ], className='div'),



html.Div([
            dbc.Row([
                        dbc.Col([
                                    dbc.Card([
                                                dbc.CardHeader(dcc.Markdown(children=markdown_text3)),
                                                dbc.CardBody([dbc.Label('Select ticker:'),
                                                              dcc.Dropdown(id='company-picker',options=company_options,value='CEC',style={'width':'60%'}),
                                                              dcc.Graph(id='line-graph')]),
                                                
                           ]),
                          
                                    ],
                                    width=5
                                    ),

                        dbc.Col([
                                    dbc.Card([
                                                dbc.CardHeader(dcc.Markdown(children=markdown_text9)),
                                                dbc.CardBody([dbc.Label('Select ticker:'),
                                                              dcc.Dropdown(id='company-picker-bar',options=company_options,value='ZAFICO',style={'width':'60%'}),
                                                              dcc.Graph(id='bar-graph')]),
                                                
                           ]),
                          
                                    ],
                                    width=7
                                    )
                
            ])




], className='div'),

html.Div([
                dbc.Row([
                           dbc.Col([
                                    dbc.Card([
                                                dbc.CardHeader(dcc.Markdown(children=markdown_text4)),
                                                dbc.CardBody([dbc.Label('Select year:'),dcc.Dropdown(id='year-picker-sc',options=year_options,value=df['year'].max(),style={'width':'29%'}),dcc.Graph(id='graph-with-dropdown')]),
                                                
                           ]),
                          
                                    ],
                                    width=12
                                    ),
                           
                          
                           
                           ]) ,
                           

                ], className='div'),

html.Div([
                dbc.Row([
                           dbc.Col([
                                    dbc.Card([
                                                
                                                dbc.CardHeader(dcc.Markdown(children=markdown_text5)),
                                                dbc.CardBody(
                                                    
                                                                dash_table.DataTable(
                                                                                        data=df.to_dict('records'),
                                                                                        columns=[
                                                                                                    {"name": "Company", "id": "company"},
                                                                                                    {"name": "Ticker", "id": "instrument"},
                                                                                                    {
                                                                                                        "name": "Year",
                                                                                                        "id": "year",
                                                                                                        "type": "numeric",
                                                                                                    },
                                                                                                    {
                                                                                                        "name": "Profit",
                                                                                                        "id": "profit",
                                                                                                        "type": "numeric",
                                                                                                        "format": FormatTemplate.money(0),
                                                                                                    },
                                                                                                    {
                                                                                                        "name": "Revenue",
                                                                                                        "id": "revenue",
                                                                                                        "type": "numeric",
                                                                                                        "format": FormatTemplate.money(0),
                                                                                                    },
                                                                                                    {
                                                                                                        "name": "Earnings Per Share",
                                                                                                        "id": "eps",
                                                                                                        "type": "numeric",
                                                                                                        "format": {"specifier": ".2f"},
                                                                                                    }
                                                                                                ],
                                                                                        id='luse-table',
                                                                                        editable=False,                  
                                                                                        row_deletable=False,             
                                                                                        sort_action="native",           
                                                                                        sort_mode="single",             
                                                                                        filter_action="native",        
                                                                                        page_action='native',
                                                                                        page_size = 7,             
                                                                                        style_table={'height': '340px', 'overflowY': 'auto'},
                                                                                        style_cell={'textAlign': 'left','padding': '5px', 'fontSize':15, 'font-family':'sans-serif'},
                                                                                        style_cell_conditional=[
                                                                                                                {
                                                                                                                    'if': {'column_id': c},
                                                                                                                    'textAlign': 'right'
                                                                                                                } for c in ['instrument','year', 'profit', 'revenue', 'eps']
                                                                                                            ],
                                                                                        style_as_list_view=False
                                                                                    )

                                                            ),
                                                
                           ]),
                          
                                    ],
                                    width=12
                                    ),
                           
                          
                           
                           ]) ,
                           

                ], className='div'),


html.Div([
                            html.P(dcc.Markdown(children=markdown_text6, className='footer2'))
            ], className='div')

]

)


         




if __name__ == '__main__':
    app.run_server(debug=False)