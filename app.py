import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from collections import Counter
import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Pre-calculations for performance
all_time = pd.read_csv(
    'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-overall.csv')

data_dict = {
    '1958': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1958.csv',
    '1959': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1959.csv',
    '1960': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1960.csv',
    '1961': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1961.csv',
    '1962': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1962.csv',
    '1963': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1963.csv',
    '1964': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1964.csv',
    '1965': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1965.csv',
    '1966': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1966.csv',
    '1967': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1967.csv',
    '1968': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1968.csv',
    '1969': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1969.csv',
    '1970': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1970.csv',
    '1971': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1971.csv',
    '1972': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1972.csv',
    '1973': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1973.csv',
    '1974': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1974.csv',
    '1975': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1975.csv',
    '1976': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1976.csv',
    '1977': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1977.csv',
    '1978': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1978.csv',
    '1979': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1979.csv',
    '1980': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1980.csv',
    '1981': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1981.csv',
    '1982': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1982.csv',
    '1983': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1983.csv',
    '1984': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1984.csv',
    '1985': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1985.csv',
    '1986': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1986.csv',
    '1987': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1987.csv',
    '1988': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1988.csv',
    '1989': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1989.csv',
    '1990': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1990.csv',
    '1991': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1991.csv',
    '1992': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1992.csv',
    '1993': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1993.csv',
    '1994': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1994.csv',
    '1995': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1995.csv',
    '1996': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1996.csv',
    '1997': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1997.csv',
    '1998': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1998.csv',
    '1999': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-1999.csv',
    '2000': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2000.csv',
    '2001': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2001.csv',
    '2002': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2002.csv',
    '2003': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2003.csv',
    '2004': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2004.csv',
    '2005': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2005.csv',
    '2006': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2006.csv',
    '2007': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2007.csv',
    '2008': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2008.csv',
    '2009': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2009.csv',
    '2010': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2010.csv',
    '2011': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2011.csv',
    '2012': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2012.csv',
    '2013': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2013.csv',
    '2014': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2014.csv',
    '2015': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2015.csv',
    '2016': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2016.csv',
    '2017': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2017.csv',
    '2018': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2018.csv',
    '2019': 'https://raw.githubusercontent.com/Safvenberger/Billboard-Hot-100/master/data/BillboardHot100-2019.csv'
}

app.layout = html.Div([
    html.Div([
            html.Div([
                ], style={'width': '30%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='year',
                    options=[{'label': i, 'value': i} for i in data_dict],
                    value='1958',
                    placeholder='Select a year'
                )
            ], style={'width': '10%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='week',
                    placeholder='Select a chart week',
                    disabled=False
                )
            ], style={'width': '10%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='artists',
                    placeholder='Select an artist'
                )
            ], style={'width': '20%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(
        id='main_graph',
        config={'displayModeBar': False}
        ),

    html.Div([
        html.Div(id='slider-show', children=[
            html.H4('Specify an interval of years where the artist appeared on the Billboard hot 100',
                    style={'text-align': 'center'}),
            dcc.RangeSlider(
                id='year_slider',
                allowCross=False
            )
        ]),

        html.Div(id='graph-show1', children=[
            dcc.Graph(
                id='graph_most_weeks',
                config={'displayModeBar': False}
            )
        ]),

        html.Div(id='item-show',
                 children=[
                     dcc.RadioItems(
                         id='Bar_select',
                         options=[
                             {'label': 'Artist', 'value': 'Artist_select'},
                             {'label': 'Song', 'value': 'Song_select'},
                         ],
                         value='Artist_select'
                     )
                 ]),

        html.Div(id='graph-show2', children=[
            dcc.Graph(
                id='graph_number_one',
                config={'displayModeBar': False}
            )
        ])
    ])

])


# Week options
@app.callback(dash.dependencies.Output('week', 'options'),
              [dash.dependencies.Input('year', 'value')])
def weeks(year_subset):

    if year_subset is None:
        return [{'label': i, 'value': i} for i in [None]]
    else:
        data = pd.read_csv(data_dict[year_subset])
        return [{'label': i, 'value': i} for i in data['Week'].unique()]


@app.callback(dash.dependencies.Output('week', 'value'),
              [dash.dependencies.Input('year', 'value')])
def week_value(year_subset):

    if year_subset is None:
        return None


# Artist options
@app.callback(dash.dependencies.Output('artists', 'options'),
              [dash.dependencies.Input('year', 'value')])
def artists(year_subset):

    if year_subset is None:
        data = all_time
    else:
        data = pd.read_csv(data_dict[year_subset])

    data.rename(index=str, columns={'Unnamed: 0': 'Position'}, inplace=True)

    art_list = [i.split('Featuring') for i in data['Artist_fix']]
    art = [item.strip() for sublist in art_list for item in sublist]

    count = Counter(art).most_common()
    count = [i[0] for i in count]

    return [{'label': i, 'value': i} for i in count]


# Slider for all years
@app.callback(dash.dependencies.Output('year_slider', 'max'),
              [dash.dependencies.Input('year', 'value'),
               dash.dependencies.Input('artists', 'value')
               ])
def slider_max(year_subset, artist_select):

    if year_subset is None:
        data = all_time
    else:
        data = pd.read_csv(data_dict[year_subset])

    data.rename(index=str, columns={'Unnamed: 0': 'Position'}, inplace=True)

    if year_subset is None and artist_select is not None:
        data_subset = data.loc[data['Artist'].str.contains(artist_select)]
        data_subset = data_subset.sort_values('Week')
        max_year = data_subset['Week'][-1][:4]
    else:
        max_year = '2019'

    return int(max_year)


@app.callback(dash.dependencies.Output('year_slider', 'min'),
              [dash.dependencies.Input('year', 'value'),
               dash.dependencies.Input('artists', 'value')
               ])
def slider_min(year_subset, artist_select):

    if year_subset is None:
        data = all_time
    else:
        data = pd.read_csv(data_dict[year_subset])

    data.rename(index=str, columns={'Unnamed: 0': 'Position'}, inplace=True)

    if year_subset is None and artist_select is not None:
        data_subset = data.loc[data['Artist'].str.contains(artist_select)]
        data_subset = data_subset.sort_values('Week')
        min_year = data_subset['Week'][0][:4]
    else:
        min_year = '1958'

    return int(min_year)


@app.callback(dash.dependencies.Output('year_slider', 'marks'),
              [dash.dependencies.Input('year', 'value'),
               dash.dependencies.Input('artists', 'value')
               ])
def slider_marks(year_subset, artist_select):

    if year_subset is None:
        data = all_time
    else:
        data = pd.read_csv(data_dict[year_subset])

    data.rename(index=str, columns={'Unnamed: 0': 'Position'}, inplace=True)

    if year_subset is None and artist_select is not None:
        data_subset = data.loc[data['Artist'].str.contains(artist_select)]
        data_subset = data_subset.sort_values('Week')
        year_list = data_subset['Week'].str.split('-', expand=True)[0].unique()
    else:
        year_list = list(range(1958, 2020))

    return {int(i): '{}'.format(i) for i in year_list}


@app.callback(dash.dependencies.Output('year_slider', 'value'),
              [dash.dependencies.Input('year', 'value'),
               dash.dependencies.Input('artists', 'value')
               ])
def slider_value(year_subset, artist_select):

    if year_subset is None:
        data = all_time
    else:
        data = pd.read_csv(data_dict[year_subset])

    data.rename(index=str, columns={'Unnamed: 0': 'Position'}, inplace=True)

    if year_subset is None and artist_select is not None:
        data_subset = data.loc[data['Artist'].str.contains(artist_select)]
        data_subset = data_subset.sort_values('Week')
        year_list = data_subset['Week'].str.split('-', expand=True)[0].unique().astype(int)
    else:
        year_list = list(range(1958, 2020))

    return [year_list[0], year_list[-1]]


# Hide graphs and items
@app.callback(dash.dependencies.Output('graph-show1', 'style'),
              [dash.dependencies.Input('year', 'value')])
def hide_graph(year):
    if year is not None:
        return {'display': 'inline-block'}
    else:
        return {'display': 'none'}


@app.callback(dash.dependencies.Output('graph-show2', 'style'),
              [dash.dependencies.Input('year', 'value')])
def hide_graph(year):
    if year is not None:
        return {'display': 'inline-block'}
    else:
        return {'display': 'none'}


@app.callback(dash.dependencies.Output('item-show', 'style'),
              [dash.dependencies.Input('year', 'value')])
def hide_item(year):
    if year is not None:
        return {'position': 'absolute', 'bottom': '400px', 'left': '850px', 'display': 'inline-block', 'z-index': '1'}
    else:
        return {'display': 'none'}


@app.callback(dash.dependencies.Output('slider-show', 'style'),
              [dash.dependencies.Input('year', 'value')])
def hide_slider(year):
    if year is None:
        return {'width': '90%', 'padding-left': '5%', 'padding-right': '4%'}
    else:
        return {'display': 'none'}


# Sub-graph 1
@app.callback(dash.dependencies.Output('graph_most_weeks', 'figure'),
              [dash.dependencies.Input('year', 'value'),
               dash.dependencies.Input('Bar_select', 'value')
               ])
def graph_weeks(year_subset, song_or_artist):

    if year_subset is None:
        data = all_time
    else:
        data = pd.read_csv(data_dict[year_subset])

    data.rename(index=str, columns={'Unnamed: 0': 'Position'}, inplace=True)

    data_song = data.groupby(['Week', 'Artist', 'Song']).sum().reset_index(level=[0, 1])
    data_song = data_song.groupby(['Song', 'Artist'])['Week'].value_counts().reset_index(level=[0, 1, 2],
                                                                                         name='Number_of_weeks')
    data_song = data_song.groupby(['Song', 'Artist']).sum().reset_index(level=[0, 1]).sort_values('Number_of_weeks',
                                                                                                  ascending=False)

    if song_or_artist == 'Artist_select':
        data_art = data.groupby(['Week', 'Artist']).sum().reset_index(level=[0, 1])
        data_art = data_art.groupby('Artist')['Week'].value_counts().reset_index(level=[0, 1], name='Number_of_weeks')
        data_art = data_art.groupby('Artist').sum().reset_index(level=[0]).sort_values('Number_of_weeks',
                                                                                       ascending=False)
        data_art = data_art.iloc[:10].reset_index(drop=True)

        plot_data = [
            go.Bar(
                x=data_art['Artist'],
                y=data_art['Number_of_weeks'],
                text=['<br><b>Artist:</b> ' + data_art['Artist'][i] + '<br><b>Number of weeks:</b> ' +
                      data_art['Number_of_weeks'][i].astype(str) for i, j in enumerate(data_art['Artist'])],
                hoverinfo='text'
            )
        ]

    else:
        data_song = data_song.iloc[:10].reset_index(drop=True)

        plot_data = [
            go.Bar(
                x=data_song['Song'],
                y=data_song['Number_of_weeks'],
                text=['<br><b>Song:</b> ' + data_song['Song'][i] + '<br><b>Artist:</b> ' + data_song['Artist'][i] +
                      '<br><b>Number of weeks:</b> ' +
                      data_song['Number_of_weeks'][i].astype(str) for i, j in enumerate(data_song['Artist'])],
                hoverinfo='text'
            )
        ]

    return {
        'data': plot_data,

        'layout': go.Layout(
            title='Most weeks on the Billboard hot 100 <br>',
            width=900,
            titlefont=dict(
                family='Old Standard TT, serif',
                size=22,
                color='black'
            ),

            xaxis=dict(
                title='',
                showgrid=False,

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),
            yaxis=dict(
                title='Position',
                autorange=False,
                range=[0, 55],
                zeroline=False,
                showgrid=False,

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),

            margin={'pad': 5},  # Graph margins
            hovermode='closest'  # Hover to the closest object

        )
    }


# Sub-graph 2
@app.callback(dash.dependencies.Output('graph_number_one', 'figure'),
              [dash.dependencies.Input('year', 'value'),
               dash.dependencies.Input('Bar_select', 'value')
               ])
def graph_one(year_subset, song_or_artist):

    if year_subset is None:
        data = all_time
    else:
        data = pd.read_csv(data_dict[year_subset])

    data.rename(index=str, columns={'Unnamed: 0': 'Position'}, inplace=True)
    data = data.loc[data['Position'] == 1]

    data_song = data.groupby(['Artist', 'Song']).sum().reset_index(level=[0, 1])
    data_song = data_song.groupby(['Artist', 'Song'])['Position'].sum().reset_index(level=[0, 1])
    data_song = data_song.sort_values('Position', ascending=False)

    if song_or_artist == 'Artist_select':
        data_art = data.groupby('Artist').sum().reset_index()
        data_art = data_art.groupby('Artist')['Position'].sum()
        data_art = data_art.sort_values(ascending=False)

        data_art = data_art.iloc[:10].reset_index()
        data_art = pd.DataFrame(data_art)

        plot_data = [
            go.Bar(
                x=data_art['Artist'],
                y=data_art['Position'],
                text=['<br><b>Artist:</b> ' + data_art['Artist'][i] + '<br><b>Number of weeks:</b> ' +
                      data_art['Position'][i].astype(str) for i, j in enumerate(data_art['Artist'])],
                hoverinfo='text'
            )
        ]
    else:
        data_song = data_song.iloc[:10].reset_index(drop=True)

        plot_data = [
            go.Bar(
                x=data_song['Song'],
                y=data_song['Position'],
                text=['<br><b>Song:</b> ' + data_song['Song'][i] + '<br><b>Artist:</b> ' + data_song['Artist'][i] +
                      '<br><b>Number of weeks:</b> ' +
                      data_song['Position'][i].astype(str) for i, j in enumerate(data_song['Artist'])],
                hoverinfo='text'
            )
        ]

    return {
        'data': plot_data,

        'layout': go.Layout(
            title='Most weeks as number one on the Billboard hot 100 <br>',
            width=900,
            titlefont=dict(
                family='Old Standard TT, serif',
                size=22,
                color='black'
            ),

            xaxis=dict(
                title='',
                showgrid=False,

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),
            yaxis=dict(
                title='Position',
                autorange=False,
                range=[0, 55],
                zeroline=False,
                showgrid=False,

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),

            margin={'pad': 5},  # Graph margins
            hovermode='closest'  # Hover to the closest object

        )
    }


# Main graph
@app.callback(dash.dependencies.Output('main_graph', 'figure'),
              [dash.dependencies.Input('year', 'value'),
               dash.dependencies.Input('artists', 'value'),
               dash.dependencies.Input('week', 'value'),
               dash.dependencies.Input('year_slider', 'value')])
def main_graph(year_subset, artist_subset, week_subset, slider_values):

    if year_subset is None:
        data = all_time
    else:
        data = pd.read_csv(data_dict[year_subset])

    data.rename(index=str, columns={'Unnamed: 0': 'Position'}, inplace=True)
    data['Artist'] = [re.sub('\$', 's', i).strip() for i in data['Artist']]

    if year_subset is None and artist_subset is not None:
        data_subset = data.loc[data['Artist'].str.contains(artist_subset)]
        data_subset = data_subset.sort_values('Week')

        if slider_values[0] != slider_values[1]:
            data_subset['Year'] = data_subset['Week'].str[:4].astype(int)
            lower_bound = slider_values[0] <= data_subset['Year']
            upper_bound = slider_values[1] >= data_subset['Year']
            data_subset = data_subset.loc[lower_bound & upper_bound]

        songs = [i for i in data_subset['Song'].unique()]
        plot_data = []

        for song_name in songs:
            trace = go.Scatter(
                x=data_subset.loc[data_subset['Song'] == song_name, 'Week'],  # Column to be plotted along y-axis
                y=data_subset.loc[data_subset['Song'] == song_name, 'Position'],  # Column to be plotted along x-axis

                text='<b>Week:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Week'] +
                     '<br><b>Position:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Position'].astype(str)
                     + '<br><b>Song:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Song'] +
                     '<br><b>Artist:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Artist'] +
                     '<br><b>Weeks on chart:</b> ' +
                     data_subset.loc[data_subset['Song'] == song_name,
                                     'Weeks on chart'].fillna(1.0).astype(int).astype(str),

                hoverinfo='text',
                mode='markers',
                name=song_name
            )
            plot_data.append(trace)

        plot_layout = go.Layout(

            title='Chart positions on the Billboard Hot 100 for {}<br>'.format(artist_subset),
            showlegend=True,
            titlefont=dict(
                family='Old Standard TT, serif',
                size=22,
                color='black'
            ),

            xaxis=dict(
                title='',
                showgrid=False,

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),
            yaxis=dict(
                title='Position',
                range=[101, -0.25],
                dtick=10,
                tickvals=[i for i in range(0, 101, 10)],
                ticktext=[1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                autorange=False,
                zeroline=False,
                showgrid=False,

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),
            margin={'l': 100, 'b': 40, 't': 100, 'r': 100, 'pad': 5},
            hovermode='closest'  # Hover to the closest object
        )

    elif year_subset is not None and artist_subset is not None and data['Artist'].str.contains(artist_subset).any():
        data_subset = data.loc[data['Artist'].str.contains(artist_subset)]
        songs = [i for i in data_subset['Song'].unique()]

        plot_data = []
        for song_name in songs:
            trace = go.Scatter(
                x=data_subset.loc[data_subset['Song'] == song_name, 'Week'],  # Column to be plotted along y-axis
                y=data_subset.loc[data_subset['Song'] == song_name, 'Position'],  # Column to be plotted along x-axis

                text='<b>Week:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Week'] +
                     '<br><b>Position:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Position'].astype(str)
                     + '<br><b>Song:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Song'] +
                     '<br><b>Artist:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Artist'] +
                     '<br><b>Weeks on chart:</b> ' +
                     data_subset.loc[data_subset['Song'] == song_name,
                                     'Weeks on chart'].fillna(1.0).astype(int).astype(str),

                hoverinfo='text',
                mode='markers',
                name=song_name
            )
            plot_data.append(trace)

        plot_layout = go.Layout(

            title='Chart positions on the Billboard Hot 100 for {} during {} <br>'.format(artist_subset, year_subset),
            showlegend=True,
            titlefont=dict(
                family='Old Standard TT, serif',
                size=22,
                color='black'
            ),

            xaxis=dict(
                title='',
                showgrid=False,
                autorange=False,
                range=[str(year_subset) + '-01-01', str(year_subset) + '-12-31'],
                tickmode='linear',
                dtick='M1',
                tickformat='%b',
                tickprefix='                        ',

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),
            yaxis=dict(
                title='Position',
                range=[101, -0.25],
                dtick=10,
                tickvals=[i for i in range(0, 101, 10)],
                ticktext=[1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                autorange=False,
                zeroline=False,
                showgrid=False,

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),
            margin={'l': 100, 'b': 40, 't': 100, 'r': 100, 'pad': 5},
            hovermode='closest'  # Hover to the closest object
        )

    elif year_subset is not None and week_subset is not None and data['Week'].str.contains(week_subset).any():
        data_subset = data.loc[data['Week'] == week_subset]
        data_subset_week = data_subset.fillna({'Last week': 101})
        data_subset_week['Delta week'] = data_subset_week['Last week'].astype(int) - data_subset_week['Position']

        data_subset_week.sort_values('Delta week', ascending=False, inplace=True)
        data_subset_week = data_subset_week.iloc[[0, 1, 2, -3, -2, -1]]

        plot_data = [
            go.Scatter(
                x=[1, 1, 1, 4, 4, 4, 7, 7, 7],
                y=[2.5, 9.5, 16.5, 2.5, 9.5, 16.5, 2.5, 9.5, 16.5],
                mode='text',
                text=['<b style="color:#cd7f32"> #3', '<b style="color:silver"> #2', '<b style="color:gold"> #1',
                      '<b style="color:green">+' + data_subset_week['Delta week'].astype(str)[2],
                      '<b style="color:green">+' + data_subset_week['Delta week'].astype(str)[1],
                      '<b style="color:green">+' + data_subset_week['Delta week'].astype(str)[0],
                      '<b style="color:red">' + data_subset_week['Delta week'].astype(str)[-3],
                      '<b style="color:red">' + data_subset_week['Delta week'].astype(str)[-2],
                      '<b style="color:red">' + data_subset_week['Delta week'].astype(str)[-1]],
                hoverinfo='none',
                textfont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='#000000'
                )
            )
        ]

        plot_layout = go.Layout(
            title='Chart details on the Billboard Hot 100 during {} <br>'.format(week_subset),
            xaxis=dict(
                range=[0, 10],
                visible=False,
                zeroline=False,
                showgrid=False
            ),
            yaxis=dict(
                range=[0, 21],
                visible=False,
                zeroline=False,
                showgrid=False
            ),

            annotations=[
                # Top 3 songs
                dict(
                    x=2,
                    y=20,
                    xref='x',
                    yref='y',
                    text='<b style="font-size:14px"> Most popular songs for the week {}</b>'.format(week_subset),
                    showarrow=False
                ),

                dict(
                    x=2,
                    y=2.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset['Song'][2] + '</b>' + '<br>' + data_subset['Artist'][2],
                    showarrow=False
                ),
                dict(
                    x=2,
                    y=9.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset['Song'][1] + '</b>' + '<br>' + data_subset['Artist'][1],
                    showarrow=False
                ),
                dict(
                    x=2,
                    y=16.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset['Song'][0] + '</b>' + '<br>' + data_subset['Artist'][0],
                    showarrow=False
                ),

                # Biggest climbers
                dict(
                    x=5,
                    y=20,
                    xref='x',
                    yref='y',
                    text='<b style="font-size:14px"> Most positions gained compared to the previous week.</b> <br>',
                    showarrow=False
                ),

                dict(
                    x=5,
                    y=2.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset_week['Song'][2] + '</b>' + '<br>' + data_subset_week['Artist'][2],
                    showarrow=False
                ),
                dict(
                    x=5,
                    y=9.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset_week['Song'][1] + '</b>' + '<br>' + data_subset_week['Artist'][1],
                    showarrow=False
                ),
                dict(
                    x=5,
                    y=16.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset_week['Song'][0] + '</b>' + '<br>' + data_subset_week['Artist'][0],
                    showarrow=False
                ),

                # Biggest losers
                dict(
                    x=8,
                    y=20,
                    xref='x',
                    yref='y',
                    text='<b style="font-size:14px"> Most positions lost compared to the previous week.</b>',
                    showarrow=False
                ),

                dict(
                    x=8,
                    y=2.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset_week['Song'][-3] + '</b>' + '<br>' + data_subset_week['Artist'][-3],
                    showarrow=False
                ),
                dict(
                    x=8,
                    y=9.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset_week['Song'][-2] + '</b>' + '<br>' + data_subset_week['Artist'][-2],
                    showarrow=False
                ),
                dict(
                    x=8,
                    y=16.5,
                    xref='x',
                    yref='y',
                    text='<b>' + data_subset_week['Song'][-1] + '</b>' + '<br>' + data_subset_week['Artist'][-1],
                    showarrow=False
                )
            ],
        )

    elif year_subset is None and artist_subset is None and week_subset is None:
        plot_data = [go.Scatter(
                x=[1],
                y=[2],
                mode='text',
                text="Select an artist to view their historical positions on the Billboard hot 100.",
                hoverinfo='none',
                textfont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='#000000'
                )
        )]

        plot_layout = go.Layout(
            xaxis=dict(
                visible=False,
                zeroline=False,
                showgrid=False),

            yaxis=dict(
                visible=False,
                zeroline=False,
                showgrid=False),

            )

    else:
        data_subset = data[data['Position'] <= 3]

        plot_data = []
        for song_name in data_subset['Song'].unique():
            trace = go.Scatter(
                x=data_subset.loc[data_subset['Song'] == song_name, 'Week'],  # Column to be plotted along y-axis
                y=data_subset.loc[data_subset['Song'] == song_name, 'Position'],  # Column to be plotted along x-axis

                text='<b>Week:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Week'] +
                     '<br><b>Song:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Song'] +
                     '<br><b>Artist:</b> ' + data_subset.loc[data_subset['Song'] == song_name, 'Artist'] +
                     '<br><b>Weeks on chart:</b> ' +
                     data_subset.loc[data_subset['Song'] == song_name,
                                     'Weeks on chart'].fillna(1.0).astype(int).astype(str),

                hoverinfo='text',
                mode='markers+lines',
                name=song_name
            )
            plot_data.append(trace)

        plot_layout = go.Layout(
            title='Top 3 charting songs for each week during {}'.format(year_subset),

            xaxis=dict(
                title='',
                showgrid=False,
                autorange=False,
                range=[str(year_subset) + '-01-01', str(year_subset) + '-12-31'],
                tickmode='linear',
                dtick='M1',
                tickformat='%b',
                tickprefix='                        ',

                titlefont=dict(
                    family='Old Standard TT, serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=14)
            ),
            yaxis=dict(
                title='Position',
                range=[3.5, 0.5],
                tickvals=[i for i in range(3, 0, -1)],
                ticktext=[3, 2, 1],
            ),
            margin={'pad': 5},
            hovermode='closest'
        )

    return {
        'data': plot_data,
        'layout': plot_layout

    }


if __name__ == '__main__':
    app.run_server()
