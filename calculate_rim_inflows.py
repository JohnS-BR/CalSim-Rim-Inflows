import os

import pandas as pd

from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021

    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # this holds the USGS data (sometimes gap filled) from the previous extension
    s_previous_data = r".\Inputs\2022_extension_data.csv"

    # USGS stations to pull data for
    sl_usgs_stations = ['11427500', '11427400', '11427200', '11427700', '11427750', '11427760', '11439501', '11434500', '11436950', '11435900', '11434900', '11428000', '11427940', '11428400',
                        '11428300', '11428800', '11428700', '11428600', '11433060', '11433080', '11429500', '11429340', '11429350', '11430000', '11429300', '11429600', '11419340', '11433040',
                        '11432000', '11433100', '11433260', '11433300', '11433500', '11435100', '11437000', '11436999', '11437500', '11436000', '11426190', '11426170', '11427000', '11426500']
    sl_cdec_stations = ['AMF', 'EDN']
    sl_other_stations = ['YB236']

    # time range to pull USGS data for
    s_start_date = '2021-10-01'
    s_end_date = '2024-09-30'

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # pull USGS data
    df_usgs_data_original, df_usgs_data_monthly_taf = pull_usgs_data(sl_usgs_stations, s_start_date, s_end_date)

    # pull the cdec data
    df_cdec_data_original, df_cdec_data_monthly_taf = pull_cdec_data(sl_cdec_stations, s_start_date, s_end_date)

    # combine all the gauge data
    df_gauge_data_original = pd.merge(df_usgs_data_original, df_cdec_data_original, how='outer', left_index=True, right_index=True)
    df_gauge_data_monthly_taf = pd.merge(df_usgs_data_monthly_taf, df_cdec_data_monthly_taf, how='outer', left_index=True, right_index=True)

    # save to csvs
    df_gauge_data_original.to_csv('./Intermediate/gauge_data_original.csv')
    df_gauge_data_monthly_taf.to_csv('./Intermediate/gauge_data_monthly_taf.csv')

    # combine the new data with the previous data
    df_full_data = read_previous_data(s_previous_data, df_gauge_data_monthly_taf)

    # save to a csv
    df_full_data.to_csv('./Intermediate/full_gauge_data.csv')

    # calculate the evaporation amounts for all of our reservoirs
    # calculate_evap_multiple(df_full_data, c_reservoirs, s_evap_dss_path)
    calc_evap_11427400(s_evap_dss_path, df_full_data)
    calc_evap_11436950(s_evap_dss_path, df_full_data)
    calc_evap_11435900(s_evap_dss_path, df_full_data)
    calc_evap_11434900(s_evap_dss_path, df_full_data)
    calc_evap_11428700(s_evap_dss_path, df_full_data)
    calc_evap_11429350(s_evap_dss_path, df_full_data)
    calc_evap_11429600(s_evap_dss_path, df_full_data)
    calc_evap_EDN(s_evap_dss_path, df_full_data)
    calc_evap_11429350_MFA001(s_evap_dss_path, df_full_data)
    calc_evap_11426170(s_evap_dss_path, df_full_data)


    df_full_data.to_csv('./Intermediate/full_gauge_data_wevap.csv')

    ### unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    df_unimpaired_data['11439501'] = unimpaired_11439501(df_full_data)
    df_unimpaired_data['11427500'] = unimpaired_11427500(df_full_data)
    df_unimpaired_data['11427760'] = unimpaired_11427760(df_full_data)
    df_unimpaired_data['11428000'] = unimpaired_11428000(df_full_data)
    df_unimpaired_data['11428400'] = unimpaired_11428400(df_full_data)
    df_unimpaired_data['11428800'] = unimpaired_11428800(df_full_data)
    df_unimpaired_data['11429500'] = unimpaired_11429500(df_full_data)
    df_unimpaired_data['11430000'] = unimpaired_11430000(df_full_data)
    df_unimpaired_data['11433040'] = unimpaired_11419340(df_full_data)
    df_unimpaired_data['11433100'] = unimpaired_11433100(df_full_data)
    df_unimpaired_data['11433300'] = unimpaired_11433300(df_full_data)
    df_unimpaired_data['11433500'] = unimpaired_11433500(df_full_data)
    df_unimpaired_data[['11435100', '11435100_ALT']] = unimpaired_11435100(df_full_data)
    df_unimpaired_data['11437000'] = unimpaired_11437000(df_full_data)
    df_unimpaired_data['11436000'] = unimpaired_11436000(df_full_data)
    df_unimpaired_data['11426190'] = unimpaired_11426190(df_full_data)
    df_unimpaired_data['11427000'] = unimpaired_11427000(df_full_data)
    df_unimpaired_data['11426500'] = unimpaired_11426500(df_full_data)

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/unimpaired_data.csv')

    # redistribute negatives
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)

    # save to csv
    df_pos_unimpaired_data.to_csv('./Intermediate/unimpaired_data_pos.csv')

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    # extend all with the s-curve disaggregation
    extend_data(df_full_data['AMF'], df_pos_unimpaired_data['11439501'], df_extended_data, df_synthetic_data, 1923, i_final_year, False, '11439501', i_final_year)
    extend_data(df_extended_data['11439501'], df_full_data['11427700'], df_extended_data, df_synthetic_data, 1961, i_final_year, False, '11427700', i_final_year)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11427500'], df_extended_data, df_synthetic_data, 1966, 2007,True, '11427500', i_final_year)
    extend_data(df_full_data['11439501_ALTERED'], df_pos_unimpaired_data['11427500'], df_extended_data, df_synthetic_data, 1966, 2007,True, '11427500_ALTERED', 2021)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11427760'], df_extended_data, df_synthetic_data, 1966, 2007, False, '11427760', i_final_year)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11428000'], df_extended_data, df_synthetic_data, 1957, 1986, False, '11428000', i_final_year)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11428400'], df_extended_data, df_synthetic_data, 1991, 2015, False, '11428400', i_final_year)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11428800'], df_extended_data, df_synthetic_data, 1966, 2007, True, '11428800', i_final_year)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11429500'], df_extended_data, df_synthetic_data, 1963, i_final_year, False, '11429500', i_final_year)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11430000'], df_extended_data, df_synthetic_data, 1963, 2021, False, '11430000', i_final_year)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11433040'], df_extended_data, df_synthetic_data, 1962, 2017, True, '11433040', i_final_year)
    extend_data(df_full_data['11439501_ALTERED'], df_unimpaired_data['11433040'], df_extended_data, df_synthetic_data, 1962, 2017, True, '11433040_ALTERED', 2021)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11433100'], df_extended_data, df_synthetic_data, 1967, 1992, False, '11433100', i_final_year)
    extend_data(df_full_data['AMF'], df_unimpaired_data['11433100'], df_extended_data, df_synthetic_data, 1967, 1992, False, '11433100_AMF', i_final_year)
    extend_data(df_extended_data['11439501'], df_full_data['11433260'], df_extended_data, df_synthetic_data, 1966, 1985, False, '11433260', i_final_year)
    extend_data(df_full_data['AMF'], df_pos_unimpaired_data['11433300'], df_extended_data, df_synthetic_data, 1959, i_final_year, False, '11433300', i_final_year)
    df_extended_data['11433500'] = flow_from_two_unimp(df_unimpaired_data['11433500'], df_unimpaired_data['11433300'], 1.06)
    extend_data(df_full_data['AMF'], df_unimpaired_data['11435100_ALT'][~df_unimpaired_data.index.isin(pd.date_range(datetime(2002, 10, 31), datetime(2012, 9, 30)))], df_extended_data, df_synthetic_data, 1971, 2002, True, '11435100_C', i_final_year)
    extend_data(df_full_data['AMF'], df_unimpaired_data['11435100'].loc[datetime(2011, 9, 30):], df_extended_data, df_synthetic_data, 2012, 2021, False, '11435100_A', i_final_year)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11435100'].loc[datetime(2011, 9, 30):], df_extended_data, df_synthetic_data, 2012, 2021, False, '11435100_B', i_final_year)
    extend_data(df_full_data['AMF'], df_pos_unimpaired_data['11437000'], df_extended_data, df_synthetic_data, 1923, 1992, True, '11437000_A', i_final_year)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11437000'], df_extended_data, df_synthetic_data, 1923, 1992, False, '11437000_B', i_final_year)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11436000'], df_extended_data, df_synthetic_data, 1923, i_final_year, False, '11436000', i_final_year)

    # save to csv
    df_extended_data.to_csv('./Intermediate/extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/synthetic_data.csv')

    df_lake_valley_watershed = calculate_watershed_factors("./Inputs/lake_valley_watershed.csv")

    # final rim inflows
    df_rim_inflows = pd.DataFrame()

    I_DCC010(df_extended_data, df_rim_inflows)
    I_FRMDW(df_extended_data, df_rim_inflows)
    I_MFA036(df_extended_data, df_rim_inflows)
    I_RUB047(df_extended_data, df_rim_inflows)
    I_LRB004(df_extended_data, df_rim_inflows)
    I_HHOLE(df_extended_data, df_rim_inflows)
    I_LOONL(df_extended_data, df_rim_inflows)
    I_SFR006(df_extended_data, df_rim_inflows)
    I_GERLE(df_extended_data, df_rim_inflows)
    I_STMPY(df_extended_data, df_rim_inflows)
    I_PLC007(df_extended_data, df_rim_inflows)
    I_NLC003(df_extended_data, df_full_data, df_rim_inflows)
    I_SLC003(df_extended_data, df_full_data, df_rim_inflows)
    I_LNG012(df_extended_data, df_rim_inflows)
    I_RUB002(df_extended_data, df_rim_inflows)
    I_NMA003(df_extended_data, df_rim_inflows)
    I_MFA025(df_extended_data, df_rim_inflows)
    I_MFA023(df_extended_data, df_rim_inflows)
    I_MFA001(df_extended_data, df_rim_inflows)
    I_ALOHA(df_extended_data, df_rim_inflows)
    I_PYR001(df_extended_data, df_rim_inflows)
    I_CAPLS(df_extended_data, df_rim_inflows)
    I_SILVR(df_extended_data, df_rim_inflows)
    I_LKVLY(df_unimpaired_data, df_full_data, df_rim_inflows, df_lake_valley_watershed)
    I_NNA013(df_unimpaired_data, df_full_data, df_rim_inflows, df_lake_valley_watershed)
    I_NFA054(df_unimpaired_data, df_rim_inflows, df_lake_valley_watershed)
    I_CYN009(df_unimpaired_data, df_rim_inflows, df_lake_valley_watershed)
    I_NFA022(df_unimpaired_data, df_rim_inflows)
    I_NFA016(df_rim_inflows)
    I_SFA066(df_extended_data, df_rim_inflows)
    I_SFA076(df_rim_inflows)

    df_rim_inflows.to_csv('./Outputs/rim_inflows.csv')
