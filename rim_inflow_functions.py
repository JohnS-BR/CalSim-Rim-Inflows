import pandas as pd
from extension_functions import create_final_flow_plots, area_scale

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
    df_rim_inflows['I_FRMDW'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2008)) + list(range(2009, 2024)), 'I_FRMDW')


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
    df_location = df_location - df_rim_inflows['I_FRMDW'] - df_rim_inflows['I_DCC010']

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
    df_location = df_extended_data['11433040']

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

    # we want the max of the scaled unimpared data and this gauge location
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