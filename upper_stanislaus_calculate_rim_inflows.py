from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021

    # this reproduces various errors found in the workbooks
    b_reproduce_errors = True
        # error 1: in LYONS,should be identical to MODELA tab in SFS030 BUT, even though it says "Run then replace Feb-
        # Sep 1940 with historical data" the 2022F version of the sheet does not have the data replaced with historical data.
        # error 2: Spicer Meadows Evaporation rate is from CS3_ER_SPICE_REV1.xlsm rather than the most recent evap rate.
    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # option to plot comparison
    b_compareData = True
    s_prev_rim_inflows_fn = "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.csv" # file path and name must be provided to plot/calculate comparison
    s_prev_rim_inflow_sheet = "Inflows"

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_stanislaus_full_gauge_data.csv', index_col=0, parse_dates=True)

    # gap fill the data sets that need it

    # save to csv
    df_full_data.to_csv('./Intermediate/upper_stanislaus_full_gauge_data_gap_filled.csv')

    # fill storage with monthly averages
    df_full_data['11295900_filled'] = fill_monthly_storage(df_full_data[['11295900']], i_start_year=1980, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=True, b_round=True)            # see PCRST and SFS033
    df_full_data['11297700_filled'] = fill_monthly_storage(df_full_data[['11297700']], i_start_year=1980, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=True, b_round=False)            # see LYONS
    df_full_data['11293460_filled'] = fill_monthly_storage(df_full_data[['11293460']], i_start_year=1980, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=False, b_round=True)           # see NFS033
    df_full_data['11293350_filled'] = fill_monthly_storage_w_middle_gap(df_full_data[['11293350']], 1980,
            10, 2006, 9, 2010, 10, i_final_year, 9, False , b_round=True)  # see NFS033
    df_full_data['11293370_filled'] = fill_monthly_storage(df_full_data[['11293370']], i_start_year=1980, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=False, b_round=True)            # see NFS033

    # set pre-1930 Lyons Storage (1129770_filled) to zero, see LYONS
    df_full_data.loc[df_full_data.index < pd.Timestamp("1930-01-01"), '11297700_filled'] = 0

    # set Spicer Meadow storage before Feb 1989 to (filled) Alpine Storage times a factor. See NFS033
    df_full_data['11293770_filled'] = np.nan
    df_full_data.loc[df_full_data.index < pd.Timestamp("1989-02-28"), '11293770_filled'] =  \
        df_full_data.loc[df_full_data.index < pd.Timestamp("1989-02-28"), '11293460_filled'] * (4062/4231)
    # set Spicer Meadow storage after (and including) Feb 1989 to its own data. See NFS033
    df_full_data.loc[df_full_data.index >= pd.Timestamp("1989-02-28"), '11293770_filled'] =  \
        df_full_data.loc[df_full_data.index >= pd.Timestamp("1989-02-28"), '11293770']


    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs
    calc_evap_11295900(s_evap_dss_path, df_full_data)                                                   # see SFS033
    calc_evap_11297700(s_evap_dss_path, df_full_data)                                                   # see SFS030
    calc_evap_11293460(s_evap_dss_path, df_full_data, b_reproduce_errors)                               # see NFS033
    calc_evap_11293350(s_evap_dss_path, df_full_data, b_reproduce_errors)                               # see NFS033
    calc_evap_11293370(s_evap_dss_path, df_full_data, b_reproduce_errors)                               # see NFS033
    calc_evap_11293770(s_evap_dss_path, df_full_data, b_reproduce_errors)                               # see NFS033

    df_full_data.to_csv('./Intermediate/upper_stanislaus_full_gauge_data_wevap.csv')

    ### unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows...")

    df_unimpaired_data['11296500'] = unimpaired_11296500(df_full_data)                                  # see SFS033
    df_unimpaired_data['11298000'] = unimpaired_11298000(df_full_data)                                  # see SFS030
    df_unimpaired_data['11293600'] = unimpaired_11293600(df_full_data)                                  # see NFS033
    df_unimpaired_data['11294500'] = unimpaired_11294500(df_full_data)                                  # see NFS033

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_stanislaus_unimpaired_data.csv')

    # redistribute negatives
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)

    # save to csv
    df_pos_unimpaired_data.to_csv('./Intermediate/upper_stanislaus_unimpaired_data_pos.csv')

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    print("Extending flows...")

    # extend all with the s-curve disaggregation
    extend_data(df_full_data['SNS'], df_unimpaired_data['11296500'],
                df_extended_data, df_synthetic_data, 1939, i_final_year, False,
                '11296500', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see SFS033
    extend_data(df_full_data['SNS'], df_unimpaired_data['11298000'],
                df_extended_data, df_synthetic_data, 1941, i_final_year, False,
                '11298000', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see SFS030
    if b_reproduce_errors:
        df_extended_data['11298000_v2'] = df_extended_data['11298000']
    df_extended_data.loc['02-28-1940':'09-30-1940', '11298000'] = (
                df_unimpaired_data.loc)['02-28-1940':'09-30-1940', '11298000']                          # see SFS030
    extend_data(df_full_data['SNS'], df_unimpaired_data['11294500'],
                df_extended_data, df_synthetic_data, 1929, i_final_year, False,
                '11294500', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see NFS033
    # replace extended data in 11294500 from WY 1922-1925 with observed data. See NFS033
    df_extended_data.loc[:'09-30-1925', '11294500'] = (df_unimpaired_data.loc)[:'09-30-1925', '11294500'] # see NFS033

    extend_data(df_extended_data['11294500'], df_unimpaired_data['11293600'],
                df_extended_data, df_synthetic_data, 1953, i_final_year, False,
                '11293600', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see NFS033

    # save to csv
    df_extended_data.to_csv('./Intermediate/upper_stanislaus_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/upper_stanislaus_synthetic_data.csv')

    df_lake_valley_watershed = calculate_watershed_factors("./Inputs/lake_valley_watershed.csv")

    # final rim inflows
    df_rim_inflows = pd.DataFrame()

    print("Calculating rim inflows...")

    I_SFS033(df_extended_data[['11296500']], df_rim_inflows)
    I_PCRST(df_extended_data[['11296500']], df_rim_inflows)
    I_SFS030(df_extended_data[['11298000']], df_rim_inflows[['I_SFS033']], df_rim_inflows[['I_PCRST']], df_rim_inflows)
    if b_reproduce_errors:
        I_LYONS(df_extended_data[['11298000_v2']], df_rim_inflows[['I_SFS033']], df_rim_inflows[['I_PCRST']],
                df_rim_inflows[['I_SFS030']], df_rim_inflows)
    else:
        I_LYONS(df_extended_data[['11298000']], df_rim_inflows[['I_SFS033']], df_rim_inflows[['I_PCRST']],
            df_rim_inflows[['I_SFS030']], df_rim_inflows)
    I_NFS033(df_extended_data[['11293600']], df_rim_inflows)
    df_rim_inflows.to_csv('./Outputs/upper_stanislaus_rim_inflows.csv')

    # Comparison with Previous Rim Inflow dataset
    if b_compareData:

        # Notes on replication
        print("The NFS033 replication differs in two months, Aug and Sept 1924, due to an s-curve bug in Excel with")
        print("negative flows at the end of the year.")

        # read in data
        df_reference = pd.read_csv(s_prev_rim_inflows_fn, index_col=0, parse_dates=True)

        # calculate differences
        df_diffs = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows).max().to_frame('Max Difference')

        # calculate percentile errors: the value of error that X% of the data is better than.
        # 1) Absolute differences per column
        diff_abs = (df_reference[df_rim_inflows.columns] - df_rim_inflows).abs()

        # 2) Choose percentiles you want (expressed as proportions)
        percentiles = [0.50, 0.90, 0.95, 0.99]

        # 3) Compute percentiles per column and give nice column names
        q_abs = diff_abs.quantile(percentiles).T
        q_abs.columns = [f'P{int(p * 100)} Abs Diff' for p in percentiles]

        # 4) Combine with your existing "Max Difference" table
        df_diffs = diff_abs.max().to_frame('Max Difference').join(q_abs)

        df_diffs.head()

        # Add the datetime where the max occurs per column
        df_diff = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)
        df_diffs['Date of Max Difference'] = df_diff.idxmax()

        # --- Max Percent Difference computed at the max-diff timestamp per column ---
        # Prepare matrices for fast, aligned lookup
        df_ref_cols = df_reference[df_rim_inflows.columns]
        df_rim_cols = df_rim_inflows[df_rim_inflows.columns]

        # Map each column to the integer row index of its "Date of Max Difference"
        row_idx = df_ref_cols.index.get_indexer(df_diffs['Date of Max Difference'])
        col_idx = np.arange(len(df_rim_inflows.columns))

        # Extract values from each column at its own max-diff row
        ref_vals = df_ref_cols.to_numpy()[row_idx, col_idx]
        rim_vals = df_rim_cols.to_numpy()[row_idx, col_idx]

        # Percent difference: |rim - ref| / ref * 100 (guard against divide-by-zero)
        with np.errstate(divide='ignore', invalid='ignore'):
            pct_vals = np.where(ref_vals != 0, np.abs(rim_vals - ref_vals) / ref_vals * 100, np.nan)

        df_diffs['Max Percent Difference'] = pct_vals
        # -------------------------------------------------------------------------------

        # calculate RMSE
        df_rmse = np.sqrt(((df_reference[df_rim_inflows.columns] - df_rim_inflows) ** 2).mean()).to_frame("RMSE")
        df_diffs = df_diffs.join(df_rmse)

        # format output
        cols_to_format = ["Max Difference", "P50 Abs Diff", "P90 Abs Diff", "P95 Abs Diff", "P99 Abs Diff",
                          "Max Percent Difference", "RMSE"]

        df_diffs[cols_to_format] = df_diffs[cols_to_format].apply(
            lambda s: s.map(lambda v: f"{v:.6f}")
        )

        # space out column headers
        df_diffs.columns = [col + "   " for col in df_diffs.columns]

        # print the analysis table
        print(df_diffs.sort_values(by='Max Difference   ', ascending=False).to_string())

        print('Creating comparison plots...')

        # Drop the first row of df_rim_inflows if its index month is September (month == 9) to match df_reference
        if df_rim_inflows.index[0].month == 9:
            df_rim_inflows = df_rim_inflows.iloc[1:]

        #trim our new inflows (from df_rim_inflows) to have the same number of rows as our reference
        i_targetLen=len(df_reference)
        df_rim_inflows_trimmed = df_rim_inflows.iloc[:i_targetLen].copy()

        create_rim_inflow_comparison_plots(df_rim_inflows_trimmed, df_reference)