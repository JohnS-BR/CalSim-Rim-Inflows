import pandas as pd
import numpy as np
from extension_functions import create_final_flow_plots, area_scale, remove_negatives_timeseries

def I_DCC010(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_DCC010

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11427700']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_DCC010'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1961, 2025)), 'I_DCC010')


def I_FRMDW(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_FRMDW

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11427500']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_FRMDW_G'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2008)) + list(range(2009, 2024)), 'I_FRMDW_G')

    # pull out the relevant station
    df_location = df_extended_data['11427500_ALTERED']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_FRMDW_F'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2008)) + list(range(2009, 2024)), 'I_FRMDW_F')


def I_MFA036(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFA036

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11427760']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_FRMDW_G'] - df_rim_inflows['I_DCC010']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFA036'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2008)), 'I_MFA036')


def I_RUB047(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_RUB047

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11428000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_RUB047'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1957, 1987)), 'I_RUB047')


def I_LRB004(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LRB004

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11428400']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LRB004'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1991, 2016)), 'I_LRB004')


def I_HHOLE(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_HHOLE

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11428800']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_LRB004'] - df_rim_inflows['I_RUB047']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_HHOLE'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2008)) + list(range(2009, 2025)), 'I_HHOLE')


def I_LOONL(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LOONL

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11429500']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LOONL'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1963, 2025)), 'I_LOONL')

def I_SFA066(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFA066

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11439501']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_CAPLS'] - df_rim_inflows['I_SILVR'] - df_rim_inflows['I_ALOHA'] - df_rim_inflows['I_PYR001']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # scaled by the water shed factors
    df_location = df_location * 0.443

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFA066'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 2025)), 'I_SFA066')


def I_SFR006(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFR006

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11430000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # scaled by the water shed factors
    df_location = df_location * 0.401

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFR006'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1963, 2022)), 'I_SFR006')


def I_GERLE(df_extended_data, df_rim_inflows):
    """
        Calculate the final rim inflow for CalSim. Location: I_GERLE

        Parameters
        ----------
        df_extended_data: dataframe
            Dataframe of extended (and unimpaired where relevant) data to pull from
        df_rim_inflows: dataframe
            Dataframe of rim inflows that have been calculated already

        Returns
        -------
        None
        """

    # pull out the relevant station
    df_location = df_rim_inflows['I_SFR006']

    # scale it based on area change
    df_location = area_scale(df_location, d_area_1=0.599, d_area_2=0.401)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_GERLE'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1963, 2022)), 'I_GERLE')


def I_STMPY(df_extended_data, df_rim_inflows):
    """
        Calculate the final rim inflow for CalSim. Location: I_STMPY

        Parameters
        ----------
        df_extended_data: dataframe
            Dataframe of extended (and unimpaired where relevant) data to pull from
        df_rim_inflows: dataframe
            Dataframe of rim inflows that have been calculated already

        Returns
        -------
        None
        """

    # pull out the relevant station
    df_location = df_extended_data['11433040']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # scaled by the water shed factors
    df_location = df_location * 0.716

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_STMPY'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1962, 2018)) + list(range(2019, 2025)), 'I_STMPY')


def I_PLC007(df_extended_data, df_rim_inflows):
    """
        Calculate the final rim inflow for CalSim. Location: I_PLC007

        Parameters
        ----------
        df_extended_data: dataframe
            Dataframe of extended (and unimpaired where relevant) data to pull from
        df_rim_inflows: dataframe
            Dataframe of rim inflows that have been calculated already

        Returns
        -------
        None
        """

    # pull out the relevant station
    df_location = df_extended_data['11433040_ALTERED']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # scaled by the water shed factors
    df_location = df_location * 0.284

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_PLC007'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1962, 2018)) + list(range(2019, 2025)), 'I_PLC007')


def I_NLC003(df_extended_data, df_gauge_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NLC003

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11433100']

    # scaled by the water shed factors
    df_location = df_location * 0.15

    # we want the max of the scaled unimpaired data and this gauge location
    df_location = pd.concat([df_location, df_gauge_data['11433080']], axis=1).max(axis=1)

    # trim off the first date that gets added
    df_location = df_location.iloc[1:]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NLC003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1967, 1993)), 'I_NLC003')

def I_SLC003(df_extended_data, df_gauge_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SLC003

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11433100']

    # scaled by the water shed factors
    df_location = df_location * 0.27

    # we want the max of the scaled unimpaired data and this gauge location
    df_location = pd.concat([df_location, df_gauge_data['11433060']], axis=1).max(axis=1)

    # trim off the first date that gets added
    df_location = df_location.iloc[1:]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SLC003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1967, 1993)), 'I_SLC003')

def I_LNG012(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LNG012

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11433100_AMF']

    df_location = df_location - df_rim_inflows['I_NLC003'] - df_rim_inflows['I_SLC003']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LNG012'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1967, 1993)), 'I_LNG012')


def I_RUB002(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_RUB002

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # these are just all zero
    df_rim_inflows['I_RUB002'] = 0

def I_NMA003(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NMA003

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11433260']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NMA003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 1986)), 'I_NMA003')


def I_MFA025(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFA025

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11433300']

    # subtract upstream
    df_location = (df_location - df_rim_inflows['I_FRMDW_F'] - df_rim_inflows['I_RUB002'] - df_rim_inflows['I_PLC007'] - df_rim_inflows['I_STMPY'] - df_rim_inflows['I_LNG012'] -
                   df_rim_inflows['I_SLC003'] - df_rim_inflows['I_NLC003'] - df_rim_inflows['I_SFR006'] - df_rim_inflows['I_LOONL'] - df_rim_inflows['I_LRB004'] - df_rim_inflows['I_RUB047']
                   - df_rim_inflows['I_HHOLE'] - df_rim_inflows['I_NMA003'] - df_rim_inflows['I_MFA036'] - df_rim_inflows['I_DCC010'] - df_rim_inflows['I_GERLE'])

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # watershed factor
    df_location = df_location * 0.853

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFA025'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1959, 2025)), 'I_MFA025')


def I_MFA023(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFA023

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_rim_inflows['I_MFA025']

    # scale it based on area change
    df_location = area_scale(df_location, d_area_1=0.147, d_area_2=0.853)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFA023'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1959, 2025)), 'I_MFA023')


def I_MFA001(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFA001

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11433500']

    # subtract upstream
    df_location = (df_location - df_rim_inflows['I_FRMDW_F'] - df_rim_inflows['I_RUB002'] - df_rim_inflows['I_PLC007'] - df_rim_inflows['I_STMPY'] - df_rim_inflows['I_LNG012'] -
                   df_rim_inflows['I_SLC003'] - df_rim_inflows['I_NLC003'] - df_rim_inflows['I_SFR006'] - df_rim_inflows['I_LOONL'] - df_rim_inflows['I_LRB004'] - df_rim_inflows['I_RUB047']
                   - df_rim_inflows['I_HHOLE'] - df_rim_inflows['I_NMA003'] - df_rim_inflows['I_MFA036'] - df_rim_inflows['I_DCC010'] - df_rim_inflows['I_GERLE'] - df_rim_inflows['I_MFA023']
                   - df_rim_inflows['I_MFA025'])

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFA001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1921, 1986)), 'I_MFA001')


def I_ALOHA(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ALOHA

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11435100_B']

    # first year gets the data from the A extension
    df_location.iloc[:12] = df_extended_data['11435100_A'].iloc[:12]

    # cale by watershed
    df_location = df_location * 0.384

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ALOHA'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(2012, 2022)), 'I_ALOHA')


def I_PYR001(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_PYR001

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11435100_B']

    # first year gets the data from the A extension
    df_location.iloc[:12] = df_extended_data['11435100_C'].iloc[:12]

    # cale by watershed
    df_location = df_location * 0.616

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_PYR001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(2012, 2022)), 'I_PYR001')


def I_CAPLS(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_CAPLS

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11437000_B']

    # first year gets the data from the A extension
    df_location.iloc[:12] = df_extended_data['11437000_A'].iloc[:12]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_CAPLS'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1993)) + list(range(1998, 2025)), 'I_CAPLS')


def I_SILVR(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SILVR

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11436000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SILVR'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 2025)), 'I_SILVR')


def I_LKVLY(df_unimpaired_data, df_full_data, df_rim_inflows, df_factors):
    """
    Calculate the final rim inflow for CalSim. Location: I_LKVLY

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_full_data: dataframe
        Dataframe of the gauge data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    df_factors: dataframe
        Watershed factors

    Returns
    -------
    None
    """

    df_nf_american = df_unimpaired_data['11427000'] * df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0]

    df_nf_american.fillna(df_unimpaired_data['11426500'] * df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0] * 1.070, inplace=True)

    df_lake_valley_canal = df_unimpaired_data['11426190'] * df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0] / (df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0] +
                                                                                                                                 df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0])

    df_location = pd.Series(np.where(df_full_data['11426170'].iloc[1:] < 7.99, df_lake_valley_canal, pd.concat([df_lake_valley_canal, df_nf_american], axis=1).max(axis=1)), index=df_nf_american.index)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LKVLY'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_LKVLY')


def I_NNA013(df_unimpaired_data, df_full_data, df_rim_inflows, df_factors):
    """
    Calculate the final rim inflow for CalSim. Location: I_NNA013

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_full_data: dataframe
        Dataframe of the gauge data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    df_factors: dataframe
        Watershed factors

    Returns
    -------
    None
    """

    df_nf_american = df_unimpaired_data['11427000'] * df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0]

    df_nf_american.fillna(df_unimpaired_data['11426500'] * df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0] * 1.070, inplace=True)

    df_lake_valley_canal = df_unimpaired_data['11426190'] * df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0] / (df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0] +
                                                                                                                                  df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0])

    df_location = pd.Series(np.where(df_full_data['11426170'].iloc[1:] < 7.99, df_lake_valley_canal, pd.concat([df_lake_valley_canal, df_nf_american], axis=1).max(axis=1)), index=df_nf_american.index)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NNA013'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NNA013')


def I_NFA054(df_unimpaired_data, df_rim_inflows, df_factors):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFA054

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    df_factors: dataframe
        Watershed factors

    Returns
    -------
    None
    """

    df_location = df_unimpaired_data['11427000'] * df_factors[df_factors['Location'] == 'I_NFA054']['Factor'].iloc[0]

    df_location.fillna(df_unimpaired_data['11426500'] * df_factors[df_factors['Location'] == 'I_NFA054']['Factor'].iloc[0] * 1.070, inplace=True)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFA054'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFA054')


def I_CYN009(df_unimpaired_data, df_rim_inflows, df_factors):
    """
    Calculate the final rim inflow for CalSim. Location: I_CYN009

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    df_factors: dataframe
        Watershed factors

    Returns
    -------
    None
    """

    df_location = df_unimpaired_data['11427000'] * df_factors[df_factors['Location'] == 'I_CYN009']['Factor'].iloc[0]

    df_location.fillna(df_unimpaired_data['11426500'] * df_factors[df_factors['Location'] == 'I_CYN009']['Factor'].iloc[0] * 1.070, inplace=True)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_CYN009'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_CYN009')

def I_NFA022(df_unimpaired_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFA022

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    df_location = df_unimpaired_data['11427000']

    df_location.fillna(df_unimpaired_data['11426500'] * 1.070, inplace=True)

    df_location = df_location - df_rim_inflows['I_NFA054'] - df_rim_inflows['I_NNA013'] - df_rim_inflows['I_LKVLY'] - df_rim_inflows['I_CYN009']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFA022'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFA022')

def I_NFA016(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFA016

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
        """

    df_location = df_rim_inflows['I_NFA022'] * 0.070803

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFA016'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFA016')


def I_SFA076(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFA076

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
        """

    df_location = df_rim_inflows['I_SFA066'] * 0.260 / 0.443

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFA076'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 2025)), 'I_SFA076')


def I_SLF009(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SLF009

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
        """

    df_location = df_rim_inflows['I_SFA066'] * 0.297 / 0.443

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SLF009'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 2025)), 'I_SLF009')


def I_ALD004(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ALD004

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11440000_B']

    # first year uses A data
    df_location.iloc[:12] = df_extended_data['11440000_A'].iloc[:12]

    # watershed factor
    df_location = df_location * 0.848

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ALD004'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1982)), 'I_ALD004')