import pandas as pd

from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021
    print("done with imports")
    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # option to plot comparison
    b_compare_data = True
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

    # for COL003 (11319500), EBMUD is main historical gage (pre 2021) but NaNs are filled with CDEC MKM
    df_full_data['EBMUD_11319500']= flow_from_two_unimp(df_full_data['EBMUD_11319500'], df_full_data['MKM'], 1.0)

    # as a continuation of the previous operation the "filled out" EBMUD is now used as the historical
    # data for USGS 11319500. Then the filled out USGS 11319500 is used for s-curve on the COL003
    # gage, which is USGS 11315000
    if '11319500' not in df_full_data.columns:
        df_full_data['11319500'] = np.nan
    df_full_data['11319500'] = flow_from_two_unimp(df_full_data['11319500'], df_full_data['EBMUD_11319500'], 1.0)

    ### ----- for SLTSP -----
    ## we create Unimpaired Lower Bear and Salt Springs ('LBearSS')
    # there are two errors in the sheets. to reproduce the error, set b_make_errors_sltsp = True.
    # to do the calculation correctly, set b_make_errors_sltsp = False.
    b_make_errors_sltsp = True

    # but only when all three inputs exist (are not NaN).
    # first, create the column for our target flow, LBearSS.
    if 'LBearSS' not in df_full_data.columns:
        df_full_data['LBearSS'] = np.nan

    # second, create the 11315030 dataset, which includes a timeshifting error reproduced here
    # create a deep copy of 11315030 dataset
    df_11315030 = df_full_data[['11315030']].copy(deep=True)
# TODO Remove
#    print(df_11315030)
#    print(type(df_11315030))
    if(b_make_errors_sltsp):
        # create a copy of 11315030 timeshifted forward by 3 months to help reproduce an error in excel
        df_shifted_11315030 = df_full_data[['11315030']].copy(deep=True).shift(3)

    ## calculate the monthly averages of the correct 11315030 data
    # set a cutoff date so we can reproducte the monthly averages of the sheets
    cutoff = '2021-09-30'

    # create a cutoff copy of the data
    df_11315030_cutoff = df_11315030.loc[:cutoff]

    #count the number of non-NaN values per month
    df_counts_by_month = df_11315030_cutoff.groupby(df_11315030_cutoff.index.month).count()

    # sum of non‑NaN values for each month
    df_sums_by_month = df_11315030_cutoff.groupby(df_11315030_cutoff.index.month).sum()

    df_sums_by_month.columns = ['11315030']

    if(b_make_errors_sltsp):
        # this reproduces the error in CS3_I_SLTSP_Rev2022G.xlsm on sheet "Cole 11315030 in Cells W127 to AH127
        df_counts_by_month = df_counts_by_month - 6
    # find the average by diving the summed month value by the data count for that month
#    # convert to Series
#    ds_sums_by_month = df_sums_by_month[:, 0]
#    ds_counts_by_month = df_counts_by_month[:, 0]
    # if any counts are zero, put NaN in df_monthly_average
    df_monthly_average = df_sums_by_month.div(df_counts_by_month.replace(0, pd.NA))


    # Build a DataFrame of fill values based on each row's month. df_month_map has the same row index as
    # df_shifted_11315030 but with monthly averages for all months
    if(b_make_errors_sltsp):
        df_month_map = (
            df_shifted_11315030.index.to_frame(index=False)
            .set_index(df_shifted_11315030.index)
        )
    else:
        df_month_map = (
            df_11315030.index.to_frame(index=False)
            .set_index(df_11315030.index)
        )
    df_month_map['month'] = df_month_map.index.month

    df_fill_values = (
        df_month_map[['month']]
        .merge(df_monthly_average, left_on='month', right_index=True)
        .iloc[:, 1:]  # keep only the monthly-average column
    )
    if(b_make_errors_sltsp):
        df_fill_values.columns = df_shifted_11315030.columns  # match original column name
    else:
        df_fill_values.columns = df_11315030.columns  # match original column name

    # Fill NaNs
    if(b_make_errors_sltsp):
        df_filled_11315030 = df_shifted_11315030.fillna(df_fill_values)
    else:
        df_filled_11315030 = df_11315030.fillna(df_fill_values)
    df_filled_11315030.to_csv('./Intermediate/upper_mokelumne_11315030_wrong.csv')

    df_full_data['11315030'] = df_filled_11315030
    # Calculate storage differences for Salt Springs and Lower Bear
    
    # Combine flows
    sum_if_all_not_nan(df_full_data, 'LBearSS', ['11315900', '11314000', '11314500',
                                                 '11315030', 'SS_HIST_EVAP', 'LB_HIST_EVAP'])


    # save to csv
    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_gap_filled.csv')

    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs

    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_wevap.csv')

    ### unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows, round 1 ...")

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

    print("Calculating unimpaired flows, round 2...")
    df_unimpaired_data['11319500'] = unimpaired_11319500(df_full_data, df_extended_data)

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # prepare for s-curve disaggregation round 2, using second round unimpaired data

    # TODO REMOVE the dropping 1943 lines below (next 5 lines)
    # make a copy of 11319500 with 1943 dropped from it for use in extending data for 11315000
    # first create a list of the index of rows to drop
#    dl_rows_to_drop = df_unimpaired_data.loc['1942-10-31':'1943-09-30'].index
    # then drop those rows of the column named '11319500'
#    df_11319500_dropped = df_unimpaired_data['11319500'].drop(dl_rows_to_drop)

    # do s-curve disaggregation, using second round unimpaired data
    extend_data(df_unimpaired_data['11319500'], df_full_data['11315000'], \
                df_extended_data, df_synthetic_data, 1928, i_final_year, False, '11315000', i_x_start_year=1922, i_final_year=i_final_year, b_is_COL003=True)

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

    I_MFM008(df_full_data, df_rim_inflows)
    I_SFM005(df_extended_data, df_rim_inflows)
    I_COL003(df_extended_data, df_rim_inflows)

    df_rim_inflows.to_csv('./Outputs/upper_mokelumne_rim_inflows.csv')

    # Comparison with Previous Rim Inflow dataset
    if b_compare_data:

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
