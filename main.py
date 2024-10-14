from http.cookiejar import debug

import dash
from click import style
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('../Datasets/Data_final.csv')
Careers = data['Career'].unique()


# Define the categories
categories = {
    'Technology & Engineering': ['Software Developer', 'Web Developer', 'Data Analyst', 'IT Support Specialist',
                                 'Game Developer', 'Aerospace Engineer', 'Electrical Engineer',
                                 'Mechanical Engineer', 'Civil Engineer', 'Robotics Engineer', 'Electronics Design Engineer',
                                 'Industrial Engineer', 'Biomedical Engineer', 'IT Project Manager'],
    'Healthcare': ['Nurse', 'Physician', 'Pharmacist', 'Psychologist', 'Pediatric Nurse', 'Speech Therapist',
                   'Physical Therapist', 'Dental Hygienist', 'Pediatrician', 'Chiropractor', 'Radiologic Technologist',
                   'Speech Pathologist', 'Genetic Counselor', 'Occupational Therapist', 'Marriage Counselor'],
    'Creative & Arts': ['Graphic Designer', 'Architect', 'Artist', 'Fashion Designer', 'Event Photographer',
                        'Musician', 'Film Director', 'Fashion Stylist'],
    'Business & Finance': ['Accountant', 'Marketing Manager', 'Salesperson', 'Financial Analyst', 'Marketing Coordinator',
                           'Marketing Analyst', 'Financial Planner', 'Financial Auditor', 'Advertising Executive',
                           'IT Project Manager', 'Investment Banker', 'Public Relations Specialist', 'Tax Accountant',
                           'Tax Collector', 'Administrative Officer'],
    'Science & Research': ['Research Scientist', 'Astronomer', 'Biologist', 'Environmental Scientist', 'Zoologist',
                           'Geologist', 'Biomedical Researcher', 'Forensic Scientist', 'Wildlife Biologist',
                           'Marine Biologist', 'Wildlife Conservationist', 'Environmental Engineer'],
    'Education': ['Teacher', 'Elementary School Teacher'],
    'Law & Social Services': ['Lawyer', 'Human Rights Lawyer', 'HR Recruiter', 'Human Resources Manager', 'Police Officer',
                              'Police Detective', 'Social Worker', 'Diplomat', 'Rehabilitation Counselor',
                              'Customs and Border Protection Officer', 'Foreign Service Officer'],
    'Other': ['Chef', 'Event Planner', 'Real Estate Agent', 'Air Traffic Controller', 'Urban Planner', 'Airline Pilot',
              'Sports Coach', 'Quality Control Inspector', 'Forestry Technician', 'Video Game Tester', 'Product Manager']
}

# Add category column to the DataFrame
data['Category'] = data['Career'].apply(lambda x: next((k for k, v in categories.items() if x in v), 'Other'))
categoryList = data['Category'].unique()

# To get the category mean
df = pd.DataFrame(data)

# Drop the 'Career' column
df.drop(['Career'], axis=1, inplace=True)

mean_by_category = df.groupby('Category').mean()
def cal_cognitive_aptitude(career):
    result = (mean_by_category['Numerical Aptitude'][career] + mean_by_category['Spatial Aptitude'][career] + mean_by_category['Perceptual Aptitude'][career] +
    mean_by_category['Abstract Reasoning'][career] + mean_by_category['Verbal Reasoning'][career]) / 5
    result = (result/10)*100
    return round(result, 2)

def emotional_stability(career):
    result = ((mean_by_category['A_score'][career] + mean_by_category['E_score'][career])/ mean_by_category['N_score'][career])
    result = (result/10)*100
    return round(result, 2)

def creativity_index(career):
    result = ((mean_by_category['O_score'][career] * mean_by_category['Abstract Reasoning'][career]))
    # result = ((mean_by_category['O_score'][career] + mean_by_category['Abstract Reasoning'][career]) / 2)
    result = (result/100)*100
    return round(result, 2)

def problem_solving_efficiency(career):
    result = ((mean_by_category['Numerical Aptitude'][career] + mean_by_category['Perceptual Aptitude'][career] + mean_by_category['Abstract Reasoning'][career]) / 3)
    result = (result/10)*100
    return round(result, 2)

def social_cognitive_index(career):
    result = ((mean_by_category['A_score'][career] + mean_by_category['E_score'][career] + mean_by_category['Verbal Reasoning'][career]) / 3)
    result = (result/10)*100
    return round(result, 2)


import plotly.graph_objects as go


def update_graphs(df, categories):
    charts = []  # List to store the plots

    # Loop over each category to create a line plot
    for i in categories:
        grouped_data = df[df['Category'] == i]  # Filter data for the specific category

        # Create a line plot for each category
        fig = go.Figure()
        for col in df.columns.drop('Category'):  # Plot all columns except 'Category'
            fig.add_trace(go.Scatter(
                x=grouped_data.index,
                y=grouped_data[col],
                mode='lines+markers',
                name=col
            ))
        # Update layout and title for each figure
        fig.update_layout(
            title=f"Line Plot for {i}",
            xaxis_title="Index",
            yaxis_title="Value",
            legend_title="Aptitude/Score",
        )
        charts.append(fig)  # Append the figure to the list of charts
    return charts  # Return the list of figures

graphs = update_graphs(df, categories)






# mean Categories and their mean values for each score/aptitude
categories_m = list(mean_by_category.keys())
scores = list(mean_by_category[categories_m[0]].keys())

# Prepare the data for the bar chart
data = []
for category in categories_m:
    data.append(go.Bar(
        x=scores,
        y=[mean_by_category[category][score] for score in scores],
        name=category
    ))
# Layout for the chart
layout = go.Layout(
    title='Comparison of Mean Scores and Aptitudes by Category',
    xaxis=dict(title='Scores/Aptitude'),
    yaxis=dict(title='Mean Values'),
    barmode='group',
    legend=dict(title='Category'),
    margin=dict(l=40, r=40, t=40, b=120)
)

# Create the figure
mean_fig = go.Figure(data=data, layout=layout)












# Create scatter plot with regression line using Plotly
def createScatteredPlotWithRegressionline(xparam, yparam, figname):
    """
    Creates a scatter plot with a regression line using the given parameters.

    Parameters:
    df (DataFrame): The DataFrame containing the data.
    xparam (str): The column name for the x-axis data.
    yparam (str): The column name for the y-axis data.
    figname (str): The title of the figure.

    Returns:
    fig (Figure): A Plotly Figure object with the scatter plot and regression line.
    """
    fig = go.Figure()

    # Add scatter plot for the data points
    fig.add_trace(go.Scatter(
        x=df[xparam],
        y=df[yparam],
        mode='markers',
        marker=dict(color='blue', opacity=0.5),
        name='Data points'
    ))

    # Calculate the regression line parameters (slope m and intercept b)
    m, b = np.polyfit(df[xparam], df[yparam], 1)

    # Add the regression line to the plot
    fig.add_trace(go.Scatter(
        x=df[xparam],
        y=m * df[xparam] + b,
        mode='lines',
        line=dict(color='red'),
        name='Regression Line'
    ))

    # Add labels and title to the plot
    fig.update_layout(
        title=f"Relationship Between {xparam} and {yparam}",
        xaxis_title=xparam,
        yaxis_title=yparam,
        showlegend=True
    )

    return fig

fig = createScatteredPlotWithRegressionline('C_score', 'Numerical Aptitude', 'Conscientiousness vs Numerical Aptitude')
figii = createScatteredPlotWithRegressionline('O_score', 'Abstract Reasoning', 'Openness vs Abstract Reasoning')
figiii = createScatteredPlotWithRegressionline('N_score', 'Perceptual Aptitude', 'Conscientiousness vs Numerical Aptitude')
figiv = createScatteredPlotWithRegressionline('E_score', 'Verbal Reasoning', 'Extraversion score vs Verbal Reasoning')







font_awesome_kit= 'https://kit.fontawesome.com/a771114d47.js'
font_awesome_cdn= 'https://pro.fontawesome.com/releases/v5.8.2/css/all.css'
meta_tags = [{"name": "viewport", "content": "width = device-width"}]
external_stylesheet = [font_awesome_cdn, meta_tags]
app = dash.Dash(__name__, external_stylesheets = external_stylesheet)

app.layout= html.Div([
    # title container
    html.Div([
        html.H2('CAREER PREDICTION ANALYSIS', className='titleText'),
        html.P('When energy stops, passion drives...', className='titleTextP')
    ], className='titleContainer card'),
    html.Div([
        html.Div(
            [
                dcc.Graph(figure=graph, style={'display': 'inline-block'}, className='graphfig') for graph in graphs
            ]
        ),
    ], className='graph', style={'margin-top': '20px'}),
    html.H4('GROUPED BAR CHART FOR CAREER CATEGORIES', className='titleText text_center'),
        dcc.Graph(
            id='grouped-bar-chart',
            figure=mean_fig
        ),

    html.H4('ANALYTICS BASED ON CAREER CATEGORY', className='titleText text_center'),

    # main section
    html.Div([
        # Dominant with big and small
        html.Div([
            html.Div([

                html.Div([

                    html.Div([
                        html.P(dcc.Markdown("""
                                                Below table shows an **exploration** of the data of **156** people
                                            """), style={"text-align": "justify"}),
                        html.Table([
                            html.Thead([
                                html.Tr([
                                    html.Td('Career'),
                                    html.Td('Cognitive Aptitude Score'),
                                    html.Td('Emotional Stability Index ((A + E + N)/3)'),
                                    html.Td('Openness and Creativity Index ((O + Abst)/2)'),
                                    html.Td('Problem Solving Efficiency ((Num + Per + Abst)/ 3)'),
                                    html.Td('Social-Cognitive Index ((A + E + Ver)/3)')
                                ], className='header_hover')
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td(career),
                                    html.Td(str(cal_cognitive_aptitude(career)) +  '%'),
                                    html.Td(str(emotional_stability(career)) + '%'),
                                    html.Td(str(creativity_index(career)) + '%'),
                                    html.Td(str(problem_solving_efficiency(career)) + '%'),
                                    html.Td(str(social_cognitive_index(career)) + '%')
                                ], className='hover_only_row')for career in categories
                            ])
                        ], className="table_style")
                    ], className="table dominant-column card_outline", style={'overflow': 'scroll'}),
                    html.Div([], style={'height': '30px'}),
                    # Relationship fig 1
                    html.Div([
                        dcc.Graph(figure=fig)
                    ], className='dominant-column card_outline'),
                ], className=''),

                # html.Div("Juxtaposed Content", className='juxtaposed-column'),
                html.Div([
                    html.P(dcc.Markdown("""
                        **Career Table**
                    """), style={"text-align": "justify"}),

                html.Div([], id='selectCategoryOutput')
                ], className='card_outline trans sub_column'
                         ),
            ], className='flex_row flex_row_stretch')
        ], className='dominant'),

        # artcle balanced column
        html.Div([

            # dcc.Dropdown(categoryList, categoryList[0], searchable=True, id='selectCategory'),
            dcc.Dropdown(
                    id="selectCategory",
                    options=[{"label": Category, "value": Category} for Category in categoryList],
                    value='Education',
                ),

            html.Div([
                dcc.Graph(id='selectCategoryPieFig', style={'width': '100%'}),
                dcc.Graph(id='selectCategoryBarFig', style={'width': '100%', 'margin-top': '-80px'})
            ])

        ], className='balanced-column card'),
    ], className='mainContainer flex_row flex_row_stretch'),

    # Research Question
    html.Div([
        html.H4('RESEARCH OBSERVATION', className='titleText text_center'),
        html.P("Research Question 1: How do personality traits (O_score, C_score, E_score, A_score, N_score) influence career choice? ", className='qt'),
        html.Div("Observation: Individuals with high Openness to Experience (O_score) are more likely to pursue creative careers, while those with high Conscientiousness (C_score) are more likely to pursue structured, detail-oriented careers (e.g., accounting, law).  ", className='card_outline'),

        html.P(
            "Research Question 2: Is there a correlation between personality traits (Big Five scores) and cognitive aptitudes (Numerical, Spatial, Perceptual, Abstract, Verbal Reasoning)? ", className='qt'),
        html.Div([
            html.Div([
                dcc.Graph(figure=figii)
            ], className='card_outline questioncol'),
            html.Div([
                dcc.Graph(figure=figiii)
            ], className='card_outline questioncol'),
        ], className="questionrow"),

        html.P(
            "Research Question 3: Can personality traits be used to predict cognitive aptitudes in a workplace context? ", className='qt'),
        html.Div([
            html.Div([
                dcc.Graph(figure=fig)
            ], className='card_outline questioncol'),
            html.Div([
                dcc.Graph(figure=figiv)
            ], className='card_outline questioncol'),
        ], className="questionrow"),

        html.P("Research Question 4: Are certain careers more likely to attract individuals with specific combinations of aptitudes (Numerical, Spatial, Perceptual) and personality traits?", className='qt'),
        html.Div([
            html.P("Observation: Artistic careers are more likely to attract people with high Openness (O_score) and Abstract Reasoning, while technical careers (like IT or engineering) may attract people with higher Spatial Aptitude. ", className="card_outline", style={"width": "100%"})
        ], className="questionrow"),

    ], className=''),


    html.P("One Prediction at a time @ 2024", className="text_center footer")
], className='Container flex_col')
# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
@app.callback(
    [Output('selectCategoryOutput', 'children'),
    Output('selectCategoryPieFig', 'figure'),
    Output('selectCategoryBarFig', 'figure')],
    [Input('selectCategory', 'value')]
)

def displayCategoryOutput(category):
    nkey = df.keys().drop('Category')
    filtered_job = categories[category]
    newdf = pd.DataFrame({i: mean_by_category[i][category] for i in nkey}, index=['Education'])
    melted_df = newdf.melt(var_name='Aptitude/Score', value_name='Value')

    selectCategoryOutput = html.Table([
            html.Thead([
                html.Tr([
                    html.Td(category),
                ], className='header_hover')
            ]),
            html.Tbody([
                html.Tr([html.Td(career)], className='hover_only_row') for career in filtered_job
            ])
        ], className="table_style")

    selectCategoryPieFig =  px.pie(
        melted_df,
        names='Aptitude/Score',
        values='Value',
        title="Career Score and Aptitude for " + category,
    )

    selectCategoryBarFig = px.bar(
        melted_df,
        x='Aptitude/Score',  # Use column names for the x-axis
        y='Value',  # Use values for the y-axis (bar heights)
        labels={'Value': 'Score/Percentage'},  # Label the y-axis
        color='Aptitude/Score',  # Color bars by category
    )


    return selectCategoryOutput, selectCategoryPieFig, selectCategoryBarFig



# for i in categories:
#     # print(i)
#     grouped_data = df[df['Category'] == i]
#     grouped_data.plot()
#     plt.title(i)
#     plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    app.run_server(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
