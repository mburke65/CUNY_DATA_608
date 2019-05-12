import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output
import dash_table
import json
from textwrap import dedent as d
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

pay_dataset =  pd.read_csv("filtered_nyc_payset.csv", low_memory = False)

available_indicators = pay_dataset['Agency Name'].unique()
calcs_indicators = {'Work Location Borough': ['nunique'],'Employee_Id':['nunique'], 'Title Description':['nunique'],
        'Regular Hours': ['sum'],'Regular Gross Paid':['mean'], 'OT Hours':['sum'],'Total OT Paid':['mean'],
        'Total Other Pay':['mean'], 'Total Pay':['mean']}

mappingtable = {'Work Location Borough': 'Boroughs (Unique)','Employee_Id':'Employees (Unique)',
 'Title Description':'Job Roles (Unique)','Regular Hours': 'Regular Hours (Sum)','Regular Gross Paid':'Gross Pay (Average)', 
 'OT Hours':'Overtime Hours (Sum)','Total OT Paid':'Overtime Pay (Average)','Total Other Pay': 'Other Pay (Average)', 
 'Total Pay':'Total Pay (Average)'}


print("readin")




def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#title
app.layout = html.Div(children=[
    html.H1(children='NYC Employee Payroll Project-Data 608',
    style={'font-style': 'bold'
    }),
    #subtitle1
    html.H4(children='About the Data:',
    style={'font-style': 'bold'
    }), 
    #first blurb
    html.Div(children='''
     The NYC Employee Payroll dataset provides gross pay information for every New York City employee from 2014 to 2018.\
     The employee payroll data can be found on the NYC Open Data website. \
     New York City's Office of Payroll Administration (OPA) regularly collects and maintains the employee data on the\
     NYC Open Data website. 

    '''), 
    #links 
    html.Div([html.A("NYC Open Data Employee Payroll Dataset & CSV Download", href=' https://data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-Fiscal-Year-/k397-673e', target="_blank")
        ]),
 

    #subtitle2
    html.H4(children='Dataset Transformation',
    style={'font-style': 'bold'
    }), 
    #first blurb
    html.Div([html.A("Dataset CSV Download (Large File)", href='https://data.cityofnewyork.us/api/views/k397-673e/rows.csv?accessType=DOWNLOAD&bom=true&format=true&delimiter=%3B', target="_blank")
        ]),
    html.Div([html.A("Dataset Columns", href='https://github.com/mburke65/CUNY_DATA_608/blob/master/Final%20Project/MB_Final/Dataset%20Columns.csv', target="_blank")
        ]),
    dcc.Markdown('''
     Steps:
     1. Read in the raw_csv from the NYC Open Data website (download via link above)
     2. Use script (view link below to access ipybn file) that does the following transformations:
     	a. Filtered for 'MANHATTAN', 'QUEENS', 'BRONX', 'BROOKLYN', & 'RICHMOND' boroughs
     	b. Filtered for full time, active employees 
     	c. Filtered for full year salaried employees
     	d. Removed null job titles
     	e. Removed 2014 as it is incomplete 
     	f. Converted all string values to uppercase & removed whitespace 
     	g. output the data to filtered_nyc_payset.csv. This is the base dataset for the dash application

    '''),  

    html.Div([html.A("Meaghan's Clean-up & EDA Jupyter Notebook", href='https://github.com/mburke65/CUNY_DATA_608/blob/master/Final%20Project/MB_Final/Project%20Data%20Cleaning%20Code%20-Meaghan%20Burke.ipynb', target="_blank")
        ]),




    #subtitle2
    html.H4(children='Goal:',
    style={'font-style': 'bold'
    }), 

    html.Div(children='''
        I would like to better understand how the city's financial resources are allocated. \
        I would also like to analyze and visualize the impact on NYC employees' salaries by occupation, \
        title, time, overtime and borough. Being a life-long New Yorker and daughter/sister to NYC civil servants, \
        I am very interested to see how NYC compensates its employees.
    '''
        ),


    #subtitle3
    html.H4(children='Data Exploration:',
    style={'font-style': 'bold'
    }), 

    dcc.Markdown('''
    The below time series clustered bar chart and data table are dynamically generated based on the two dropdown selections. The first dropdown\
    allows the user to select agency Name(s). The second dropdown allows the user to select the aggregation type.\

    Aggregation Types:

    1. Total Pay - average total pay by agency
    2. Employee_Id - unique count of employees by agency
    3. Work Location Borough - unique count of boroughs present in the data by agency
    4. Title Description - unique count of job roles by agency
    5. Regular Hours - sum of the total hours worked by agency
    6. Regular Gross Paid - average regular gross pay by agency
    7. OT Hours - sum of the total overtime hours by agency
    8. Total OT Paid - average overtime by agency
    9. Total Other Pay - average other pay by agency
    '''
        ),
    


    html.Div([#subtitle3
    html.H4(children='Data Exploration by Agency & Aggregation Type',
    style={'font-style': 'bold'
    }), 

	    html.Div([
		    dcc.Dropdown(
		    	id = "my-dropdown",
		    	options=[{'label': i, 'value': i} for i in available_indicators],
		    	value=['POLICE DEPARTMENT', 'FIRE DEPARTMENT'], #Initial values,
		    	
		    	multi=True
		)

		],
	        style={'width': '50%', 'display': 'inline-block'}),


	    html.Div([

		    dcc.Dropdown(
		    	id = "aggregator-dropdown",
		    	options=[{'label': i, 'value': i} for i in calcs_indicators],
		    	value='Total Pay', #Initial values,
		    	
		    	multi=False
		)

		],
	        style={'width': '50%', 'display': 'inline-block'}),

]),

    dcc.Graph(id='byborough_nosteward'),
html.Div([html.H5(children='General Commentary',
    style={'font-style': 'bold'
    }), 
    html.Div([html.Div(id='table-container')],
	        style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([dcc.Markdown('''

    General Findings:

    1. Most Employees (unique) - DEPT OF ED PEDAGOGICAL (NYC Teachers) 107,081 Unique Employees between 2015 -2018
    2. Most Titles (unique) -  DEPT OF HEALTH/MENTAL HYGIENE  & POLICE DEPARTMENT. Both departments have 235 unique job roles
    3. POLICE DEPARTMENT (sum) - POLICE DEPARTMENT works the most "regular hours" with a total sum of 391,341,006 hours 2015 -2018
    4. Highest Gross Pay (average) - OFFICE OF COLLECTIVE BARGAINING  with an average employee gross pay of $106,146.3
    5. Lowest Gross Pay (average) - DEPT OF ED PARA PROFESSIONALS with an average employee gross pay of $33,949.3
    6. Most Overtime (sum) - POLICE DEPARTMENT with 47,006,951.9 hours of overtime
    7. Highest Overtime Pay (average) - DEPARTMENT OF CORRECTION with $20,055.6 in overtime, on average
    8. Highest Total Other Pay (average) - DEPARTMENT OF SANITATION with $13,767.9 in other pay, on average
    9. Highest Total Pay (average)- OFFICE OF COLLECTIVE BARGAINING with a total $106,865.1, on average 
    '''
        )],style={'width': '50%', 'display': 'inline-block'}),
]), 

html.Div([html.H4(children='Pay Analysis',
    style={'font-style': 'bold'
    }), 
html.Div([dcc.Graph(id='Regularpay_scatter')],
	        style={'width': '50%', 'display': 'inline-block'}),

html.Div([dcc.Graph(id='overtime_scatter')],style={'width': '50%', 'display': 'inline-block'}),


]),

html.Div([html.H5(children='Pay Commentary',
    style={'font-style': 'bold'
    }),
html.Div([html.Div(id='regular_table_container')],
	        style={'width': '50%', 'display': 'inline-block'}),

html.Div([html.Div(id='overtime_table_container')],style={'width': '50%', 'display': 'inline-block'}),


]),

html.Div([dcc.Markdown('''

   ### Pay Findings:

   1. The above scatter charts and tables display employee pay as a\
   factor of hours worked, on average. The chart shows that each of the 148 NYC agencies\
   structures employee compensation differently. In some agencies, the employees are eligible for overtime.\
   Other agencies provide higher base salaries. 

   ### Future Enhancements:

   1. Within the agencies there is a huge disparity on job responsibility and pay. To better compare across\
   agencies, the data would need to be enriched with cross-agency mapping tables. For example, in the police department,\
   a Capitan in the police department is equivalent to a battalion chief in the Fire Department.


       '''
        )])




])


@app.callback(
    Output(component_id='byborough_nosteward', component_property='figure'),
    [Input(component_id='my-dropdown', component_property='value'),
     Input(component_id='aggregator-dropdown', component_property='value')


    ]
)
def update_output_div(input_value, selected_aggregator):
	df_plot = pay_dataset[pay_dataset['Agency Name'].isin(input_value)]
	df_plot= df_plot.groupby(['Fiscal Year','Agency Name'])[selected_aggregator].agg(calcs_indicators[selected_aggregator][0]).reset_index()
	df_plot = df_plot.pivot(index = 'Fiscal Year', columns='Agency Name', values=selected_aggregator).reset_index()

	print(df_plot)
	data_trace = []
	for x in df_plot.columns[1:]:
		trace = go.Bar(x=df_plot['Fiscal Year'], y=df_plot[x], name=str(x))
		data_trace.append(trace)
	return {
    'data': data_trace,
    'layout':
    go.Layout(
        title='{}'.format(mappingtable[selected_aggregator].title()),
        
        )}


@app.callback(
    Output(component_id='table-container', component_property='children'),
    [Input(component_id='my-dropdown', component_property='value'),
     Input(component_id='aggregator-dropdown', component_property='value')
     ])

def update_table(input_value, selected_aggregator):
	df_plot = pay_dataset[pay_dataset['Agency Name'].isin(input_value)]
	df_plot= df_plot.groupby(['Fiscal Year','Agency Name'])[selected_aggregator].agg(calcs_indicators[selected_aggregator][0]).reset_index()
	df_plot[selected_aggregator] = round(df_plot[selected_aggregator],1)

	df_plot = df_plot.pivot(index = 'Agency Name', columns='Fiscal Year', values=selected_aggregator).reset_index()
	
	return generate_table(df_plot)



@app.callback(
    Output(component_id='overtime_scatter', component_property='figure'),
    [Input(component_id='my-dropdown', component_property='value')])


def update_scatter(input_value):
	calcs_scatter = {'OT Hours': ['mean'], 'Total OT Paid':['mean']}
	df_plot = pay_dataset[pay_dataset['Agency Name'].isin(input_value)]
	df_plot= df_plot.groupby(['Agency Name']).agg(calcs_scatter).reset_index()
	df_plot.columns = df_plot.columns.droplevel(-1)
	df_plot = df_plot.loc[df_plot['OT Hours'] > 0 ]

	data_trace = []
	for x in df_plot['Agency Name'].unique():
		trace =  go.Scatter(x=df_plot.loc[df_plot['Agency Name']== x]['OT Hours'], 
			y= df_plot.loc[df_plot['Agency Name']== x]['Total OT Paid'], 
			text = df_plot.loc[df_plot['Agency Name']== x]['Agency Name'],
			name=str(x),
            mode='markers',
            opacity=0.7,
            marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    })
		data_trace.append(trace)

	return {
    'data': data_trace,
    'layout':
    go.Layout(
    	title= 'Overtime Pay vs. Overtime Hours (Average)',
        xaxis={'title': 'OT Hours (average)'},
        yaxis={'title': 'Total OT Paid (average)'},
       
        
        )}


@app.callback(
    Output(component_id='Regularpay_scatter', component_property='figure'),
    [Input(component_id='my-dropdown', component_property='value')])


def update_scatter(input_value):
	calcs_scatter = {'Regular Hours': ['mean'], 'Regular Gross Paid':['mean']}
	df_plot = pay_dataset[pay_dataset['Agency Name'].isin(input_value)]
	df_plot= df_plot.groupby(['Agency Name']).agg(calcs_scatter).reset_index()
	df_plot.columns = df_plot.columns.droplevel(-1)
	df_plot = df_plot.loc[df_plot['Regular Hours'] > 0 ]

	data_trace = []
	for x in df_plot['Agency Name'].unique():
		trace =  go.Scatter(x=df_plot.loc[df_plot['Agency Name']== x]['Regular Hours'], 
			y= df_plot.loc[df_plot['Agency Name']== x]['Regular Gross Paid'], 
			text = df_plot.loc[df_plot['Agency Name']== x]['Agency Name'],
			name=str(x),
            mode='markers',
            opacity=0.7,
            marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    })
		data_trace.append(trace)

	return {
    'data': data_trace,
    'layout':
    go.Layout(
    	title= 'Gross Pay vs. Regular Hours (Average)',
        xaxis={'title': 'Regular Hours (average)'},
        yaxis={'title': 'Regular Pay (average)'},
       
        
        )}


@app.callback(
    Output(component_id='regular_table_container', component_property='children'),
    [Input(component_id='my-dropdown', component_property='value') ])

def update_reg_table(input_value):
	calcs_scatter = {'Regular Hours': ['mean'], 'Regular Gross Paid':['mean'] ,'Employee_Id':['nunique'] }
	df_plot = pay_dataset[pay_dataset['Agency Name'].isin(input_value)]
	df_plot= df_plot.groupby(['Agency Name']).agg(calcs_scatter).reset_index()
	df_plot.columns = df_plot.columns.droplevel(-1)
	df_plot = df_plot.loc[df_plot['Regular Hours'] > 0 ]
	#df_plot = df_plot.sort_values('Regular Gross Paid', ascending = False)
	df_plot[['Regular Hours', 'Regular Gross Paid']] = df_plot[['Regular Hours', 'Regular Gross Paid']].round(1)
	return generate_table(df_plot)

@app.callback(
    Output(component_id='overtime_table_container', component_property='children'),
    [Input(component_id='my-dropdown', component_property='value') ])

def update_overtime_table(input_value):
	calcs_scatter = {'OT Hours': ['mean'], 'Total OT Paid':['mean'], 'Employee_Id':['nunique']}
	df_plot = pay_dataset[pay_dataset['Agency Name'].isin(input_value)]
	df_plot= df_plot.groupby(['Agency Name']).agg(calcs_scatter).reset_index()
	df_plot.columns = df_plot.columns.droplevel(-1)
	df_plot = df_plot.loc[df_plot['OT Hours'] > 0 ]
	#df_plot = df_plot.sort_values('Total OT Paid', ascending = False)
	df_plot[['OT Hours', 'Total OT Paid']] = df_plot[['OT Hours', 'Total OT Paid']].round(1)



	return generate_table(df_plot)












if __name__ == '__main__':
    app.run_server(debug=True)