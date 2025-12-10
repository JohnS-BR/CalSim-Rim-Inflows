from extension_functions import unimpaired_flows, get_diversions
import numpy as np

def unimpaired_11439501(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11439501 SF AMERICAN R NR KYBURZ TOTAL FLOW CA. Follows the logic from CS3_I_SFA066_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Add differences in Caples, Silver, and Aloha storage and Caples, Silver, and Aloha evaporation, and subtracts Echo Lake Conduit flow

    # 11439501: South Fork American River near Kyburz (what we are unimpairing)
    # 11434500: Echo Lake Conduit
    # 11436950: Caples Lake
    # 11435900: Silver Lake
    # 11434900: Lake Aloha
    # currently gap fillinf aloha with 0s but this would probably want to change in the future
    df_unimpaired = unimpaired_flows(df_gauge_data['11439501'],
                                     fl_storages=[df_gauge_data['11436950'], df_gauge_data['11435900'], df_gauge_data['11434900'].fillna(0)],
                                     fl_additions=[df_gauge_data['11436950_evap'], df_gauge_data['11435900_evap'], df_gauge_data['11434900_evap'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11434500']])

    return df_unimpaired


def unimpaired_11427500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11427500 MF AMERICAN R A FRENCH MEADOWS CA. Follows the logic from CS3_I_FRMDW_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Add differences in French Meadows storage, French Meadows evaporation, and French Meadows power plant and subtracts Duncan Creek Diversion

    # Calculate duncan creek diversion
    df_duncan_creek_diversions = get_diversions(df_gauge_data['11427700'], df_gauge_data['11427750'], 9.94, 10.5)

    # 11427500: Middle Fork American River at French Meadows (what we are unimpairing)
    # 11427400: French Meadows Reservoir
    # 11427200: French Meadows Power Plant
    # df_duncan_creek_diversions: Duncan Creek Diversions (previously calculated)
    df_unimpaired = unimpaired_flows(df_gauge_data['11427500'],
                                     fl_storages=[df_gauge_data['11427400']],
                                     fl_additions=[df_gauge_data['11427200'], df_gauge_data['11427400_evap']],
                                     fl_subtractions=[df_duncan_creek_diversions])

    return df_unimpaired


def unimpaired_11427760(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11427760 MF AMERICAN R AB MF PH NR FORESTHILL CA. Follows the logic from CS3_I_MFA036_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Add differences in French Meadows storage, French Meadows evaporation, and French Meadows power plant

    # 11427760: Middle Fork American River above North Fork near Foresthill (what we are unimpairing)
    # 11427400: French Meadows Reservoir
    # 11427200: French Meadows Power Plant
    df_unimpaired = unimpaired_flows(df_gauge_data['11427760'],
                                     fl_storages=[df_gauge_data['11427400']],
                                     fl_additions=[df_gauge_data['11427200'], df_gauge_data['11427400_evap']],
                                     )

    return df_unimpaired


def unimpaired_11428000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11428000 RUBICON R A RUBICON SPRINGS NR MEEKS BAY CA. Follows the logic from CS3_I_RUB047_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Rubicon Rockbound Tunnel

    # 11428000: Rubicon River at Rubicon Springs (what we are unimpairing)
    # 11427940: Rubicon Rockbound Tunnel
    # fill na with zero because we dont want nans if that data is missing
    df_unimpaired = unimpaired_flows(df_gauge_data['11428000'],
                                     fl_additions=[df_gauge_data['11427940'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11428400(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11428400 L RUBICON R BL BUCK ISLAND DAM CA. Follows the logic from CS3_I_LRB004_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Buck Loon Tunnel and subtracts Rubicon Rockbound Tunnel

    # 11428400: Little Rubicon River (what we are unimpairing)
    # 11428300: Buck Loon Tunnel
    # 11427940: Rubicon Rockbound Tunnel
    df_unimpaired = unimpaired_flows(df_gauge_data['11428400'],
                                     fl_additions=[df_gauge_data['11428300']],
                                     fl_subtractions=[df_gauge_data['11427940']],
                                     )

    return df_unimpaired


def unimpaired_11428800(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11428800 RUBICON R BL HELL HOLE DAM CA. Follows the logic from CS3_I_HHOLE_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Hell Hole storage differences, Hell Hole evaporation, Middle Fork PH, and Buck Look Tunnel, and subtracts French Meadows power plant and Long Canyon Canal diversions

    # 11428800: Rubicon River below Hell Hole (what we are unimpairing)
    # 11428700: Hell Hole Reservoir
    # 11428600: Middle Fork PH
    # 11428300: Buck Look Tunnel
    # 11427200: French Meadows power plant
    # 11433060: South Fork Long Canyon Canal diversions
    # 11433080: North Fork Long Canyon Canal Diversions
    # fill the nans with zeros for the locations where we can skip if it is a nan
    df_unimpaired = unimpaired_flows(df_gauge_data['11428800'],
                                     fl_storages=[df_gauge_data['11428700']],
                                     fl_additions=[df_gauge_data['11428700_evap'], df_gauge_data['11428600'].fillna(0), df_gauge_data['11428300'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11427200'], df_gauge_data['11433060'].fillna(0), df_gauge_data['11433080'].fillna(0)],
                                     )

    return df_unimpaired


def unimpaired_11429500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11429500 GERLE C BL LOON LK NR MEEKS BAY CA. Follows the logic from CS3_I_LOONL_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Loon Lake storage differences and Loon Lake evaporation and subtracts Buck Look Tunnel

    # 11429500: Gerle Creek below Loon Lake (what we are unimpairing)
    # 11429340: Look Lake PH
    # 11429350: Look Lake
    # 11428300: Buck Look Tunnel

    # this will be when there is data for 11429340
    df_unimpaired_all = unimpaired_flows(df_gauge_data['11429500'],
                                     fl_storages=[df_gauge_data['11429350'].fillna(0)],
                                     fl_additions=[df_gauge_data['11429350_evap'].fillna(0), df_gauge_data['11429340'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11428300_LL'].fillna(0)],
                                     )

    # this will be when there is no data for 11429340 but is reservoir data
    df_unimpaired_no_ph = unimpaired_flows(df_gauge_data['11429500'],
                                         fl_storages=[df_gauge_data['11429350'].fillna(0)],
                                         fl_additions=[df_gauge_data['11429350_evap'].fillna(0)],
                                         fl_subtractions=[df_gauge_data['11428300_LL'].fillna(0)],
                                         )

    # combine these with the gauge data used when it is the only data
    df_unimpaired = np.where(~df_gauge_data['11429340'].isna(),
                             df_unimpaired_all,
                             np.where(~df_gauge_data['11429500'].isna() & ((df_gauge_data['11429350'].isna()) | (df_gauge_data['11429350'] == 0)),
                                      df_gauge_data['11429500'],
                                      df_unimpaired_no_ph))

    return df_unimpaired

def unimpaired_11430000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11430000 SF RUBICON R BL GERLE C NR GEORGETOWN CA. Follows the logic from CS3_I_LOONL_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Loon Lake storage differences and Loon Lake evaporation and subtracts Buck Look Tunnel

    # 11430000: SF Rubicon River below Gerle Creek (what we are unimpairing)
    # 11429600: Gerle Reservoir
    # 11429300: Robbs Peak Powerhouse
    # 11429500: Gerle Creek below Loon Lake
    # 11429340: Look Lake Powerhouse

    # if 11429600_evap, 11429300, or 11429340 are nans, just skip. so fill with zeros
    df_unimpaired = unimpaired_flows(df_gauge_data['11430000'],
                                     fl_additions=[df_gauge_data['11429600_evap'].fillna(0), df_gauge_data['11429300'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11429500'], df_gauge_data['11429340'].fillna(0)],
                                     )


    return df_unimpaired