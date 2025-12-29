from pydsstools.heclib.dss import HecDss
import pandas as pd
from datetime import timedelta
import numpy as np


def read_evap_data(s_path, s_b_part):
    """
    Reads in the evap rates from the evap DSS file
    Parameters
    ----------
    s_path: str
        Path to DSS file
    s_b_part:str
        B part for reading from the DSS file

    Returns
    -------
    df_dss_data: dataframe
        Data from the DSS file corresponding to the B part
    """

    # open the DSS file
    o_file = HecDss.Open(s_path)

    # get the potential paths for this b part
    ls_paths = o_file.getPathnameList(f"/CALSIM/{s_b_part}/EVAPORATION-RATE/*/1Month/*/")

    # if there are no paths, it doesn't exist and we want to fail
    if ls_paths == []:
        raise Exception(f"No paths found for {s_b_part} in {s_path}")

    # get the path but replace the date with a blank so we get the full timeseries
    ls_final_path = ls_paths[0].split('/')
    ls_final_path[4] = ''
    s_final_path = '/'.join(ls_final_path)

    # read the timeseries in
    o_timeseries = o_file.read_ts(s_final_path, trim_missing=True)

    # check that it is not empty
    if o_timeseries.empty:
        raise Exception(f"Empty timeseries at path: {s_final_path}")

    # put it in a dataframe with the units as the column name
    df_dss_data = pd.DataFrame(o_timeseries.values, index=o_timeseries.pytimes, columns=[o_timeseries.units])

    # adjust the dates to match what they should be
    df_dss_data.index = df_dss_data.index + timedelta(days=-1)

    # return the dataframe
    return df_dss_data.copy()


def calculate_evap_data(df_storage_data, df_evap_rates, df_area_capacity, b_set_zeros=True):
    """
    Calculate the evaporation amounts based on the rates and storage
    Parameters
    ----------
    df_storage_data: dataframe
        Storage data for the reservoir
    df_evap_rates: dataframe
        Evaporation rates for the reservoir
    df_area_capacity: dataframe
        Area capacity relationship for the reservoir
    d_max_cap: float
        Max capacity for the reservoir (TAF)
    d_max_area: float
        Max area for the reservoir (Acres)
    b_set_zeros: bool
        Flag for if

    Returns
    -------
    df_evaporation_data: dataframe
        Evaporation data for the reservoir
    """

    # if the storage data is a series, convert to dataframe
    if isinstance(df_storage_data, pd.Series):
        df_storage_data = pd.DataFrame(df_storage_data)
        df_storage_data.columns = ['TAF']

    # get the storage averages
    df_storage_data['Averages'] = (df_storage_data['TAF'] + df_storage_data['TAF'].shift(1)) / 2

    # evap rates are in inches, convert to feet
    df_evap_rates['Feet'] = df_evap_rates['IN']/12

    # create empty evap dataframe that we will fill
    df_evaporation_data = pd.DataFrame(index=df_evap_rates.index, columns=['TAF'], dtype='float')

    # loop through the storage timeseries
    for index, row in df_storage_data.iterrows():
        # check if the row is nans
        if row.isna().any():
            df_evaporation_data.loc[index, 'TAF'] = np.nan

        elif b_set_zeros and row.iloc[0] == 0:
            df_evaporation_data.loc[index, 'TAF'] = 0

        else:
            # linearly interpolate the capacities to get the area value for the current capacity. units are acers here
            d_pred_area = np.interp(row['Averages'], df_area_capacity['Capacity'], df_area_capacity['Area'])

            # multiply but the evap rate
            df_evaporation_data.loc[index, 'TAF'] = d_pred_area * df_evap_rates.loc[index, 'Feet'] / 1000

    # return the dataframe
    return df_evaporation_data.copy()


def calc_evap_11427400(s_dss_file, df_storage_data):
    """
    Calculates the evaporation amount for USGS 11427400 FRENCH MEADOWS RES NR FORESTHILL CA; CDEC ID FMD FRENCH MEADOWS. Follows the logic in CS3_I_FRMDW_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_FRMDW')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11427400_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # calculate and set the evaporation
    df_storage_data['11427400_evap'] = calculate_evap_data(df_storage_data['11427400'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)


def calc_evap_11436950(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11436950 CAPLES LK NR KIRKWOOD CA; CDEC CAPLES LAKE (PG&E) (CPL). Follows the logic in CS3_I_SFA006_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_CAPLS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11436950_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # add in a row with a maximum capacity and area
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [23, 620]

    # update the one area that needs to be raised. this is done in the sheet
    df_area_capacity.loc[10, 'Area'] = 596

    # calculate and set the evaporation
    df_storage_data['11436950_evap'] = calculate_evap_data(df_storage_data['11436950'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], False)
    df_storage_data['11436950_CAPLS_evap'] = calculate_evap_data(df_storage_data['11436950_CAPLS'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], False)


def calc_evap_11435900(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11435900 SILVER LK NR KIRKWOOD CA; CDEC SILVER LAKE RESERVOIR (SIV). Follows the logic in CS3_I_SFA006_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SILVR')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11435900_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # add in a row with a maximum capacity and area
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [8.792, 385]

    # calculate and set the evaporation
    df_storage_data['11435900_evap'] = calculate_evap_data(df_storage_data['11435900'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], False)
    df_storage_data['11435900_ALT_evap'] = calculate_evap_data(df_storage_data['11435900_ALT'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11434900(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11434900 LK ALOHA NR PHILLIPS(MEDLEY LAKE) CA. Follows the logic in CS3_I_SFA006_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # the original need uses different evap rates from the dss file so we will pull from a csv
    # df_evap_rates = read_evap_data(s_dss_file, 'ER_ALOHA')
    df_evap_rates = pd.read_csv(r"./Inputs/modified_evap_rates.csv", index_col=0, parse_dates=True)[['ALOHA']]
    df_evap_rates.columns = ['IN']

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11434900_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (AF)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (AF)'].shift(1) - df_area_capacity['Capacity (AF)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # add in a row with a maximum capacity and area
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [5.35, 627]

    # adjust one elevation to match the sheet
    df_area_capacity.loc[7, 'Capacity'] = df_area_capacity.loc[6, 'TAF']

    # set teh first row to be slighltly above 0 to match the sheet
    df_area_capacity.loc[0, ['Capacity', 'Area']] = [0.001, 0.001]

    # calculate and set the evaporation
    df_storage_data['11434900_evap'] = calculate_evap_data(df_storage_data['11434900'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)
    # calculate the alternative evaporation that uses different Aloha data
    df_storage_data['11434900_ALT_evap'] = calculate_evap_data(df_storage_data['11434900_ALT'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11428700(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11428700 HELL HOLE RES NR MEEKS BAY CA. Follows the logic in CS3_I_HHOLE_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_HHOLE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11428700_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (AF)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (AF)'].shift(1) - df_area_capacity['Capacity (AF)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # calculate and set the evaporation
    df_storage_data['11428700_evap'] = calculate_evap_data(df_storage_data['11428700'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11429350(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11429350 LOON LK NR MEEKS BAY CA. Follows the logic in CS3_I_LOONL_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_LOONL')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11429350_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 1450
    df_area_capacity.loc[df_area_capacity['Area'] > 1450, 'Area'] = 1450

    # calculate and set the evaporation
    df_storage_data['11429350_evap'] = calculate_evap_data(df_storage_data['11429350'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11429600(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11429600 GERLE RES NR MEEKS BAY CA. Follows the logic in CS3_I_SFR006_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_GERLE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11429600_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # uses straight data not averages
    df_area_capacity['Elevation'] = df_area_capacity['Elevation (ft)']
    df_area_capacity['Capacity'] = df_area_capacity['TAF']

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 50
    df_area_capacity.loc[df_area_capacity['Area'] > 50, 'Area'] = 50

    # calculate and set the evaporation
    df_storage_data['11429600_evap'] = calculate_evap_data(df_storage_data['11429600'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_EDN(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for CDEC EDN STUMPY MEADOWS RESERVOIR (MARK EDSON DAM). Follows the logic in CS3_I_STMPY_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_STMPY')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/EDN_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # make sure none of the areas are above a maximum of 330
    df_area_capacity.loc[df_area_capacity['Area'] > 330, 'Area'] = 330

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [20.0001, 330]

    # calculate and set the evaporation
    df_storage_data['EDN_evap'] = calculate_evap_data(df_storage_data['EDN'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11429350_MFA001(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11429350 LOON LK NR MEEKS BAY CA. Follows the logic in CS3_I_MFA001_Rev2022G. This location has more data than when this reservoirs is used normally

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_LOONL')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11429350_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 1450
    df_area_capacity.loc[df_area_capacity['Area'] > 1450, 'Area'] = 1450

    # calculate and set the evaporation
    df_storage_data['11429350_MFA001_evap'] = calculate_evap_data(df_storage_data['11429350_MFA001'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11426170(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11426170 LAKE VALLEY RESERVOIR NEAR CISCO  CA. Follows the logic in CS3_I_LKVLY_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    # df_evap_rates = read_evap_data(s_dss_file, 'ER_LKVLY')
    df_evap_rates = pd.read_csv(r"./Inputs/modified_evap_rates.csv", index_col=0, parse_dates=True)[['LKVLY']]
    df_evap_rates.columns = ['IN']

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11426170_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 312
    df_area_capacity.loc[df_area_capacity['Area'] > 312, 'Area'] = 312

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [8.4, 312]

    # calculate and set the evaporation
    df_storage_data['11426170_evap'] = calculate_evap_data(df_storage_data['11426170'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11441000(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11441001 UNION VALLEY RES NR RIVERTON CA. Follows the logic in CS3_I_UNVLY_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_UNVLY')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11441001_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)


    # calculate and set the evaporation
    df_storage_data['11441001_evap'] = calculate_evap_data(df_storage_data['11441001'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)
