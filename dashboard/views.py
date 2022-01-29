from django.shortcuts import render
import pandas as pd
import plotly
import plotly.express as px
from plotly.offline import plot
from urllib.request import urlopen
import json


# Create your views here.
def index(request):
    # JSON file to draw county choropleth
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    # CSV to pull population per county for Choropleth
    df = pd.read_csv("dashboard/static/csv/population.csv",
                     # on_bad_lines='skip',
                     # names=['county_name', 'fips', 'tot_pop', 'uep'],
                     # sep='delimiter',
                     # engine='python',
                     dtype={"fips": str})
    # Plotly function to render Choropleth
    usa = px.choropleth(df,
                        geojson=counties,
                        locations='fips',
                        color='uep',
                        color_continuous_scale="Portland",
                        range_color=(0, 10),
                        hover_name='county_name',
                        hover_data=['fips', 'uep', 'tot_pop'],
                        labels={"fips": "FIPS", 'uep': 'Unemployment Rate', 'tot_pop': 'Population'},
                        template='presentation',

                        )
    usa.update_layout(
        coloraxis_colorbar=dict(
            thicknessmode="pixels",
            thickness=30,
            lenmode="pixels",
            len=600,
            yanchor="top",
            y=0.9,
            xanchor='left',
            x=1,
            ticks="inside",
            ticksuffix=" %",
            dtick=2
        ),
        title={
            'text': "United States Unemployment per County ",
            'y': 0.05,
            'x': 0.45,
            'font_size': 28,
            'xanchor': 'center',
            'yanchor': 'top'},
        # separators=',',
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        margin=dict(l=20, r=20, t=20, b=30),
        autosize=False,
        width=1860,
        height=850
    )
    usa.update_geos(
        scope='usa',
        visible=False,
    )
    # Getting HTML needed to render the plot.
    plot_div = plot(usa,
                    output_type='div',
                    include_plotlyjs=False)

    return render(request, 'index.html', context={'plot_div': plot_div})