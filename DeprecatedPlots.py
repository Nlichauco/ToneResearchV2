import csv

import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator

symbols = []
raw_symbols = SymbolValidator().values
for i in range(0, len(raw_symbols), 12):
    symbols.append(raw_symbols[i])


def GetCols(filename, col):
    df = pd.read_csv(filename, usecols=[col])
    list = df.keys()
    ToneScores = df[list[0]].tolist()
    return ToneScores


def GetCovData(country):
    if country == "US":
        Covid_Data = GetCols("res/CovidData/UScovidAVG.csv", 0)
    elif country == "UK":
        Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
    return Covid_Data


def FormatFig(Covid_Data, fig, tone, country, weeks):
    if country == "UK":
        source = "GRD"
    else:
        source = "Guardian"
    fig.update_layout(
        yaxis2=dict(title="Weekly Avg. COVID-19 Cases in the " + country, titlefont=dict(size=18), range=[0, 50000],
                    anchor="x", overlaying="y", side="right"))
    fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='COVID-19 Cases', yaxis='y2', fill='tozeroy'))
    fig.update_layout(title_text="<b>" + source + "</b>")
    fig.update_layout(title_x=.01, paper_bgcolor="#FFF",
                      plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(title_font_size=20, width=900, height=520, autosize=True,
                      margin=dict(l=100, r=10, b=100, t=100, pad=5))
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      margin=dict(l=0, r=50, ))
    fig.update_yaxes(gridcolor='black')
    return fig


# same tone mutliple desks
def makePlot(filenames, country, tone, tone_col):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        fname = fname[start + 1:end]
        data = GetCols(filenames[i], tone_col)
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=fname, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))
    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, showgrid=False)
    fig.update_yaxes(title_text="Weekly Avg. " + tone + " Tone Scores", title_font_size=18, range=[.5, 1],
                     showgrid=False)
    Covid_Data = GetCovData(country)
    FormatFig(Covid_Data, fig, tone, country, weeks)
    # fig.write_image("fig1.png", width=1200, height=600, scale=1)
    # fig.write_image("fig1.png")
    fig.show()


"""
Used to Plot average of a tone score across multiple desks
Args:
    filenames: List of files you want to plot from
    source_1: News source one
    source_2: Another News source
    tone: String literal of the tone you want to plot, ex. "Analytical"
    tone_col: Singular Index associated with what you want to plot

Returns:
    Nothing, creates a plot.
    """


def crossPlot(filenames, source_1, source_2, tone, tone_col):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        if fname.find("Guardian") != -1:
            fname = fname[start + 1:end + 1]
            traceName = "GRD " + fname[:fname[i].find(".")]
        else:
            fname = fname[start + 1:end + 1]
            traceName = "Guardian " + fname[:fname[i].find(".")]
        data = GetCols(filenames[i], tone_col)
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))

    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, range=[-.25, 42.15])
    fig.update_yaxes(title_text="Weekly Avg. " + tone + " Tone Scores", title_font_size=18, range=[.5, 1])
    fig.update_layout(title_text="<b>" + source_1 + " Vs " + source_2 + "</b>")
    graph_setup(fig)
    saveName = tone + ".png"
    fig.update_yaxes(gridcolor='black')
    # fig.write_image(saveName, width=1200, height=600, scale=1)
    fig.show()


"""
Plots all the ratio tone scores of one tone given multiple sections
Args:
    filenames: List of files you want to plot from
    country: Country of the news source you are plotting from
    tone: String literal of the tone you want to plot, ex. "Analytical"
    tone_col: Singular Index associated with what you want to plot
    CovidData: Can be set to true of false, shows covid cases.

Returns:
    Nothing, creates a plot.
    """


def PercPlot(filenames, country, tone, tone_col, CovidData):
    fig = go.Figure()
    weeks = GetCols(filenames[0], 0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        if fname.find("Guardian") != -1:
            fname = fname[start + 1:end + 1]
            traceName = fname[:fname[i].find(".")]
            source = "GRD"
        else:
            fname = fname[start + 1:end + 1]
            traceName = fname[:fname[i].find(".")]
            source = "Guardian"
        data = GetCols(filenames[i], tone_col)
        newdata = []
        for num in data:
            newdata.append(num * 100)
        fig.add_trace(
            go.Scatter(x=weeks, y=newdata, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))
    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, range=[-.25, 42.15])
    fig.update_yaxes(title_text="% Of Articles With a " + tone + "Tone", title_font_size=18, range=[0, 100],
                     ticksuffix="%")
    fig.update_layout(title_text="<b>" + source + "</b>")
    graph_setup(fig)

    if CovidData == True:
        if country == "US":
            Covid_Data = GetCols('res/CovidData/UScovidAVG.csv', 0)
            high = 250000
        else:
            Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
            high = 50000
        fig.update_layout(yaxis2=dict(
            title="Weekly Avg. COVID-19 Cases in the " + country,
            titlefont=dict(
                size=17
            ),
            range=[0, high],
            anchor="x",
            overlaying="y",
            side="right"
        ))
        fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='COVID-19 Cases', yaxis='y2', fill='tozeroy'))

    saveName = tone + "Ratio.png"
    fig.update_yaxes(gridcolor='black')
    fig.write_image(saveName, width=1200, height=600, scale=1)
    # fig.show()


"""
Plots all the cumulative tone scores of one tone given multiple sections
Args:
    filenames: List of files you want to plot from
    country: Country of the news source you are plotting from
    tone: String literal of the tone you want to plot, ex. "Analytical"
    tone_col: Singular Index associated with what you want to plot
    CovidData: Can be set to true of false, shows covid cases.

Returns:
    Nothing, creates a plot.
    """


def TotalPlot(filenames, country, tone, tone_col, CovidData, source):
    fig = go.Figure()
    big = 0
    weeks = GetCols(filenames[0], 0)
    for i in range(0, len(filenames)):
        fname = filenames[i]
        start = fname.rfind("/")
        end = fname.rfind(".")
        fname = fname[start + 1:end + 1]
        traceName = fname[:fname[i].find(".")]

        data = GetCols(filenames[i], tone_col)
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=traceName, yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))
        if big < max(data):
            big = max(data)
    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, range=[-.25, 42.15])
    fig.update_yaxes(title_text="Weekly Cumulative " + tone + " Tone Scores", title_font_size=18, range=[0, big + 1])

    fig.update_layout(title_text="<b>" + source + "</b>")
    graph_setup(fig)

    if CovidData == True:
        if country == "US":
            Covid_Data = GetCols('res/CovidData/UScovidAVG.csv', 0)
            high = 250000
        else:
            Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
            high = 50000
        fig.update_layout(yaxis2=dict(
            title="Weekly Avg. COVID-19 Cases in the " + country,
            titlefont=dict(
                size=17
            ),
            range=[0, high],
            anchor="x",
            overlaying="y",
            side="right"
        ))
        fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='COVID-19 cases', yaxis='y2', fill='tozeroy'))

    # fig.write_image("fig1.png", width=1200, height=600, scale=1)
    fig.show()


"""
Plots multiple tones from one file.
Args:
    file: Singular file you want to plot
    tones: array of indicies specifying which columns you want to plot
    tone_name: Associated names to the above indicies
    country: Country of the news source you are plotting from
Returns:
    Nothing, creates a plot.
    """


def MultiTonePlot(file, tones, tone_name, country):
    fig = go.Figure()
    weeks = GetCols(file, 0)
    fname = file
    for i in range(0, len(tones)):
        tone = tones[i]
        data = GetCols(file, tone)
        start = fname.rfind("/")
        end = fname.rfind(".")
        fname = fname[start + 1:end + 1]
        sectionName = fname[:fname.find(".")]
        fig.add_trace(
            go.Scatter(x=weeks, y=data, name=tone_name[i], yaxis="y", mode='lines+markers', marker_symbol=symbols[i]))

    fig.update_xaxes(title_text="Weeks", title_font_size=18, tickangle=90, range=[-.25, 42.15])
    fig.update_yaxes(title_text="Weekly Avg. Tone Scores", title_font_size=18, range=[.5, 1], showgrid=True)
    if country == "US":
        Covid_Data = GetCols('res/CovidData/UScovidAVG.csv', 0)
        high = 250000
        source = "Guardian"
    else:
        Covid_Data = GetCols("res/CovidData/UKcovidAVG.csv", 0)
        high = 50000
        source = "GRD"
    fig.update_layout(yaxis2=dict(
        title="Weekly Avg. COVID-19 Cases in the " + country,
        titlefont=dict(
            size=17
        ),
        range=[0, high],
        anchor="x",
        overlaying="y",
        side="right"
    ))
    graph_setup(fig)
    fig.add_trace(go.Scatter(x=weeks, y=Covid_Data, name='COVID-19 Cases', yaxis='y2', fill='tozeroy'))
    fig.update_layout(title_text="<b>" + source + " " + sectionName + "</b>")
    saveName = sectionName + ".png"
    # fig.write_image(saveName, width=1200, height=600, scale=1)
    fig.show()


"""
Get the first data row in a csv file
Args:
    filename: the path of the csv

Returns:
    an int array contains all data in the first row
    """


def get_row(filename):
    t = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        body = next(reader)
        for k in range(0, 7):
            t.append(int(float(body[k])))
    return t


"""
Plot cumulative tone scores comparison between Guardian and Guardian for given desk
Args:
    desk: Desk name in string

Returns:
    Nothing, creates a plot.
    """


def overall_graph_cross_compare(desk):
    source = ['New York Times', 'Guardian']
    nyt = get_row("res/Guardian/Overall/NYT_" + desk + ".csv")
    guardian = get_row("res/Guardian/Overall/Guardian_" + desk + ".csv")
    fig = go.Figure(data=[
        go.Bar(name='Anger', x=source, y=[nyt[0], guardian[0]]),
        go.Bar(name='Sad', x=source, y=[nyt[1], guardian[1]]),
        go.Bar(name='Fear', x=source, y=[nyt[2], guardian[2]]),
        go.Bar(name='Joy', x=source, y=[nyt[3], guardian[3]]),
        go.Bar(name='Analy', x=source, y=[nyt[4], guardian[4]]),
        go.Bar(name='Confi', x=source, y=[nyt[5], guardian[5]]),
        go.Bar(name='Tenta', x=source, y=[nyt[6], guardian[6]])
    ])
    graph_setup(fig)
    fig.update_xaxes(tickfont=dict(size=18))
    fig.update_yaxes(range=[0, 1400])
    fig.update_layout(barmode='group',
                      title_text=desk + " Cumulative Score Comparison" + ", New York Times VS Guardian",
                      yaxis_title="Cumulative Tone Scores")
    fig.show()


"""
Plot cumulative tone scores cross desks for a given source
Args:
    source: Source name in string

Returns:
    Nothing, creates a plot.
    """


def overall_graph_single_source(source):
    desks = ['Business', 'Science', 'Politics', 'Opinion']
    filenames = ['res/' + source + '/Overall/' + source + '_Business.csv',
                 'res/' + source + '/Overall/' + source + '_Science.csv',
                 'res/' + source + '/Overall/' + source + '_Politics.csv',
                 'res/' + source + '/Overall/' + source + '_Opinion.csv']
    t = [[], [], [], [], [], [], []]
    for filename in filenames:
        row = get_row(filename)
        for k in range(0, 7):
            t[k].append(row[k])

    fig = go.Figure(data=[
        go.Bar(name='Anger', x=desks, y=t[0]),
        go.Bar(name='Sad', x=desks, y=t[1]),
        go.Bar(name='Fear', x=desks, y=t[2]),
        go.Bar(name='Joy', x=desks, y=t[3]),
        go.Bar(name='Analy', x=desks, y=t[4]),
        go.Bar(name='Confi', x=desks, y=t[5]),
        go.Bar(name='Tenta', x=desks, y=t[6])
    ])
    graph_setup(fig)
    fig.update_yaxes(range=[0, 1350])
    fig.update_xaxes(tickfont=dict(size=18))
    fig.update_layout(barmode='group',
                      title_text="Cumulative Tone Scores Comparison Between Primary Desks Of " + source,
                      yaxis_title="Cumulative Tone Scores")
    fig.show()


"""
Graph set up for
Args:
    source: Source name in string

Returns:
    Nothing, creates a plot.
    """


def graph_setup(fig):
    fig.update_layout(title_x=.1,
                      yaxis_title_font_size=18,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, width=900, height=520, autosize=True,
                      margin=dict(
                          l=100,
                          r=10,
                          b=100,
                          t=100,
                          pad=5
                      ),
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="right",
                          x=1
                      ))
    fig.update_yaxes(showgrid=True, gridcolor='black')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')


import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator

symbols = []
raw_symbols = SymbolValidator().values
for i in range(0, len(raw_symbols), 12):
    symbols.append(raw_symbols[i])


def set_yaxes_range_avg(fig):
    fig.update_yaxes(range=[.5, 1])


def single_tone_four_desks_subplot(source, col_name, tone_name):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Business", "Opinion", "Science", "Politics"))

    df = pd.read_csv('res/' + source + '/Business.csv')
    df1 = pd.read_csv('res/' + source + '/Opinion.csv')
    df2 = pd.read_csv('res/' + source + '/Science.csv')
    df3 = pd.read_csv('res/' + source + '/Politics.csv')

    fig.add_trace(go.Scatter(x=df['Week'], y=df[col_name], name="Business", mode='lines+markers',
                             marker_symbol=symbols[0]), row=1, col=1)

    fig.add_trace(go.Scatter(x=df1['Week'], y=df1[col_name], name="Opinion", mode='lines+markers',
                             marker_symbol=symbols[1]), row=1, col=2)

    fig.add_trace(go.Scatter(x=df2['Week'], y=df2[col_name], name="Science", mode='lines+markers',
                             marker_symbol=symbols[2]), row=2, col=1)

    fig.add_trace(go.Scatter(x=df3['Week'], y=df3[col_name], name="Politics", mode='lines+markers',
                             marker_symbol=symbols[3]), row=2, col=2)

    fig.update_layout(height=800, width=1500,
                      title={
                          'text': tone_name + " Tone Comparison Between Different Desks in " + source,
                          'y': 0.95,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'
                      })
    set_yaxes_range_avg(fig)
    fig.update_xaxes(title_text="Weeks", title_font_size=18)
    fig.update_yaxes(title_text="Weekly Avg " + tone_name + " Tone Score", title_font_size=18,
                     showgrid=True, gridcolor='black', zeroline=True, zerolinewidth=1, zerolinecolor='black')
    fig.update_layout(yaxis_title_font_size=18,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, autosize=True,
                      margin=dict(
                          pad=10
                      ))

    # fig.write_image("31.eps", width=2000, height=1000, scale=1)
    fig.show()


def cross_source_comparison(desk):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Analytical Tone Comparison", "Anger Tone Comparison", "Tentative Tone Comparison", "Sad Tone Comparison"))

    df = pd.read_csv('res/Guardian/' + desk + '.csv')
    df1 = pd.read_csv('res/Guardian/' + desk + '.csv')

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Analy_avg"], name="Guardian", mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df1['Week'], y=df1["Analy_avg"], name="Guardian", mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))],
        rows=1, cols=1)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Anger_avg"], showlegend=False, mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df1['Week'], y=df1["Anger_avg"], showlegend=False, mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))],
        rows=1, cols=2)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Tenta_avg"], showlegend=False, mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df1['Week'], y=df1["Tenta_avg"], showlegend=False, mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))],
        rows=2, cols=1)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Sad_avg"], showlegend=False, mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df1['Week'], y=df1["Sad_avg"], showlegend=False, mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))],
        rows=2, cols=2)

    fig.update_layout(height=800, width=1500,
                      title={
                          'text': desk + ' Comparison, Guardian VS Guardian',
                          'y': 0.95,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'
                      })
    fig.update_xaxes(title_text="Weeks", title_font_size=18)
    fig.update_yaxes(title_text="Weekly Avg Tone Scores", title_font_size=18, showgrid=True, gridcolor='black',
                     zeroline=True, zerolinewidth=1, zerolinecolor='black')
    set_yaxes_range_avg(fig)
    fig.update_layout(
        yaxis_title_font_size=18,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, autosize=True,
        margin=dict(
            pad=10
        ))

    # fig.write_image("31.eps", width=2000, height=1000, scale=1)
    fig.show()


# single_tone_four_desks_subplot("Guardian", "Sad_avg", "Sad")
# single_tone_four_desks_subplot("Guardian", "Analy_avg", "Analytical")
# single_tone_four_desks_subplot("Guardian", "Tenta_avg", "Tentative")
# single_tone_four_desks_subplot("Guardian", "Anger_avg", "Anger")

def sad(df, tag):
    return go.Scatter(x=df['Week'], y=df["Sad_" + tag], showlegend=False, name="Sad", mode='lines+markers',
                      marker=dict(color='goldenrod', symbol=symbols[3]), line=dict(color='goldenrod'))


def analytical(df, tag):
    return go.Scatter(x=df['Week'], y=df["Analy_" + tag], showlegend=False, name="Analytical", mode='lines+markers',
                      marker=dict(color='red', symbol=symbols[0]), line=dict(color='red'))


def anger(df, tag):
    return go.Scatter(x=df['Week'], y=df["Anger_" + tag], showlegend=False, name="Anger", mode='lines+markers',
                      marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))


def tentative(df, tag):
    return go.Scatter(x=df['Week'], y=df["Tenta_" + tag], showlegend=False, name="Tentative", mode='lines+markers',
                      marker=dict(color='green', symbol=symbols[2]), line=dict(color='green'))


def joy(df, tag):
    return go.Scatter(x=df['Week'], y=df["Joy_" + tag], showlegend=False, name="Joy", mode='lines+markers',
                      marker=dict(color='black', symbol=symbols[4]), line=dict(color='black'))


def fear(df, tag):
    return go.Scatter(x=df['Week'], y=df["Fear_" + tag], showlegend=False, name="Fear", mode='lines+markers',
                      marker=dict(color='magenta', symbol=symbols[5]), line=dict(color='magenta'))


def confi(df, tag):
    return go.Scatter(x=df['Week'], y=df["Confi_" + tag], showlegend=False, name="Confidence", mode='lines+markers',
                      marker=dict(color='pink', symbol=symbols[6]), line=dict(color='pink'))


def all_tone_four_plot(fig, df, df1, df2, df3, tag):
    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Analy_" + tag], name="Analytical", mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red')),
         go.Scatter(x=df['Week'], y=df["Anger_" + tag], name="Anger", mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue')),
         go.Scatter(x=df['Week'], y=df["Tenta_" + tag], name="Tentative", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[2]), line=dict(color='green')),
         go.Scatter(x=df['Week'], y=df["Sad_" + tag], name="Sad", mode='lines+markers',
                    marker=dict(color='goldenrod', symbol=symbols[3]), line=dict(color='goldenrod')),
         go.Scatter(x=df['Week'], y=df["Joy_" + tag], name="Joy", mode='lines+markers',
                    marker=dict(color='black', symbol=symbols[4]), line=dict(color='black')),
         go.Scatter(x=df['Week'], y=df["Fear_" + tag], name="Fear", mode='lines+markers',
                    marker=dict(color='magenta', symbol=symbols[5]), line=dict(color='magenta')),
         go.Scatter(x=df['Week'], y=df["Confi_" + tag], name="Confidence", mode='lines+markers',
                    marker=dict(color='pink', symbol=symbols[6]), line=dict(color='pink'))], rows=1, cols=1)

    fig.add_traces(
        [analytical(df1, tag), anger(df1, tag), tentative(df1, tag), sad(df1, tag), joy(df1, tag), fear(df1, tag),
         confi(df1, tag)],
        rows=1, cols=2)

    fig.add_traces(
        [analytical(df2, tag), anger(df2, tag), tentative(df2, tag), sad(df2, tag), joy(df2, tag), fear(df2, tag),
         confi(df2, tag)],
        rows=2, cols=1)

    fig.add_traces(
        [analytical(df3, tag), anger(df3, tag), tentative(df3, tag), sad(df3, tag), joy(df3, tag), fear(df3, tag),
         confi(df3, tag)],
        rows=2, cols=2)


def confi_tenta(fig, df, df1, df2, df3, tag):
    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Confi_" + tag], name="Confidence", mode='lines+markers',
                    marker=dict(color='pink', symbol=symbols[0]), line=dict(color='pink')),
         go.Scatter(x=df['Week'], y=df["Tenta_" + tag], name="Tentative", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[2]), line=dict(color='green'))], rows=1, cols=1)

    fig.add_traces(
        [confi(df1, tag), tentative(df1, tag)], rows=1, cols=2)

    fig.add_traces(
        [confi(df2, tag), tentative(df2, tag)], rows=2, cols=1)

    fig.add_traces(
        [confi(df3, tag), tentative(df3, tag)], rows=2, cols=2)


def fear_sad_anger(fig, df, df1, df2, df3, tag):
    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Anger_" + tag], name="Anger", mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue')),
         go.Scatter(x=df['Week'], y=df["Sad_" + tag], name="Sad", mode='lines+markers',
                    marker=dict(color='goldenrod', symbol=symbols[3]), line=dict(color='goldenrod')),
         go.Scatter(x=df['Week'], y=df["Fear_" + tag], name="Fear", mode='lines+markers',
                    marker=dict(color='magenta', symbol=symbols[5]), line=dict(color='magenta'))], rows=1, cols=1)

    fig.add_traces(
        [anger(df1, tag), sad(df1, tag), fear(df1, tag)], rows=1, cols=2)

    fig.add_traces(
        [anger(df2, tag), sad(df2, tag), fear(df2, tag)], rows=2, cols=1)

    fig.add_traces(
        [anger(df3, tag), sad(df3, tag), fear(df3, tag)], rows=2, cols=2)


def subplot_config(fig, t, tag):
    fig.update_layout(height=800, width=1500,
                      title={
                          'text': t,
                          'y': 0.95,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'

                      })
    name = "Average"
    if tag == "total":
        name = "Total"
    fig.update_yaxes(title_text="Weekly " + name + " Tone Scores", title_font_size=18, showgrid=True, gridcolor='black',
                     zeroline=True, zerolinewidth=1, zerolinecolor='black')
    fig.update_layout(
        yaxis_title_font_size=18,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, autosize=True,
        margin=dict(
            pad=10
        ))


def confi_vs_tenta(mode):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "COVID-19 Guardian", "COVID-19 GRD", "H1N1-09 Guardian", "H1N1-09 GRD"))

    df = pd.read_csv('NYT_overall.csv')
    df1 = pd.read_csv('Guardian_overall.csv')
    df2 = pd.read_csv('res/H1N1/NYT.csv')
    df3 = pd.read_csv('res/H1N1/Guardian.csv')
    tag = "avg"
    if mode == "Overall":
        tag = "total"

    confi_tenta(fig, df, df1, df2, df3, tag)
    subplot_config(fig, mode + ' Confidence and Tentative Score Comparison, Covid-19 vs H1N1-09', tag)
    if tag == 'avg':
        set_yaxes_range_avg(fig)
    fig.show()


def fear_vs_sad_vs_anger(mode):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "COVID-19 Guardian", "COVID-19 GRD", "H1N1-09 Guardian", "H1N1-09 GRD"))

    df = pd.read_csv('NYT_overall.csv')
    df1 = pd.read_csv('Guardian_overall.csv')
    df2 = pd.read_csv('res/H1N1/NYT.csv')
    df3 = pd.read_csv('res/H1N1/Guardian.csv')
    tag = "avg"
    if mode == "Overall":
        tag = "total"

    fear_sad_anger(fig, df, df1, df2, df3, tag)
    subplot_config(fig, mode + ' Fear, Sad, and Anger Score Comparison, Covid-19 vs H1N1-09', tag)
    if tag == 'avg':
        set_yaxes_range_avg(fig)
    fig.show()


def tentative_fear_sad_anger(fig, df, df1, df2, df3, tag):
    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Anger_" + tag], name="Anger", mode='lines+markers',
                    marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue')),
         go.Scatter(x=df['Week'], y=df["Sad_" + tag], name="Sad", mode='lines+markers',
                    marker=dict(color='goldenrod', symbol=symbols[3]), line=dict(color='goldenrod')),
         go.Scatter(x=df['Week'], y=df["Fear_" + tag], name="Fear", mode='lines+markers',
                    marker=dict(color='magenta', symbol=symbols[5]), line=dict(color='magenta')),
         go.Scatter(x=df['Week'], y=df['Tenta_' + tag], name="Tentative", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[2], line=dict(color='green')))], rows=1, cols=1)

    fig.add_traces(
        [anger(df1, tag), sad(df1, tag), fear(df1, tag), tentative(df1, tag)], rows=1, cols=2)

    fig.add_traces(
        [anger(df2, tag), sad(df2, tag), fear(df2, tag), tentative(df2, tag)], rows=2, cols=1)

    fig.add_traces(
        [anger(df3, tag), sad(df3, tag), fear(df3, tag), tentative(df3, tag)], rows=2, cols=2)


def tentative_vs_fear_vs_sad_vs_anger(mode):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "COVID-19 Guardian", "COVID-19 GRD", "H1N1-09 Guardian", "H1N1-09 GRD"))

    df = pd.read_csv('NYT_overall.csv')
    df1 = pd.read_csv('Guardian_overall.csv')
    df2 = pd.read_csv('res/H1N1/NYT.csv')
    df3 = pd.read_csv('res/H1N1/Guardian.csv')
    tag = "avg"
    if mode == "Overall":
        tag = "total"

    tentative_fear_sad_anger(fig, df, df1, df2, df3, tag)
    subplot_config(fig, mode + ' Fear, Sad, Anger, and Tentative Score Comparison, Covid-19 vs H1N1-09', tag)
    if tag == 'avg':
        set_yaxes_range_avg(fig)
    fig.show()


def overall_comparison(mode):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "COVID-19 Guardian", "COVID-19 GRD", "H1N1-09 Guardian", "H1N1-09 GRD"))

    df = pd.read_csv('NYT_overall.csv')
    df1 = pd.read_csv('Guardian_overall.csv')
    df2 = pd.read_csv('res/H1N1/NYT.csv')
    df3 = pd.read_csv('res/H1N1/Guardian.csv')
    tag = "avg"
    if mode == "Overall":
        tag = "total"

    all_tone_four_plot(fig, df, df1, df2, df3, tag)
    subplot_config(fig, mode + ' Tone Score Comparison, Covid-19 vs H1N1-09', tag)
    if tag == 'avg':
        set_yaxes_range_avg(fig)
    fig.show()


# tentative_vs_fear_vs_sad_vs_anger("Average")
#
#
# overall_comparison("Overall")
# confi_vs_tenta("Average")
# confi_vs_tenta("Overall")
# fear_vs_sad_vs_anger("Average")
# fear_vs_sad_vs_anger("Overall")

tentative_vs_fear_vs_sad_vs_anger("Overall")
tentative_vs_fear_vs_sad_vs_anger("Average")


def GetCols(filename, col):
    df = pd.read_csv(filename, usecols=[col])
    list = df.keys()
    ToneScores = df[list[0]].tolist()
    return ToneScores


def main():
    overall_graph_single_source("Guardian")
    overall_graph_single_source("Guardian")


main()
