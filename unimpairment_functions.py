import pandas as pd
from pandas import interval_range

from extension_functions import unimpaired_flows, get_diversions
import numpy as np
from datetime import datetime

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

    # Adds in Gerle Reservoir evap and Robbs Peak powerhouse and subtracts Gerle Creek below Loon Lake and Loon Lake powerhouse

    # 11430000: SF Rubicon River below Gerle Creek (what we are unimpairing)
    # 11429600: Gerle Reservoir
    # 11429300: Robbs Peak Powerhouse
    # 11429500: Gerle Creek below Loon Lake
    # 11429340: Loon Lake Powerhouse

    # if 11429600_evap, 11429300, or 11429340 are nans, just skip. so fill with zeros
    df_unimpaired = unimpaired_flows(df_gauge_data['11430000'],
                                     fl_additions=[df_gauge_data['11429600_evap'].fillna(0), df_gauge_data['11429300'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11429500'], df_gauge_data['11429340'].fillna(0)],
                                     )


    return df_unimpaired

def unimpaired_11419340(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11433040 PILOT C BL MUTTON CANYON NR GEORGETOWN CA. Follows the logic from CS3_I_STMPY_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Stumpy Meadows storage differences, Stumpy Meadows evaporation and Georgetown divide ditch

    # 11433040: Pilot Creek below Mutton Canyon
    # EDN: Stumpy Meadows Reservoir
    # 11432000: Georgetown divide ditch

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11433040'],
                                     fl_storages=[df_gauge_data['EDN'].fillna(0)],
                                     fl_additions=[df_gauge_data['EDN_evap'].fillna(0), df_gauge_data['11432000'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11433100(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11433100 LONG CANYON C NR FRENCH MEADOWS CA. Follows the logic from CS3_I_NCL003_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in North and South Fork Long Canyon Canal Diversions

    # 11433100: Long Canyon Creek near French Meadows
    # 11433060: South Fork Long Canyon Canal diversions
    # 11433080: North Fork Long Canyon Canal Diversions

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11433100'],
                                     fl_additions=[df_gauge_data['11433060'].fillna(0), df_gauge_data['11433080'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11433300(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11433300 MF AMERICAN R NR FORESTHILL CA. Follows the logic from CS3_I_MFA025_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11433300: Middle Fork of the American near Foresthill (what we are unimpairing)
    # 11429350: Loon Lake
    # 11428700: Hell Hole
    # 11427400: French Meadows
    # EDN: Stumpy Meadows
    # 11432000: Georgetown divide ditch
    # 11429300: Robbs Peak powerhouse

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11433300'],
                                     fl_storages=[df_gauge_data['11429350'].fillna(0), df_gauge_data['11428700'].fillna(0), df_gauge_data['11427400'].fillna(0), df_gauge_data['EDN'].fillna(0)],
                                     fl_additions=[df_gauge_data['11429350_evap'].fillna(0), df_gauge_data['11428700_evap'].fillna(0), df_gauge_data['11427400_evap'].fillna(0),
                                                   df_gauge_data['EDN_evap'].fillna(0), df_gauge_data['11432000'].fillna(0), df_gauge_data['11429300'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11433500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11433500 MF AMERICAN R NR AUBURN CA. Follows the logic from CS3_I_MFA001_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11433500: Middle Fork of the American near Auburn (what we are unimpairing)
    # 11429350: Loon Lake
    # 11428700: Hell Hole
    # 11427400: French Meadows
    # EDN: Stumpy Meadows
    # 11432000: Georgetown divide ditch
    # 11429300: Robbs Peak powerhouse

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11433500'],
                                     fl_storages=[df_gauge_data['11429350_MFA001'].fillna(0), df_gauge_data['11428700'].fillna(0), df_gauge_data['11427400'].fillna(0), df_gauge_data['EDN'].fillna(0)],
                                     fl_additions=[df_gauge_data['11429350_MFA001_evap'].fillna(0), df_gauge_data['11428700_evap'].fillna(0), df_gauge_data['11427400_evap'].fillna(0),
                                                   df_gauge_data['EDN_evap'].fillna(0), df_gauge_data['11432000'], df_gauge_data['11429300'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11435100(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11435100 PYRAMID C A TWIN BRIDGES CA. Follows the logic from CS3_I_ALOHA_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11435100: Pyramid creek (what we are unimpairing)
    # 11434900: Lake Aloha

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11435100'],
                                     fl_storages=[df_gauge_data['11434900']],
                                     fl_additions=[df_gauge_data['11434900_evap'].fillna(0)]
                                     )

    # calculate the alternative unimpairment that uses different Aloha data
    df_unimpaired_ALT = unimpaired_flows(df_gauge_data['11435100'],
                                     fl_storages=[df_gauge_data['11434900_ALT']],
                                     fl_additions=[df_gauge_data['11434900_ALT_evap'].fillna(0)]
                                     )

    return pd.concat([df_unimpaired, df_unimpaired_ALT], axis=1)


def unimpaired_11437000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11437000 CAPLES LK OUTLET NR KIRKWOOD CA. Follows the logic from CS3_I_CAPLS_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11437000: Caples Lake outlet (what we are unimpairing)
    # 11436999: Caples release
    # 11437500: Caples Spill
    # 11436950: Caples Lake

    # first fill what is missing with release + spill
    df_gauge_data['11437000_EXT'] = df_gauge_data['11437000'].fillna(df_gauge_data['11436999'] + df_gauge_data['11437500'])

    # replicate the calculations done in the CAPLS sheet
    df_storage_temp = df_gauge_data['11436950_CAPLS']
    df_storage_temp.loc[datetime(1922, 9, 30)] = 1.2
    df_storage_temp.loc[datetime(1924, 2, 29)] = df_storage_temp.loc[datetime(1924, 3, 31)]
    df_storage_temp.interpolate('linear', inplace=True)

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11437000_EXT'],
                                     fl_storages=[df_storage_temp],
                                     fl_additions=[df_gauge_data['11436950_CAPLS_evap'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11436000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11436000 SILVER LK OUTLET NR KIRKWOOD CA. Follows the logic from CS3_I_SILVR_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11436000: Silver Lake outlet (what we are unimpairing)
    # 11435900: Silver Lake

    # calcualte seepage for different storages
    df_seepage = pd.DataFrame(np.arange(0, 10.1, 0.1), columns=['Storage'])
    df_seepage['Seepage'] = 0.02733 * (df_seepage['Storage'] ** 2) - 0.13408 * df_seepage['Storage'] + 0.01
    df_seepage.loc[df_seepage['Storage'] < 5, 'Seepage'] = 0
    df_seepage['Storage'] = df_seepage['Storage'].round(1)

    # match based on the storage
    # this will get the largest value below or equal to the storage value
    df_gauge_data['11435900_seepage'] = (np.floor(df_gauge_data[['11435900']] * 10) / 10).merge(df_seepage, how='left', left_on='11435900', right_on='Storage')['Seepage'].values

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11436000'],
                                     fl_storages=[df_gauge_data['11435900'].fillna(0)],
                                     fl_additions=[df_gauge_data['11435900_ALT_evap'].fillna(0), df_gauge_data['11435900_seepage']]
                                     )

    return df_unimpaired


def unimpaired_11426190(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11426190 LAKE VALLEY CN NR EMIGRANT GAP  CA. Follows the logic from CS3_I_LKVLY_Rev2022F

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11426190: Lake Valley canal (what we are unimpairing)
    # 11426170: Lake Valley
    # YB236: Fish release from lake valley canal

    df_unimpaired = unimpaired_flows(df_gauge_data['11426190'],
                                     fl_storages=[df_gauge_data['11426170']],
                                     fl_additions=[df_gauge_data['11426170_evap'], df_gauge_data['YB236']]
                                     )

    return df_unimpaired


def unimpaired_11427000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11427000 NF AMERICAN R A NORTH FORK DAM  CA. Follows the logic from CS3_I_LKVLY_Rev2022F

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11427000: North Fork american river at north fork dam (what we are unimpairing)
    # 11426170: Lake Valley
    # 11426190: Lake valley canal

    df_unimpaired = unimpaired_flows(df_gauge_data['11427000'],
                                     fl_storages=[df_gauge_data['11426170']],
                                     fl_additions=[df_gauge_data['11426170_evap'], df_gauge_data['11426190']]
                                     )

    return df_unimpaired


def unimpaired_11426500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11426500 NF AMERICAN R NR COLFAX  CA. Follows the logic from CS3_I_LKVLY_Rev2022F

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11426500: North Fork American river near Colfax (what we are unimpairing)
    # 11426170: Lake Valley
    # 11426190: Lake valley canal

    df_unimpaired = unimpaired_flows(df_gauge_data['11426500'],
                                     fl_storages=[df_gauge_data['11426170']],
                                     fl_additions=[df_gauge_data['11426170_evap'], df_gauge_data['11426190']]
                                     )

    return df_unimpaired