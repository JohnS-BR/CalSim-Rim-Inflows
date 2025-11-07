from extension_functions import create_final_flow_plots

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