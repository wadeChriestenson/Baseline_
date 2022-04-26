import sqlite3
from pandas import DataFrame
from .views import fipsNumber
import os


def fips_year_query(year, fips):
    """
    Query CRA & FDIC data by year & fips code from baseline database
    Returns dataframe
    Note: only queries available data for given year
    --> e.g. BDS data is not queried for 2019 because it is not currently available
    """

    conn = sqlite3.connect('baseline.db')  # connect to baseline database
    cur = conn.cursor()  # open cursor

    if int(year) > 2018:
        cur.execute(f"""SELECT cra.year, names.county, names.state, cra.fips, cra.sm_ln_ct, cra.sm_ln_vol,
                    fdic.tot_br_ct, fdic.st_br_ct, fdic.loc_br_ct, acs.tot_pop, acs.per_cap_inc, acs.med_hh_inc,
                    acs_add.unemp_perc, acs_add.no_int_perc, acs_add.brdbnd_perc

                    FROM cra{year} AS cra

                    INNER JOIN cty_adj as names
                    ON cra.fips = names.neighbor AND cra.fips = names.fips

                    INNER JOIN fdic{year} AS fdic
                    ON cra.fips = fdic.fips

                    INNER JOIN acs{year} AS acs
                    ON cra.fips = acs.fips

                    INNER JOIN acs_add{year} acs_add
                    ON cra.fips = acs_add.fips

                    WHERE cra.fips IN (
                        SELECT neighbor FROM cty_adj
                        WHERE fips = {fips})""")  # query database for neighboring & specified counties

        names = [description[0] for description in cur.description]  # get column names
        names[3] = 'neighbor_fips'  # change column name for neibgoring fips
        df = DataFrame(cur.fetchall(), columns=names)

    elif int(year) > 2017:
        cur.execute(f"""SELECT cra.year, names.county, names.state, cra.fips, bds.emp, bds.estabs_entry,
                    bds.estabs_exit, bds.net_job_creation, cra.sm_ln_ct, cra.sm_ln_vol, fdic.tot_br_ct,
                    fdic.st_br_ct, fdic.loc_br_ct, acs.tot_pop, acs.per_cap_inc, acs.med_hh_inc, acs_add.unemp_perc,
                    acs_add.no_int_perc, acs_add.brdbnd_perc

                    FROM cra{year} AS cra

                    INNER JOIN cty_adj as names
                    ON cra.fips = names.neighbor AND cra.fips = names.fips

                    INNER JOIN fdic{year} AS fdic
                    ON cra.fips = fdic.fips

                    INNER JOIN acs{year} AS acs
                    ON cra.fips = acs.fips

                    INNER JOIN acs_add{year} acs_add
                    ON cra.fips = acs_add.fips

                    INNER JOIN bds{year} AS bds
                    ON cra.fips = bds.fips

                    WHERE cra.fips IN (
                        SELECT neighbor FROM cty_adj
                        WHERE fips = {fips})""")  # query database for neighboring & specified counties

        names = [description[0] for description in cur.description]  # get column names
        names[3] = 'neighbor_fips'  # change column name for neibgoring fips
        df = DataFrame(cur.fetchall(), columns=names)

    else:
        cur.execute(f"""SELECT cra.year, names.county, names.state, cra.fips, bds.emp, bds.estabs_entry,
                    bds.estabs_exit, bds.net_job_creation, cra.sm_ln_ct, cra.sm_ln_vol, fdic.tot_br_ct,
                    fdic.st_br_ct, fdic.loc_br_ct, acs.tot_pop, acs.per_cap_inc, acs.med_hh_inc

                    FROM cra{year} AS cra

                    INNER JOIN cty_adj as names
                    ON cra.fips = names.neighbor AND cra.fips = names.fips

                    INNER JOIN fdic{year} AS fdic
                    ON cra.fips = fdic.fips

                    INNER JOIN acs{year} AS acs
                    ON cra.fips = acs.fips

                    INNER JOIN bds{year} AS bds
                    ON cra.fips = bds.fips

                    WHERE cra.fips IN (
                        SELECT neighbor FROM cty_adj
                        WHERE fips = {fips})""")  # query database for neighboring & specified counties

        names = [description[0] for description in cur.description]  # get column names
        names[3] = 'neighbor_fips'  # change column name for neibgoring fips
        df = DataFrame(cur.fetchall(), columns=names)

    cur.close()  # close cursor
    conn.close()  # close connection

    return df  # return dataframe


def fips_query(fips, years=[]):
    """
    Takes year as a list and fips as a single number
    Returns 3 dataframes
    --> fips_df: data for queried fips code
    --> nbr_df: data for each county adjacent to queried fips code
    --> nbr_avg: average values for all neighboring counties, for all variables, across each year
    Note: Returns 'NaN' where data is unavailable

    Variable descriptions (all data is county specific and applies to previous 12 months):
        year, county, state, & fips are self-explanatory
        emp: total employment - from Census Bureau Business Dynamics Statistics (BDS) time series
        estabs_entry: total businesses opened - BDS data
        estabs_exit: total businesses closed - BDS data
        net_job_creation: total jobs created minus total jobs lost - BDS data
        sm_ln_ct: total number of business loans < $100k at time or origination - from Community Reinvestment Act (CRA) data
        sm_ln_vol: total volume of business loans < $100k at time of origination - CRA data
        tot_br_ct: total bank branches in county - from FDIC data
        st_br_ct: total bank branches in county with in-state headquarters - FDIC data
        loc_br_ct: total bank branches in county with in-county headquarters - FDIC data
        tot_pop: total population - from Census Bureau's American Community Survey (ACS) 5-year estimates
        per_cap_inc: per capita income - ACS 5-year estimates
        med_hh_inc: median household income - ACS 5-year estimates
        unemp_perc: percentage of available labor force not employed - ACS 5-year estimates
        no_int_perc: percentage of households without internet access - ACS 5-year estimates
        brdbnd_perc: percentage of household with broadband internet access - ACS 5-year estimates

    Example query for Polk County, Oregon from 2010-2019:

        fips = 41053 # call county by fips code
        years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'] # years as a list of str's

        fips_df, nbr_df, nbr_avg = fips_query(fips=fips, years=years) # returns 3 dataframes (described above)
    """

    if years is None:
        years = []
    years = [str(x) for x in years]
    df = fips_year_query(years[0], fips)
    if len(years) > 1:
        for year in years[1:]:
            df = df.append(fips_year_query(year, fips))

    df.sort_values('neighbor_fips', inplace=True)  # dataframe of queried and neighbor fips data

    fips_df = df[df.neighbor_fips == fips].copy()
    fips_df.columns = fips_df.columns.str.replace('neighbor_fips', 'fips')
    fips_df.sort_values('year', inplace=True)
    fips_df.reset_index(inplace=True, drop=True)  # queried fips data for all years

    nbr_df = df[df.neighbor_fips != fips].copy()
    nbr_df.sort_values(['neighbor_fips', 'year'], inplace=True)
    nbr_df.reset_index(inplace=True, drop=True)  # neighbor fips data for all years

    new_df = nbr_df.drop(columns=['county', 'state', 'neighbor_fips'])
    nbr_avg = new_df.groupby('year').mean()

    nbr_avg.reset_index(inplace=True)
    nbr_avg.unemp_perc = [round(x, 2) for x in nbr_avg.unemp_perc]
    nbr_avg.no_int_perc = [round(x, 2) for x in nbr_avg.no_int_perc]
    nbr_avg.brdbnd_perc = [round(x, 2) for x in nbr_avg.brdbnd_perc]
    nbr_avg['emp'] = [round(nbr_avg.emp[x], 0) for x in range(len(nbr_avg))]
    nbr_avg['estabs_entry'] = [round(nbr_avg.estabs_entry[x], 0) for x in range(len(nbr_avg))]
    nbr_avg['estabs_exit'] = [round(nbr_avg.estabs_exit[x], 0) for x in range(len(nbr_avg))]
    nbr_avg['net_job_creation'] = [round(nbr_avg.net_job_creation[x], 0) for x in range(len(nbr_avg))]
    nbr_avg[nbr_avg.columns[5:-3]] = nbr_avg[nbr_avg.columns[5:-3]].astype(int, errors='ignore')  # neighbors averages

    return fips_df, nbr_df, nbr_avg


def FIP(request):
    if request.method == 'POST':
        FIPS = request.POST['fips']
        print(type(FIPS))
        print('Fips: ', FIPS)
        return FIPS


############################################################################################
# expample query for Boulder County, CO                                                     #
fips = FIP
years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']  #

############################################################################################


fips_df, nbr_df, nbr_avg = fips_query(fips=fips,
                                      years=years)  # specify fips as integer & years as list of strings (2010-2019)
