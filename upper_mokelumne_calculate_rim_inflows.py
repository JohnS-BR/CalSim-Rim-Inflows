from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021

    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # option to plot comparison
    b_compareData = True
    s_prev_rim_inflows_fn = "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.xlsm" # file path and name must be provided to plot/calculate comparison
    s_prev_rim_inflow_sheet = "Inflows"

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_mokelumne_full_gauge_data.csv', index_col=0, parse_dates=True)

    # gap fill the data sets that need it. this gap fills the location with monthly averages
    # nothing needed yet

    # merge gages that need it. 

    # for COL003, EBMUD is main historical gage (pre 2021) but NaNs are filled with CDEC MKM
    df_full_data['EBMUD_11319500']= flow_from_two_unimp(df_full_data['EBMUD_11319500'], df_full_data['MKM'], 1.0)
    # as a continuation of the previous operation the "filled out" EBMUD is now used as the historical
    # data for USGS 11319500. Then the filled out USGS 11319500 is used for s-curve on the COL003
    # gage, which is USGS 11315000
    df_full_data['11319500'] = flow_from_two_unimp(df_full_data['11319500'], df_full_data['EBMUD_11319500'], 1.0)

    # save to csv
    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_gap_filled.csv')

    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs


    # calc_evap_folsom(s_evap_dss_path, df_full_data)
    # calc_evap_NAT(s_evap_dss_path, df_full_data)


    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_wevap.csv')

    ### unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows...")

    # TODO I don't understand what the following (commented out) line does
    # df_unimpaired_data['CalSim3'] = unimpaired_calsim3(df_full_data)

    # drop the first row which is only for calculating storage differences
    # TODO commented out following line because we are not yet unimparing anything.
    # bring this back in once we have an unimpared data set
    # df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    # TODO see previous TODO comment
    # df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # redistribute negatives
    # TODO see previous
    # df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)

    # save to csv
    #df_pos_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data_pos.csv')

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    print("Extending flows...")

    # extend all with the s-curve disaggregation, round 1
    extend_data(df_full_data['11317000'], df_full_data['11318500'], \
                df_extended_data, df_synthetic_data, 1934, i_final_year, False, '11318500', i_final_year=i_final_year)
      
    ### unimpairing the data for those that rely on previously s-curved data

    print("Calculating second round of unimpaired flows...")
    df_unimpaired_data['11319500'] = unimpaired_11319500(df_full_data, df_extended_data)
#    print("in calc rim, df_unimp 9500 around 6/1924 is", df_unimpaired_data.iloc[31:38]['11319500'])

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # extend with s-curve disaggregation, using second round unimpaired data
#    print("1in calc rim, df_full 5000 around 6/1924 is", df_full_data.iloc[31:38]['11315000'])

#TODO REMOVE    extend_data(df_unimpaired_data['11319500'], df_full_data.loc['1927-10-31':'2021-09-30','11315000'], \
#                df_extended_data, df_synthetic_data, 1928, i_final_year, True, '11315000', i_final_year=i_final_year)

    extend_data(df_unimpaired_data['11319500'], df_full_data['11315000'], \
                df_extended_data, df_synthetic_data, 1944, i_final_year, False, '11315000', i_final_year=i_final_year)

#    print("2in calc rim, df_extended 5000 around 6/1924 is", df_extended_data.iloc[31:38]['11315000'])
#    print("3in calc rim, df_synthetic 5000 around 6/1924 is", df_synthetic_data.iloc[31:38]['11315000'])

    df_synthetic_data['11315000'].to_csv('./Intermediate/upper_mokelumne_synthetic_11315000_data.csv')

    # copy synthetic data to extended data where extended data is NaN
    df_extended_data.fillna({'11315000': df_synthetic_data['11315000']}, inplace=True)

    # save to csv
    df_extended_data.to_csv('./Intermediate/upper_mokelumne_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/upper_mokelumne_synthetic_data.csv')

    df_lake_valley_watershed = calculate_watershed_factors("./Inputs/lake_valley_watershed.csv")

    # final rim inflows
    df_rim_inflows = pd.DataFrame()

    print("Calculating rim inflows...")
    # TODO add function calls to rim inflow functions here

    I_MFM008(df_full_data, df_rim_inflows)
    I_SFM005(df_extended_data, df_rim_inflows)
    I_COL003(df_extended_data, df_rim_inflows)

    df_rim_inflows.to_csv('./Outputs/upper_mokelumne_rim_inflows.csv')

    # Comparison with Previous Rim Inflow dataset
    if b_compareData:

        # read in data
        df_reference = pd.read_excel(s_prev_rim_inflows_fn, sheet_name=s_prev_rim_inflow_sheet, skiprows=[0,2,3,4,5,6,7,8,9,10,11],header=0, index_col=0, parse_dates=True)

        # calculate differences
        df_diffs = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows).max().to_frame('Max Difference')
        df_diffs['Median Value - Original'] = df_reference[df_rim_inflows.columns].mean()
        df_diffs['Max Percent Difference'] = (abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)).max() / df_reference[df_rim_inflows.columns].mean()*100

        print("Maximum differences:")
        print(df_diffs.sort_values(by='Max Difference', ascending=False).to_string())

        # TODO figure out the size of the two data frames df_rim_inflows and df_reference. 
        # currently df_rim_inflows is 1236 rows X 2 columms and
        # df_reference is 1200 rows x 81 columns
        # I think the row difference is the problem. It has to do with the years represented on each.
        print('Creating comparison plots...')

        # drop the first row of df rim inflows trimmed so it matches the reference
        df_rim_inflows.drop(index=df_rim_inflows.index[0], inplace=True)

        #trim our new inflows (from df_rim_inflows) to have the same number of rows as our reference
        i_targetLen=len(df_reference)
        df_rim_inflows_trimmed = df_rim_inflows.iloc[:i_targetLen].copy()

        create_rim_inflow_comparison_plots(df_rim_inflows_trimmed, df_reference)
