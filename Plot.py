import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator

symbols = []
raw_symbols = SymbolValidator().values
for i in range(0, len(raw_symbols), 12):
    symbols.append(raw_symbols[i])

"""
Create sad trace
Args:
    df: DataFrame with the data and labels from the file data.
    tag: avg or total

Returns:
    Return sad trace
    """


def sad(df, tag):
    return go.Scatter(x=df['Week'], y=df["Sad_" + tag], showlegend=False, name="Sad", mode='lines+markers',
                      marker=dict(color='goldenrod', symbol=symbols[3]), line=dict(color='goldenrod'))


"""
Create analytical trace
Args:
    df: DataFrame with the data and labels from the file data.
    tag: avg or total

Returns:
    Return analytical trace
    """


def analytical(df, tag):
    return go.Scatter(x=df['Week'], y=df["Analy_" + tag], showlegend=False, name="Analytical", mode='lines+markers',
                      marker=dict(color='red', symbol=symbols[0]), line=dict(color='red'))


"""
Create anger trace
Args:
    df: DataFrame with the data and labels from the file data.
    tag: avg or total

Returns:
    Return anger trace
    """


def anger(df, tag):
    return go.Scatter(x=df['Week'], y=df["Anger_" + tag], showlegend=False, name="Anger", mode='lines+markers',
                      marker=dict(color='blue', symbol=symbols[1]), line=dict(color='blue'))


"""
Create tentative trace
Args:
    df: DataFrame with the data and labels from the file data.
    tag: avg or total

Returns:
    Return tentative trace
    """


def tentative(df, tag):
    return go.Scatter(x=df['Week'], y=df["Tenta_" + tag], showlegend=False, name="Tentative", mode='lines+markers',
                      marker=dict(color='green', symbol=symbols[2]), line=dict(color='green'))


"""
Create joy trace
Args:
    df: DataFrame with the data and labels from the file data.
    tag: avg or total

Returns:
    Return joy trace
    """


def joy(df, tag):
    return go.Scatter(x=df['Week'], y=df["Joy_" + tag], showlegend=False, name="Joy", mode='lines+markers',
                      marker=dict(color='black', symbol=symbols[4]), line=dict(color='black'))


"""
Create fear trace
Args:
    df: DataFrame with the data and labels from the file data.
    tag: avg or total

Returns:
    Return fear trace
    """


def fear(df, tag):
    return go.Scatter(x=df['Week'], y=df["Fear_" + tag], showlegend=False, name="Fear", mode='lines+markers',
                      marker=dict(color='magenta', symbol=symbols[5]), line=dict(color='magenta'))


"""
Create confidence trace
Args:
    df: DataFrame with the data and labels from the file data.
    tag: avg or total

Returns:
    Return confidence trace
    """


def confi(df, tag):
    return go.Scatter(x=df['Week'], y=df["Confi_" + tag], showlegend=False, name="Confidence", mode='lines+markers',
                      marker=dict(color='pink', symbol=symbols[6]), line=dict(color='pink'))


"""
Add traces for fear, sad, and anger plot
Args:
    fig: the plot object
    df: data frame 1
    df1: data frame 2
    df2: data frame 3
    df3: data frame 4
    tag: avg or total

Returns:
    Config the plot object
    """


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


"""
Plots Fear vs sad vs anger
Args:
    mode: average or overall, in string form

Returns:
    Nothing, creates a plot.
    """


def fear_vs_sad_vs_anger(mode):
    fig = make_subplots(
        vertical_spacing=0.15,
        horizontal_spacing=0.10,
        rows=2, cols=2,
        subplot_titles=(
            "COVID-19 Guardian", "COVID-19 GRD", "H1N1-09 Guardian", "H1N1-09 GRD"),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": True}, {"secondary_y": True}]])

    df = pd.read_csv('NYT_overall.csv')
    df1 = pd.read_csv('Guardian_overall.csv')
    df2 = pd.read_csv('res/H1N1/NYT.csv')
    df3 = pd.read_csv('res/H1N1/Guardian.csv')
    tag = "avg"
    if mode == "Overall":
        tag = "total"
    if mode =="Percentage":
        tag="ratio"

    fear_sad_anger(fig, df, df1, df2, df3, tag)
    add_second_yaxis(fig, df, df2, pd.read_csv('res/CovidData/UScovidAVG.csv'),
                     pd.read_csv('res/CovidData/UKcovidAVG.csv'), pd.read_csv('res/H1N1Data/us.csv'),
                     pd.read_csv('res/H1N1Data/uk.csv'))
    subplot_config2(fig, 'Weekly ' + mode + ' Fear-Sad-Anger', tag)
    fig.show()


"""
Add traces for confidence, tentative, and analytical plot
Args:
    fig: the plot object
    df: data frame 1
    df1: data frame 2
    df2: data frame 3
    df3: data frame 4
    tag: avg or total

Returns:
    Config the plot object
    """


def confi_tenta_analy(fig, df, df1, df2, df3, tag):
    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Confi_" + tag], name="Confidence", mode='lines+markers',
                    marker=dict(color='pink', symbol=symbols[0]), line=dict(color='pink')),
         go.Scatter(x=df['Week'], y=df["Tenta_" + tag], name="Tentative", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[2]), line=dict(color='green')),
         go.Scatter(x=df['Week'], y=df["Analy_" + tag], name="Analytical", mode='lines+markers',
                    marker=dict(color='red', symbol=symbols[0]), line=dict(color='red'))], rows=1, cols=1)

    fig.add_traces(
        [confi(df1, tag), tentative(df1, tag), analytical(df1, tag)], rows=1, cols=2)

    fig.add_traces(
        [confi(df2, tag), tentative(df2, tag), analytical(df2, tag)], rows=2, cols=1)

    fig.add_traces(
        [confi(df3, tag), tentative(df3, tag), analytical(df3, tag)], rows=2, cols=2)


"""
Plots confidence vs tentative vs analytical
Args:
    mode: average or overall, in string form

Returns:
    Nothing, creates a plot.
    """


def confi_vs_tenta_vs_analy(mode):
    fig = make_subplots(
        vertical_spacing=0.15,
        horizontal_spacing=0.10,
        rows=2, cols=2,
        subplot_titles=(
            "COVID-19 Guardian", "COVID-19 GRD", "H1N1-09 Guardian", "H1N1-09 GRD"),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": True}, {"secondary_y": True}]])

    df = pd.read_csv('NYT_overall.csv')
    df1 = pd.read_csv('Guardian_overall.csv')
    df2 = pd.read_csv('res/H1N1/NYT.csv')
    df3 = pd.read_csv('res/H1N1/Guardian.csv')
    tag = "avg"
    if mode == "Overall":
        tag = "total"
    if mode=="Percentage":
        tag="ratio"

    confi_tenta_analy(fig, df, df1, df2, df3, tag)
    add_second_yaxis(fig, df, df2, pd.read_csv('res/CovidData/UScovidAVG.csv'),
                     pd.read_csv('res/CovidData/UKcovidAVG.csv'), pd.read_csv('res/H1N1Data/us.csv'),
                     pd.read_csv('res/H1N1Data/uk.csv'))
    subplot_config2(fig, 'Weekly ' + mode + ' Confidence-Tentative-Analytical', tag)
    fig.show()


"""
Add traces for plot contains all seven tones
Args:
    fig: the plot object
    df: data frame 1
    df1: data frame 2
    df2: data frame 3
    df3: data frame 4
    tag: avg or total

Returns:
    Config the plot object
    """


def all_tone_four_plot2US(fig, df, df1, df2, df3, tag):
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


"""
Add secondary yaxis traces for plot
Args:
    fig: the plot object
    covid: covid cases data frame
    h1n1: h1n1 cases data frame
    df: data frame 1
    df1: data frame 2
    df2: data frame 3
    df3: data frame 4
    tag: avg or total

Returns:
    Config the plot object
    """


def add_second_yaxis(fig, covid, h1n1, df, df1, df2, df3):
    fig.add_trace(go.Scatter(x=covid['Week'], y=df['cases'], name="US Covid Cases", fill='tozeroy'), row=1,
                  col=1, secondary_y=True)
    fig.add_trace(go.Scatter(x=covid['Week'], y=df1['cases'], name="UK Covid Cases", fill='tozeroy'), row=1,
                  col=2, secondary_y=True)
    fig.add_trace(go.Scatter(x=h1n1['Week'], y=df2['cases'], name="US H1N1 Cases", fill='tozeroy'), row=2,
                  col=1, secondary_y=True)
    fig.add_trace(go.Scatter(x=h1n1['Week'], y=df3['cases'], name="UK H1N1 Cases", fill='tozeroy'), row=2,
                  col=2, secondary_y=True)


"""
Config common subplot elements
Args:
    fig: the plot object
    t: plot title
    tag: avg or total

Returns:
    Nothing, config the plot object
    """


def subplot_config2(fig, t, tag):
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
    fig.update_yaxes(title_font_size=18, showgrid=True, gridcolor='black',
                     zeroline=True, zerolinewidth=1, zerolinecolor='black')
    fig.update_layout(
        width=1200,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, autosize=True,
        margin=dict(
            pad=10
        ))
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    fig.update_layout(legend_borderwidth=6)
    fig.update_layout(legend_bordercolor='#fff')
    fig.update_layout(title_xanchor="center")
    fig.update_layout(title_pad_b=100)

    fig.update_layout(
        yaxis2=dict(
            range=[0, 250000],
        ),
        yaxis4=dict(
            range=[0, 50000],
        ),
        yaxis6=dict(
            range=[0, 10000000],
        ),
        yaxis8=dict(
            range=[0, 100000],
        )
    )

    if tag == "avg":
        fig.update_layout(
            yaxis=dict(
                range=[0.5, 1]
            ),
            yaxis3=dict(
                range=[0.5, 1],
            ),
            yaxis5=dict(
                range=[0.5, 1]
            ),
            yaxis7=dict(
                range=[0.5, 1]
            )
        )
    elif tag=="ratio":
        fig.update_layout(
            yaxis=dict(
                range=[0, 100]
            ),
            yaxis3=dict(
                range=[0, 100],
            ),
            yaxis5=dict(
                range=[0, 100]
            ),
            yaxis7=dict(
                range=[0, 100]
            )
        )

    else:
        fig.update_layout(
            yaxis=dict(
                range=[0, 500]
            ),
            yaxis3=dict(
                range=[0, 250],
            ),
            yaxis5=dict(
                range=[0, 10]
            ),
            yaxis7=dict(
                range=[0.5, 100]
            )
        )


"""
Plots Seven tones
Args:
    mode: average or overall, in string form

Returns:
    Nothing, creates a plot.
    """


def overall_comparison2(mode):
    fig = make_subplots(
        vertical_spacing=0.15,
        horizontal_spacing=0.10,
        rows=2, cols=2,
        subplot_titles=(
            "COVID-19 Guardian", "COVID-19 GRD", "H1N1-09 Guardian", "H1N1-09 GRD"),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": True}, {"secondary_y": True}]])

    df = pd.read_csv('NYT_overall.csv')
    df1 = pd.read_csv('Guardian_overall.csv')
    df2 = pd.read_csv('res/H1N1/NYT.csv')
    df3 = pd.read_csv('res/H1N1/Guardian.csv')
    tag = "avg"
    if mode == "Overall":
        tag = "total"
    if mode=="Percentage":
        tag="ratio"
    all_tone_four_plot2US(fig, df, df1, df2, df3, tag)
    add_second_yaxis(fig, df, df2, pd.read_csv('res/CovidData/UScovidAVG.csv'),
                     pd.read_csv('res/CovidData/UKcovidAVG.csv'), pd.read_csv('res/H1N1Data/us.csv'),
                     pd.read_csv('res/H1N1Data/uk.csv'))
    subplot_config2(fig, mode + ' Tone Score Comparison, Covid-19 vs H1N1-09', tag)

    fig.show()






def confi_tenta2(fig, df, df1, df2, df3, tag):
    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Fear_" + tag], name="Sports", mode='lines+markers',
                    marker=dict(color='pink', symbol=symbols[0]), line=dict(color='pink'),showlegend=False),
         go.Scatter(x=df1['Week'], y=df1["Fear_" + tag], name="Business", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[2]), line=dict(color='green'),showlegend=False),
        go.Scatter(x=df2['Week'], y=df2["Fear_" + tag], name="Politics", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[4]), line=dict(color='blue'),showlegend=False),
        go.Scatter(x=df3['Week'], y=df3["Fear_" + tag], name="Opinion", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[6]), line=dict(color='red'),showlegend=False)], rows=1, cols=1)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Sad_" + tag],  mode='lines+markers',
                    marker=dict(color='pink', symbol=symbols[0]), line=dict(color='pink'),showlegend=False),
         go.Scatter(x=df1['Week'], y=df1["Sad_" + tag],  mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[2]), line=dict(color='green'),showlegend=False),
        go.Scatter(x=df2['Week'], y=df2["Sad_" + tag],  mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[4]), line=dict(color='blue'),showlegend=False),
        go.Scatter(x=df3['Week'], y=df3["Sad_" + tag],  mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[6]), line=dict(color='red'),showlegend=False)], rows=1, cols=2)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Tenta_" + tag], name="Sports", mode='lines+markers',
                    marker=dict(color='pink', symbol=symbols[0]), line=dict(color='pink'),showlegend=False),
         go.Scatter(x=df1['Week'], y=df1["Tenta_" + tag], name="Business", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[2]), line=dict(color='green'),showlegend=False),
        go.Scatter(x=df2['Week'], y=df2["Tenta_" + tag], name="Politics", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[4]), line=dict(color='blue'),showlegend=False),
        go.Scatter(x=df3['Week'], y=df3["Tenta_" + tag], name="Opinion", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[6]), line=dict(color='red'),showlegend=False)], rows=2, cols=1)

    fig.add_traces(
        [go.Scatter(x=df['Week'], y=df["Analy_" + tag], name="Sports", mode='lines+markers',
                    marker=dict(color='pink', symbol=symbols[0]), line=dict(color='pink')),
         go.Scatter(x=df1['Week'], y=df1["Analy_" + tag], name="Business", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[2]), line=dict(color='green')),
        go.Scatter(x=df2['Week'], y=df2["Analy_" + tag], name="Politics", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[4]), line=dict(color='blue')),
        go.Scatter(x=df3['Week'], y=df3["Analy_" + tag], name="Opinion", mode='lines+markers',
                    marker=dict(color='green', symbol=symbols[6]), line=dict(color='red'))], rows=2, cols=2)






def desk_add_second_yaxis(fig, covid, h1n1, df, df1, df2, df3):
    fig.add_trace(go.Scatter(x=covid['Week'], y=df['cases'], name="US Covid Cases", fill='tozeroy'), row=1,
                  col=1, secondary_y=True)

    fig.add_trace(go.Scatter(x=covid['Week'], y=df['cases'], name="US Covid Cases", fill='tozeroy',showlegend=False), row=1,
                  col=2, secondary_y=True)

    fig.add_trace(go.Scatter(x=covid['Week'], y=df['cases'], name="US Covid Cases", fill='tozeroy',showlegend=False), row=2,
                  col=1, secondary_y=True)

    fig.add_trace(go.Scatter(x=covid['Week'], y=df['cases'], name="US Covid Cases", fill='tozeroy',showlegend=False), row=2,
                  col=2, secondary_y=True)



def bydesk(mode):

    fig = make_subplots(
        vertical_spacing=0.15,
        horizontal_spacing=0.10,
        rows=2, cols=2,
        subplot_titles=(
            "Fear", "Sad", "Tentative", "Analytical"),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": True}, {"secondary_y": True}]])



    df = pd.read_csv('/Users/nathaniel/Desktop/Tone-Research/res/NYT/Sports.csv')
    df1 = pd.read_csv('/Users/nathaniel/Desktop/Tone-Research/res/NYT/Business.csv')
    df2 = pd.read_csv('/Users/nathaniel/Desktop/Tone-Research/res/NYT/Politics.csv')
    df3 = pd.read_csv('/Users/nathaniel/Desktop/Tone-Research/res/NYT/Opinion.csv')
    tag="avg"
    if mode=="Percentage":
        tag="ratio"
    elif mode=="Overall":
        tag="total"



    confi_tenta2(fig, df, df1, df2, df3, tag)
    subplot_config3(fig, 'NYT-'+mode + ' Tone Score Comparison by Desk', tag)
    desk_add_second_yaxis(fig, df, df2, pd.read_csv('res/CovidData/UScovidAVG.csv'),
                     pd.read_csv('res/CovidData/UScovidAVG.csv'), pd.read_csv('res/CovidData/UScovidAVG.csv'),
                     pd.read_csv('res/CovidData/UScovidAVG.csv'))




    fig.update_layout(legend_borderwidth=6)
    fig.update_layout(legend_bordercolor='#fff')
    fig.update_layout(title_xanchor="center")
    fig.update_layout(title_pad_b=100)
    fig.show()



def subplot_config3(fig, t, tag):
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
    if tag=="ratio":
        name="Percentage"
    fig.update_yaxes(title_font_size=18, showgrid=True, gridcolor='black',
                     zeroline=True, zerolinewidth=1, zerolinecolor='black')
    fig.update_layout(
        width=1200,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', title_font_size=20, autosize=True,
        margin=dict(
            pad=10
        ))
    # fig.update_layout(legend=dict(
    #     orientation="v",
    #     yanchor="bottom",
    #     y=1.02,
    #     xanchor="right",
    #
    #     x=1
    # ))
    fig.update_layout(legend=dict(

        y=1.02,
        x=1
    ))

    fig.update_layout(legend_borderwidth=6)
    fig.update_layout(legend_bordercolor='#fff')
    fig.update_layout(title_xanchor="center")

    fig.update_layout(title_pad_b=100)

    fig.update_layout(
        yaxis2=dict(
            range=[0, 250000],
        ),
        yaxis4=dict(
            range=[0, 250000],
        ),
        yaxis6=dict(
            range=[0, 250000],
        ),
        yaxis8=dict(
            range=[0, 250000],
        )
    )

    if tag == "avg":
        fig.update_layout(
            yaxis=dict(
                range=[0.5, 1]
            ),
            yaxis3=dict(
                range=[0.5, 1],
            ),
            yaxis5=dict(
                range=[0.5, 1]
            ),
            yaxis7=dict(
                range=[0.5, 1]
            )
        )
    elif tag=="ratio":
        fig.update_layout(
            yaxis=dict(
                range=[0, 100]
            ),
            yaxis3=dict(
                range=[0, 100],
            ),
            yaxis5=dict(
                range=[0, 100]
            ),
            yaxis7=dict(
                range=[0, 100]
            )
        )
    else:
        fig.update_layout(
            yaxis=dict(
                range=[0, 25]
            ),
            yaxis3=dict(
                range=[0.5, 75],
            ),
            yaxis5=dict(
                range=[0, 55]
            ),
            yaxis7=dict(
                range=[0, 50]
            )
        )


def overall_comparison3(mode):
    fig = make_subplots(
        vertical_spacing=0.15,
        horizontal_spacing=0.10,
        rows=2, cols=2,
        subplot_titles=(
            "COVID-19 NYT", "COVID-19 GRD", "H1N1-09 NYT", "H1N1-09 GRD"),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": True}, {"secondary_y": True}]])

    df = pd.read_csv('NYT_overall.csv')
    df1 = pd.read_csv('Guardian_overall.csv')
    df2 = pd.read_csv('res/H1N1/NYT.csv')
    df3 = pd.read_csv('res/H1N1/Guardian.csv')
    tag = "avg"
    if mode == "Overall":
        tag = "total"
    if mode=="Percentage":
        tag="ratio"
    some_tone_four_plot2US(fig, df, df1, df2, df3, tag)
    add_second_yaxis(fig, df, df2, pd.read_csv('res/CovidData/UScovidAVG.csv'),
                     pd.read_csv('res/CovidData/UKcovidAVG.csv'), pd.read_csv('res/H1N1Data/us.csv'),
                     pd.read_csv('res/H1N1Data/uk.csv'))
    subplot_config2(fig, mode + ' Tone Score Comparison, Covid-19 vs H1N1-09', tag)

    fig.show()



# tentative_vs_fear_vs_sad_vs_anger("Average")
#
#
overall_comparison2("Average")
overall_comparison2("Overall")
# confi_vs_tenta_vs_analy("Average")
# confi_vs_tenta_vs_analy("Overall")
# fear_vs_sad_vs_anger("Average")
# fear_vs_sad_vs_anger("Overall")
