import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Sample Data
# Replace this with your career prediction data
data = {
    'Career': ['Data Scientist', 'Software Engineer', 'Product Manager', 'Designer', 'Business Analyst'],
    'Prediction Accuracy': [85, 78, 90, 72, 80],
    'Years of Study': [3, 4, 3, 2, 3]
}

df = pd.DataFrame(data)

# Create Dash App
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("Career Prediction Research Dashboard", style={'text-align': 'center'}),

    # Dropdown for Career Selection
    dcc.Dropdown(
        id="career-dropdown",
        options=[{"label": career, "value": career} for career in df['Career']],
        value="Data Scientist",
        style={'width': "50%"}
    ),

    # Graphs Section
    html.Div([
        dcc.Graph(id='accuracy-graph', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='study-graph', style={'display': 'inline-block', 'width': '50%'})
    ]),

    # Table or Additional Data Display
    html.Div(id='career-stats'),

    # Markdown for Insights and Explanation
    dcc.Markdown('''
    ## Research Insights:
    - **Data Scientist** is the most accurate career prediction at 85% accuracy.
    - Further analysis shows that years of study correlate with prediction accuracy.
    - Explore different careers using the dropdown menu for more insights.
    ''', style={'margin': '20px'})
])


# Callbacks for interactivity
@app.callback(
    [Output('accuracy-graph', 'figure'),
     Output('study-graph', 'figure'),
     Output('career-stats', 'children')],
    [Input('career-dropdown', 'value')]
)
def update_graphs(career):
    # Filter data based on dropdown selection
    filtered_data = df[df['Career'] == career]

    # Create Accuracy Graph
    accuracy_fig = px.bar(
        filtered_data,
        x="Career",
        y="Prediction Accuracy",
        title=f"Prediction Accuracy for {career}",
        labels={'Prediction Accuracy': 'Accuracy (%)'}
    )

    # Create Years of Study Graph
    study_fig = px.pie(
        filtered_data,
        names="Career",
        values="Years of Study",
        title=f"Years of Study for {career}"
    )

    # Career Stats
    stats = f"Career: {career}, Prediction Accuracy: {filtered_data['Prediction Accuracy'].values[0]}%, Years of Study: {filtered_data['Years of Study'].values[0]}"

    return accuracy_fig, study_fig, stats


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




