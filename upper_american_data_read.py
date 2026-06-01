from extension_functions import *


if __name__ == "__main__":

    # this file reads in the upper american USGS and CDEC data amd combines it with the previous data

    # this holds the USGS data (sometimes gap filled) from the previous extension
    s_previous_data = r".\Inputs\2022_extension_data.csv"

    # USGS stations to pull data for
    sl_usgs_stations = ['11427500', '11427400', '11427200', '11427700', '11427750', '11427760', '11439501', '11434500',
                        '11436950', '11435900', '11434900', '11428000', '11427940', '11428400', '11428300', '11428800',
                        '11428700', '11428600', '11433060', '11433080', '11429500', '11429340', '11429350', '11430000',
                        '11429300', '11429600', '11419340', '11433040', '11432000', '11433100', '11433260', '11433300',
                        '11433500', '11435100', '11437000', '11436999', '11437500', '11436000', '11426190', '11426170',
                        '11427000', '11426500', '11440000', '11440500', '11441000', '11441002', '11441001', '11440900',
                        '11429300', '11441500', '11441100', '11442000', '11443500', '11443460', '11443450', '11444500',
                        '11443501', '11444201', '11444280', '11446000', '11446500', '11425416', '11433930']
    sl_cdec_stations = ['AMF', 'EDN', 'NAT', 'BEV']
    sl_other_stations = ['YB236', 'El Dorado', 'PCWA Pump Station', 'EID Diversions', 'Folsom Diversions',
                         'Folsom South Canal', 'Folsom', 'YB90', 'YB91', 'Folsom Fair Oaks']

    # time range to pull USGS data for
    s_start_date = '2021-10-01'
    s_end_date = '2024-09-30'

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)

    # pull USGS data
    df_usgs_data_original, df_usgs_data_monthly_taf = pull_usgs_data(sl_usgs_stations, s_start_date, s_end_date)

    # pull the cdec data
    df_cdec_data_original, df_cdec_data_monthly_taf = pull_cdec_data(sl_cdec_stations, s_start_date, s_end_date)

    # combine all the gauge data
    df_gauge_data_original = pd.merge(df_usgs_data_original, df_cdec_data_original, how='outer', left_index=True,
                                      right_index=True)
    df_gauge_data_monthly_taf = pd.merge(df_usgs_data_monthly_taf, df_cdec_data_monthly_taf, how='outer',
                                         left_index=True, right_index=True)

    df_gauge_data_monthly_taf.rename(columns={'BEV': 'YB90'}, inplace=True)

    # save to csvs
    df_gauge_data_original.to_csv('./Intermediate/gauge_data_original.csv')
    df_gauge_data_monthly_taf.to_csv('./Intermediate/gauge_data_monthly_taf.csv')

    # combine the new data with the previous data
    df_full_data = read_previous_data(s_previous_data, df_gauge_data_monthly_taf)
    # save to a csv
    df_full_data.to_csv('./Intermediate/full_gauge_data.csv')