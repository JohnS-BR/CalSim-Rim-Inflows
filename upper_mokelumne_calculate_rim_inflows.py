import pandas as pd

#from Examples.Example_SingleRimInflow_I_RCK001 import df_unimpaired_data
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

    # option to run current operation with "given" SV INPUT values from sheets rather than from internally
    # calculated values
    b_use_upstream_sheets = True

    s_prev_rim_inflows_fn = "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.xlsm" # file path and name must be provided to plot/calculate comparison
    s_prev_rim_inflow_sheet = "Inflows"

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_mokelumne_full_gauge_data.csv', index_col=0, parse_dates=True)

    # read in upstream sheet SV INPUT sheet data
    if b_use_upstream_sheets:
        s_upstream_sheets_path = r".\Inputs\upper_mokelumne_2022_sv_inputs.csv"

        # read the CSV
        df_upstream_sheets = pd.read_csv(s_upstream_sheets_path, index_col=0, parse_dates=True)

        # set -901 to nan
        df_upstream_sheets.replace(-901, np.nan, inplace=True)

    # gap fill the data sets that need it. this gap fills the location with monthly averages
    # nothing needed yet

    # merge gauges that need it.

    # -- start COL003 merge --
    # with COL003 (11319500), EBMUD is main historical gage (pre 2021) but NaN's are filled with CDEC MKM
    df_full_data['EBMUD_11319500']= flow_from_two_unimp(df_full_data['EBMUD_11319500'], df_full_data['MKM'], 1.0)

    # as a continuation of the previous operation the "filled out" EBMUD is now used as the historical
    # data for USGS 11319500. Then the filled out USGS 11319500 is used for s-curve on the COL003
    # gage, which is USGS 11315000
    if '11319500' not in df_full_data.columns:
        df_full_data['11319500'] = np.nan
    df_full_data['11319500'] = flow_from_two_unimp(df_full_data['11319500'], df_full_data['EBMUD_11319500'], 1.0)
    # -- end COL003 merge --

    # save to csv
    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_gap_filled.csv')

    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs
    # nothing needed yet

    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_wevap.csv')

    # unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows, round 1 ...")

    df_unimpaired_data['LBearSS'] = unimpaired_lbear_salt_springs_fnf(df_full_data, b_reproduce_error_lbear_ss=True)

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # redistribute negatives
    # not needed yet

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    print("Extending flows, part 1...")

    # extend with the s-curve disaggregation, round 1
    extend_data(df_full_data['11317000'], df_full_data['11318500'],
                df_extended_data, df_synthetic_data, 1934, i_final_year, False,
                '11318500', i_final_year=i_final_year, b_new_method_no_loop=False, b_run_loop=False)
      
    # unimpairing the data for those that rely on previously s-curved data
    print("Calculating unimpaired flows, round 2...")
    df_unimpaired_data['11319500'] = unimpaired_11319500(df_full_data, df_extended_data)
    df_unimpaired_data['11316600'] = unimpaired_11316600(df_full_data, df_extended_data, df_unimpaired_data)
    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # extend with the s-curve disaggregation, round 2
    print("Extending flows, part 2...")
    # TODO remove comment marks on 10 lines below
    extend_data(df_unimpaired_data['11319500'], df_full_data['11315000'],
               df_extended_data, df_synthetic_data, 1928, i_final_year, False,
               '11315000', i_x_start_year=1922, i_final_year=i_final_year, b_is_COL003=True,
                b_new_method_no_loop=True, b_run_loop=False)
    extend_data(df_unimpaired_data['11319500'], df_unimpaired_data['LBearSS'],
               df_extended_data, df_synthetic_data, 1989, i_final_year, False,
               'LBearSS', i_final_year=i_final_year)
    extend_data(df_unimpaired_data['11319500'], df_unimpaired_data['11316600'],
                df_extended_data, df_synthetic_data, 1986, i_y_end_year=2001,
                b_use_all_y_data=False, s_name='11316600', i_final_year=i_final_year)

    # copy synthetic data to extended data where extended data is NaN for 11315000 and
    df_extended_data.fillna({'11315000': df_synthetic_data['11315000']}, inplace=True)
    df_extended_data.fillna({'11316600': df_synthetic_data['11316600']}, inplace=True)

    # save to csv
    df_extended_data.to_csv('./Intermediate/upper_mokelumne_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/upper_mokelumne_synthetic_data.csv')

    # final rim inflows
    df_rim_inflows = pd.DataFrame()

    print("Calculating rim inflows...")

    I_MFM008(df_full_data, df_rim_inflows)
    I_SFM005(df_extended_data, df_rim_inflows)
    I_COL003(df_extended_data, df_rim_inflows)
    I_SLTSP(df_extended_data, df_rim_inflows)
    I_UBEAR(df_extended_data, df_rim_inflows)
    I_NFM010(df_extended_data, df_rim_inflows)

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
        # currently df_rim_inflows is 1236 rows X 2 columns and
        # df_reference is 1200 rows x 81 columns
        # I think the row difference is the problem. It has to do with the years represented on each.
        print('Creating comparison plots...')

        # drop the first row of df rim inflows trimmed so it matches the reference
        df_rim_inflows.drop(index=df_rim_inflows.index[0], inplace=True)

        #trim our new inflows (from df_rim_inflows) to have the same number of rows as our reference
        i_targetLen=len(df_reference)
        df_rim_inflows_trimmed = df_rim_inflows.iloc[:i_targetLen].copy()

        create_rim_inflow_comparison_plots(df_rim_inflows_trimmed, df_reference)
