from dash import dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd



drivers_df = pd.read_csv("data/formula1_2021season_drivers.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
table_cols = [
    'Abbreviation',
    'Number',
    'Team',
    'Country',
    'Podiums',
    'Points',
    'Grands Prix Entered',
    'World Championships',
    'Highest Grid Position',
    'Place of Birth'
]

# app.layout = dbc.Container(
#     dbc.Row([
#         dbc.Col([
#             dcc.Dropdown(
#                 options = ['a', 'b', 'c'],
#                 value = 'a',
#                 multi = False),
#         ])
#     ]),
#     dbc.Row([
#         dbc.Col([
#             'Select criteria to rank drivers by:',
#             dcc.Dropdown(
#                 id = "ranking-criteria",
#                 options = ['Podiums', 'Points', 'World Championships'],
#                 value = 'Podiums',
#                 multi = False,
#                 placeholder = 'Select a city'),
#         ]),
#         dbc.Col([
#             html.Iframe(
#                 id='ranking-plot',
#                 style={'border-width': '0', 'width': '100%', 'height': '400px'})
#         ], width=10)
#     ])
# )

app.layout = html.Div(
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id = 'driver-select',
                options = [driver for driver in drivers_df['Driver']],
                value = 'Max Verstappen',
                multi = False),
        ]),
        dbc.Col([
            # dash_table.DataTable(
            #     id = 'table',
            #     columns = [{'name': col, 'id': col} for col in table_cols],
            #     data = drivers_df[table_cols].to_dict('records')
            # )
            dash_table.DataTable(
                id = 'table',
                data = []
            )
        ]),
        dbc.Row([
            dbc.Col([
                'Select criteria to rank drivers by:',
                dcc.Dropdown(
                    id = "ranking-criteria",
                    options = ['Podiums', 'Points', 'World Championships'],
                    value = 'Podiums',
                    multi = False,
                    placeholder = 'Select a city'),
            ]),
            dbc.Col([
                html.Iframe(
                    id='ranking-plot',
                    style={'border-width': '0', 'width': '100%', 'height': '400px'})
            ], width=10)
        ])
    ])
)


@app.callback(
    Output('table', 'columns'),
    Output('table', 'data'),
    Input('driver-select', 'value')
)
def render_driver_table(driver_select):
    df = drivers_df.query("Driver == @driver_select")
    df = df[table_cols]
    return [{'name': col, 'id': col} for col in df.columns], df.to_dict('records')


@app.callback(
    Output('ranking-plot', 'srcDoc'),
    Input('ranking-criteria', 'value')
)
def plot_altair(ranking):
    if ranking == 'World Championships':
        df = drivers_df.sort_values(ranking, ascending=False).head(5)
    else:
        df = df = drivers_df.sort_values(ranking, ascending=False).head(7)
    chart = alt.Chart(df).mark_bar().encode(
        x=ranking,
        y=alt.Y('Driver', sort="-x")
    )
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)
