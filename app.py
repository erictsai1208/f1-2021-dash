from dash import dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd


IMG_DIR = "assets/img/drivers/"
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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div([
    dbc.Row([
        html.H1("2021 Formula 1 Statistics", style={"text-align": "center"}),
    ]),
    dbc.Row([
        dbc.Col([
            'View driver information:',
            dcc.Dropdown(
                id = 'driverinfo-select',
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
                dash_table.DataTable(
                    id = 'table',
                    data = []
                )
            ], width=10),
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                'Rank by:',
                dcc.Dropdown(
                    id = 'ranking-criteria',
                    options = ['Podiums', 'Points', 'World Championships'],
                    value = 'Podiums',
                    multi = False,
                    clearable = False)
            ], width=1),
            dbc.Col([
                html.Iframe(
                    id='ranking-plot',
                    style={'border-width': '0', 'width': '100%', 'height': '500px'})
            ]),
            dbc.Col([
                dbc.Row([
                    dcc.Dropdown(
                        id = 'gp-select',
                        options = laps_df['GP'].unique().tolist(),
                        value = 'Bahrain Grand Prix',
                        multi = False,
                        clearable = False)
                ]),
                dbc.Row([
                    dcc.Checklist(
                        id = 'driver-select',
                        options = laps_df['name'].unique().tolist(),
                        value=['Max Verstappen', 'Lance Stroll', 'Lando Norris'],
                        labelStyle={'display': 'block'})
                ])
            ], width=2),
            dbc.Col([
                html.Iframe(
                    id='laptime-boxplot',
                    style={'border-width': '0', 'width': '100%', 'height': '500px'})
            ])
        ]),
    ])
])


@app.callback(
    Output('table', 'columns'),
    Output('table', 'data'),
    Input('driverinfo-select', 'value')
)
def render_driver_table(driverinfo_select):
    df = drivers_df.query("Driver == @driverinfo_select")
    df = df[table_cols]
    return [{'name': col, 'id': col} for col in df.columns], df.to_dict('records')

@app.callback(
    Output('image', 'src'),
    Input('driverinfo-select', 'value')
)
def display_image(driverinfo_select):
    img_path = IMG_DIR + driverinfo_select+ ".png"
    return img_path

@app.callback(
    Output('ranking-plot', 'srcDoc'),
    Input('ranking-criteria', 'value')
)
def plot_ranking(ranking):
    chart = alt.Chart(drivers_df, title="Ranking by number of " + ranking).mark_bar().encode(
        x = ranking,
        y = alt.Y('Driver', sort="-x")
    )
    return chart.to_html()


@app.callback(
    Output('laptime-boxplot', 'srcDoc'),
    Input('driver-select', 'value'),
    Input('gp-select', 'value')
)
def plot_laptime_boxplot(driver_select, gp_select):
    df = laps_df.query("GP == @gp_select")
    df = df.query("name in @driver_select")
    chart = alt.Chart(df, title="Laptime distribution of each driver").mark_boxplot(size=30).encode(
        y = alt.Y("lap_time_ms", title='Laptime', scale=alt.Scale(zero=False)),
        x = alt.X("name", title='Driver', axis=alt.Axis(labelAngle=-45)),
        color = alt.Color("name", legend=None)
    ).properties(
        width=400
    )
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)

server = app.server
