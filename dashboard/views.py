# Required Packages
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from plotly.offline import plot
from plotly.subplots import make_subplots

from . import models
from .forms import fipsNumber

DATA_PATH = 'dashboard/static/csv/population.csv'
DATA_ARGS_PATH = 'dashboard/static/json/DATA_ARGS.json'

CHOROPLETH_ARGS_PATH = 'dashboard/static/json/CHOROPLETH_ARGS.json'
CHOROPLETH_LAYOUT_ARGS_PATH = 'dashboard/static/json/CHOROPLETH_LAYOUT_ARGS.json'


# Create your views here.
@csrf_exempt
def index(request):
    def get_df(path, args={}):
        return pd.read_csv(path, **args)

    def get_choropleth(df, args):
        return px.choropleth(df, **args)

    def update_choropleth_layout(choropleth, layout_args):
        choropleth.update_layout(**layout_args)

    DATA_ARGS = json.load(open(DATA_ARGS_PATH))
    DF = get_df(DATA_PATH, DATA_ARGS)

    CHOROPLETH_ARGS = json.load(open(CHOROPLETH_ARGS_PATH))
    CHOROPLETH_LAYOUT_ARGS = json.load(open(CHOROPLETH_LAYOUT_ARGS_PATH))

    usa = get_choropleth(DF, CHOROPLETH_ARGS)
    update_choropleth_layout(usa, CHOROPLETH_LAYOUT_ARGS)

    # Getting HTML needed to render the plot.
    plot_div = plot(usa,
                    output_type='div',
                    include_plotlyjs=False)

    getFips = fipsNumber()
    return render(request, 'index.html', context={'plot_div': plot_div, 'getFips': getFips})


@csrf_exempt
def charts(request):
    if request.method == 'POST':
        FIPS = request.POST['fips']
        year = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
        snap_shot = models.snapShot.objects.values().filter(fips=FIPS)
        time_series = models.time_table.objects.all().values().filter(fips=FIPS)

        neighbors = models.neighbors.objects.values().filter(fips=FIPS)
        neighborsFips = []
        for x in neighbors:
            neighborsFips.append(x['fipsneighbors'])
        nextDoor = pd.DataFrame(neighborsFips)
        print(nextDoor)

        countyData = []
        for time in time_series:
            countyData.append(time)
        county = pd.DataFrame(countyData)

        # print(county)
        # print(snap_shot[0]['year'])
        # print(snap_shot[0])
        # print(type(FIPS))
        # print('Fips: ', FIPS)
        # print(fip)
        template = 'none'
        color = 'whitesmoke'
        fontColor = '#221F1F'
        hoverBgColor = '#FFFFFF'

        fakeNum = [2, 5, 8, 3, 6, 9, 1, 4, 7]
        name = snap_shot[0]['county']
        state = snap_shot[0]['state']
        # # Render Plotly chart 1
        pop_line = make_subplots()
        pop_line.add_trace(
            go.Scatter(x=county['year'],
                       y=county['tot_pop'],
                       mode="markers+lines",
                       name="County",
                       hovertemplate=None,
                       line=dict(color='firebrick', width=2)
                       ))
        pop_line.update_layout(
            template=template,
            margin={"r": 5, "t": 20, "l": 60, "b": 30},
            showlegend=False,
            # separators=',',
            title={
                'text': "Population",
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor=hoverBgColor,
                font_size=14,
            ),
            yaxis_tickformat=',',
            font=dict(
                family="Cardo",
                size=14,
                color=fontColor
            ),
            paper_bgcolor=color,
            plot_bgcolor=color
        )
        # pop_line.update_xaxes( zeroline=True)
        pop_line.update_yaxes(tickangle=35, showgrid=True, gridcolor='#6b6b6b')
        # //////////////////////////////// END Chart 1 (population) ///////////////////////////////////////////////////

        # render plotly chart 2
        headerColor = 'grey'
        rowEvenColor = 'lightgrey'
        rowOddColor = 'white'
        table = go.Figure(data=[go.Table(
            header=dict(
                values=['Snap Shot:', name + ', ' + state],
                line_color='darkslategray',
                fill_color=headerColor,
                font=dict(
                    color=fontColor,
                    size=26,
                ),
                align=['left', 'center'],
                height=35
            ),
            cells=dict(values=[
                [
                    ['Fips'],
                    ['Year'],
                    ['Total Population'],
                    ['Medium Household Income'],
                    ['Unemployment Rate'],
                    ['Number of Employed People'],
                    ['Number of Households with Broadband'],
                    ['Number of Households without Internet'],
                    ['Total Bank Branches'],
                    ['Banks with In-State Headquarters'],
                    ['Total Deposits'],
                ],
                [
                    [snap_shot[0]['fips']],
                    [snap_shot[0]['year']],
                    [snap_shot[0]['tot_pop']],
                    ['$' + str(snap_shot[0]['med_hh_inc'])],
                    [str(snap_shot[0]['unemployment_pct']) + '%'],
                    [snap_shot[0]['emp']],
                    [snap_shot[0]['tot_hh_brdbnd_18']],
                    [snap_shot[0]['tot_hh_no_int_18']],
                    [snap_shot[0]['branches']],
                    [snap_shot[0]['in_st_hq']],
                    [snap_shot[0]['depsumbr']],
                ]
            ],
                line_color='darkslategray',
                fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor] * 12],
                align=['left', 'center'],
                font=dict(
                    color=fontColor,
                    size=24,
                    family="Cardo",
                ),
                height=35

            ))
        ])
        table.update_layout(
            autosize=True,
            separators=',',
            template=template,
            margin={"r": 5, "t": 0, "l": 0, "b": 0},
            paper_bgcolor=color,
            plot_bgcolor=color
        )
        # ///////////////////////////////////// End of chart 2 (table) //////////////////////////////////////////////

        # render plotly chart 3
        ee_stack = go.Figure(data=[
            go.Bar(name='Entry',
                   x=county['year'],
                   y=county['estabs_entry'],
                   marker_color='firebrick'),
            go.Bar(name='Exit',
                   x=county['year'],
                   y=county['estabs_exit'],
                   marker_color='royalblue'),
            go.Bar(name='Total',
                   x=county['year'],
                   y=county['estabs'],
                   marker_color='orange'),
        ])
        ee_stack.update_layout(barmode='group',
                               showlegend=False,
                               template=template,
                               autosize=True,
                               # separators=',',
                               title={
                                   'text': "Birth and Deaths of Establishments",
                                   'y': 0.98,
                                   'x': 0.5,
                                   'xanchor': 'center',
                                   'yanchor': 'top'},
                               #                    yaxis=dict(
                               #     title='# of Establishments',
                               # ),
                               # xaxis=dict(
                               #     title='Year',
                               # ),
                               yaxis_tickformat=',',
                               hovermode="x unified",
                               hoverlabel=dict(
                                   bgcolor=hoverBgColor,
                                   font_size=14,
                               ),
                               font=dict(
                                   family="Cardo",
                                   size=14,
                                   color=fontColor
                               ),
                               margin={"r": 5, "t": 20, "l": 80, "b": 30},
                               paper_bgcolor=color,
                               plot_bgcolor=color
                               ),
        # ee_stack.update_xaxes(showgrid=True, zeroline=True)
        ee_stack.update_yaxes(title_text="# of Establishments", tickangle=0, showgrid=True, gridcolor='#6b6b6b')
        # ////////////////// End of chart 3 (birth and deaths of establishments)
        # /////////////////////////////////////////

        #  render plotly chart 4
        bank_stack = go.Figure(data=[
            go.Bar(name='Small Loans',
                   x=county['year'],
                   y=county['sm_ln_amt'],
                   marker_color='firebrick'),
            go.Bar(name='Medium Loans',
                   x=county['year'],
                   y=county['med_ln_amt'],
                   marker_color='royalblue'),
            go.Bar(name='Large Loans',
                   x=county['year'],
                   y=county['lg_ln_amt'],
                   marker_color='orange'),
            # go.Bar(name='Large Loans', x=fips_df['year'], y='final_small_business_lending[4]'),
        ])

        bank_stack.update_layout(
            template=template,
            margin={"r": 5, "t": 32, "l": 100, "b": 20},
            showlegend=False,
            title={
                'text': "Small Business Loan Lending",
                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            # yaxis=dict(
            #     title='Dollar Amount',
            # ),
            # xaxis=dict(
            #     title='Year',
            # ),
            yaxis_tickformat=',',
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor=hoverBgColor,
                font_size=14,
            ),
            font=dict(
                family="Cardo",
                size=14,
                color=fontColor
            ),
            paper_bgcolor=color,
            plot_bgcolor=color
            # separators=',',
        ),
        # bank_stack.update_xaxes(showline=True)
        bank_stack.update_yaxes(title_text="Dollar", tickangle=35, showgrid=True, gridcolor='#6b6b6b')
        # ////////////////// End of chart 4 (small business loan lending) /////////////////////////////////////////

        # render plotly chart 5
        # with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        #     counties = json.load(response)
        #
        # county = px.choropleth(geojson=counties,
        #                        locations=nbr_map[0],
        #                        color=nbr_2019['med_hh_inc'],
        #                        color_continuous_scale="Earth",
        #                        scope='usa',
        #                        hover_name=nbr_2019['county'],
        #                        labels={'locations': 'FIPS ', 'color': 'Income '},
        #                        template='plotly_white',
        #                        )
        # county.update_geos(fitbounds="locations",
        #                    showsubunits=True,
        #                    subunitcolor="Black"
        #                    )
        # county.update_layout(
        #     title={
        #         'text': "Neighboring Counties Medium Household Income",
        #         'y': 0.97,
        #         'x': 0.5,
        #         'font_size': 20,
        #         'xanchor': 'center',
        #         'yanchor': 'top'},
        #     showlegend=False,
        #     font=dict(
        #         family="Cardo",
        #         size=14,
        #         color=fontColor
        #     ),
        #     hoverlabel=dict(
        #         bgcolor=hoverBgColor,
        #         font_size=16,
        #     ),
        #     margin={"r": 20, "t": 30, "l": 20, "b": 20},
        #     paper_bgcolor=color,
        #     # plot_bgcolor='#00586A'
        # ),

        # //////////////////////////////// All data queries for chart 6 (household income) ///////////////////////////
        #  Query for year and household income////////////////////////////////////

        # render plotly chart 6
        hhi_line = make_subplots()
        hhi_line.add_trace(
            go.Scatter(x=county['year'],
                       y=county['med_hh_inc'],
                       mode="markers+lines",
                       name="County",
                       hovertemplate=None,
                       line=dict(color='firebrick', width=2)
                       )),


        hhi_line.update_layout(
            # separators=',',
            showlegend=False,
            margin={"r": 5, "t": 20, "l": 80, "b": 20},
            title={
                'text': "Medium Household Income",
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor=hoverBgColor,
                font_size=14,
            ),
            font=dict(
                family="Cardo",
                size=14,
                color=fontColor
            ),
            yaxis_tickformat=',',
            template=template,
            paper_bgcolor=color,
            plot_bgcolor=color
        )
        # hhi_line.update_xaxes(showgrid=True, zeroline=True)
        hhi_line.update_yaxes(title_text="Dollar", tickangle=35, showgrid=True, gridcolor='#6b6b6b')
        # /////////////////////////////////////// End chart 6 (household income) ///////////////////////////////

        # dash = [pop_line, table, ee_stack, bank_stack, county, hhi_line]
        # graph = json.dumps(dash, cls=plotly.utils.PlotlyJSONEncoder)
        pop = plot(pop_line,
                   output_type='div',
                   include_plotlyjs=False)
        snap = plot(table,
                    output_type='div',
                    include_plotlyjs=False)
        employment = plot(ee_stack,
                          output_type='div',
                          include_plotlyjs=False)
        bank = plot(bank_stack,
                    output_type='div',
                    include_plotlyjs=False)
        household = plot(hhi_line,
                         output_type='div',
                         include_plotlyjs=False)
        return render(request,
                      'charts.html',
                      context={
                          'pop': pop,
                          'snap': snap,
                          'employment': employment,
                          'bank': bank,
                          'household': household
                      })


def back(request):
    return redirect('index')
