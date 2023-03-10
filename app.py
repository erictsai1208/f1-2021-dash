from dash import dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd


IMG_DIR = "\\img\\drivers\\"
drivers_df = pd.read_csv("data/formula1_2021season_drivers.csv")
laps_df = pd.read_csv("data/2021_all_laps_info.csv")
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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    dbc.Row([
        dbc.Col([
            'View driver information:',
            dcc.Dropdown(
                id = 'driver-select',
                options = [driver for driver in drivers_df['Driver']],
                value = 'Max Verstappen',
                multi = False,
                clearable = False),
        ], width=2),
        dbc.Row([
            dbc.Col([
                html.Img(id = 'image')
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
            ], width=10),
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                'Select criteria to rank drivers by:',
                dcc.Dropdown(
                    id = "ranking-criteria",
                    options = ['Podiums', 'Points', 'World Championships'],
                    value = 'Podiums',
                    multi = False,
                    clearable = False)
            ]),
            dbc.Col([
                html.Iframe(
                    id='ranking-plot',
                    style={'border-width': '0', 'width': '100%', 'height': '500px'})
            ], width=10)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    options = laps_df['GP'].unique().tolist(),
                    value = 'Bahrain Grand Prix',
                    multi = False,
                    clearable = False
                )
            ], width=3),
            dbc.Col([
                dcc.Checklist(
                    options = drivers_df['Driver'].tolist(),
                    value=['Max Verstappen'],
                    labelStyle={'display': 'block'},
                    style={"height":200, "width":200, "overflow":"auto"})
            ])
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
    Output('image', 'src'),
    Input('driver-select', 'value')
)
def display_image(driver_select):
    img_path = IMG_DIR + driver_select+ ".png"
    print(img_path)
    return img_path

@app.callback(
    Output('ranking-plot', 'srcDoc'),
    Input('ranking-criteria', 'value')
)
def plot_altair(ranking):
    # if ranking == 'World Championships':
    #     df = drivers_df.sort_values(ranking, ascending=False).head(5)
    # else:
    #     df = df = drivers_df.sort_values(ranking, ascending=False).head(7)
    chart = alt.Chart(drivers_df).mark_bar().encode(
        x=ranking,
        y=alt.Y('Driver', sort="-x")
    )
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)
