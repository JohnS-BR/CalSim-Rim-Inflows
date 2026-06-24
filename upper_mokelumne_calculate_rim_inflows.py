import pandas as pd

#from Examples.Example_SingleRimInflow_I_RCK001 import df_unimpaired_data
from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021
    print("done with imports")

    # --- Begin Flags ---
    # option to plot comparison
    b_compare_data = True

    # option to run each element using "upstream" (antecedent) SV INPUT values from sheets rather than from the values
    # calculated within the Python code.
    b_use_upstream_sv_inputs = True

    # this flag initiates two things. 1) It runs the upstream code up until we reach the inputs for the s-curve
    # disaggregation. It then checks the x watershed and y watershed against data in files that end in
    # "input_to_s_curve.csv".  2) It takes the s-curve from the sheets (found in files that end in
    # "output_from_s_curve.csv") and runs the code downstream of that point. It compares the final output to the
    # SV INPUT tab of the sheets (found in "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.xlsm").
    b_replicate_sheets = True

    # true on this b_reproduce_error_lbear_ss reproduces two errors in the sheets. 1) time shifts the monthly averages
    # relative to where they belong by 3 months to replicate sheet. 2) calculates monthly averages with an incorrect
    # denominator. The flag is set at the top of this document. Set this to false to run a more correct version of
    # I_SLTSP.
    b_reproduce_error_lbear_ss = True

    # --- End Flags

    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # file path and name must be provided to plot/calculate comparison and to use SV INPUTS from sheets as upstream
    # data
    s_prev_rim_inflows_fn = "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.xlsm"
    s_prev_rim_inflow_sheet = "Inflows"

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_mokelumne_full_gauge_data.csv', index_col=0, parse_dates=True)

    # read in upstream sheet SV INPUT sheet data
    if b_use_upstream_sv_inputs:
        # read in data
        df_sv_inputs = pd.read_excel(s_prev_rim_inflows_fn, sheet_name=s_prev_rim_inflow_sheet,
                                     skiprows=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], header=0, index_col=0,
                                     parse_dates=True)

    if b_replicate_sheets:
        # read in files that contain the sheet data from just before and just after the s-curve process, to isolate that
        # factor. The "after s" files are the data from the sheets after merging the synthetic output into the gaps in
        # the data.

        # create a list of lists. inner elements are ['column_name', 'path to before csv', 'path to after csv']
        ls_sheet_info = [['COL003', './Inputs/s_curve_replication/col003_input_to_s_curve.csv',
                          './Inputs/s_curve_replication/col003_output_from_s_curve.csv'],
                         ['SLTSP', './Inputs/s_curve_replication/sltsp_input_to_s_curve.csv',
                          './Inputs/s_curve_replication/sltsp_output_from_s_curve.csv'],
                         ['UBEAR', './Inputs/s_curve_replication/ubear_input_to_s_curve.csv',
                         './Inputs/s_curve_replication/ubear_output_from_s_curve.csv'],
                         ['NFM010', './Inputs/s_curve_replication/nfm010_input_to_s_curve.csv',
                         './Inputs/s_curve_replication/nfm010_output_from_s_curve.csv'],
                         ['TGC003', './Inputs/s_curve_replication/nfm010_input_to_s_curve.csv',
                         './Inputs/s_curve_replication/tgc003_output_from_s_curve.csv']
                         ]
        # create the dataframes where we keep the before and after data
        df_before_s = pd.DataFrame()
        df_after_s = pd.DataFrame()

        read_replication_data(ls_sheet_info, df_before_s, df_after_s)

    # gap fill the data sets that need it. this gap fills the location with monthly averages
    # nothing needed yet

    # merge gauges that need it.

    # -- begin COL003 merge --
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
    calc_evap_NHGAN(s_evap_dss_path, df_full_data)
    calc_evap_OHGAN(s_evap_dss_path, df_full_data)

    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_wevap.csv')

    # unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows, round 1 ...")

    # see the top of this doc for details on the lbear_ss errors.
    df_unimpaired_data['LBearSS_V1'] = unimpaired_lbear_salt_springs_fnf_v1(df_full_data,
                                            b_reproduce_error_lbear_ss=b_reproduce_error_lbear_ss)
    df_unimpaired_data['LBearSS_V2'] = unimpaired_lbear_salt_springs_fnf_v2(df_full_data,
                                            b_reproduce_error_lbear_ss=b_reproduce_error_lbear_ss)
    df_unimpaired_data['11309500'] = unimpaired_11309500(df_full_data)
    df_unimpaired_data['NF_SF_ITAS'] = unimpaired_NF_SF_ITAS(df_full_data)
    df_unimpaired_data['NH_DAM_RELEASE'] = unimpaired_NH_DAM_RELEASE(df_full_data)

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # redistribute negatives
    # not needed yet

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    if b_replicate_sheets:
        print("Checking inputs to s-curve, part 1...")
        # compare unrounded 11317000
        # TODO update. the next line should really be comparing the code's 11317000 (full data) to a sheet copied in from
        #  the scurve inputs of sheet SFM005
        compare_two_df(df_full_data['11317000'].drop(df_full_data['11317000'].index[0]), df_sv_inputs['I_MFM008'], '11317000',
                       'SV_INPUT_MFM008')
        # compare rounded 11317000
        compare_two_df(df_full_data['11317000'].drop(df_full_data['11317000'].index[0]).round(2), df_sv_inputs['I_MFM008'], '11317000',
                       'SV_INPUT_MFM008')

    print("Extending flows, part 1...")
    # extend with the s-curve disaggregation, round 1
    extend_data(df_full_data['11317000'], df_full_data['11318500'],
                df_extended_data, df_synthetic_data, 1934, i_final_year, False,
                '11318500', i_final_year=i_final_year)

    # unimpairing the data for those that rely on previously s-curved data
    print("Calculating unimpaired flows, round 2...")
    df_unimpaired_data['11319500'] = unimpaired_11319500(df_full_data, df_extended_data)
    df_unimpaired_data['11316600'] = unimpaired_11316600(df_full_data, df_extended_data, df_unimpaired_data)
    df_unimpaired_data['tiger_creek_conduit_accretions'] = unimpaired_tiger_creek_conduit_accretions(df_full_data,
                                                                                                     df_extended_data)
    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # extend with the s-curve disaggregation, round 2
    print("Extending flows, part 2...")

    if b_replicate_sheets:
        print("Checking inputs to s-curve, part 2...")
        compare_two_df(df_before_s['COL003'], df_unimpaired_data['11319500'], 'col003_before_s',
                       '11319500')
        compare_two_df(df_before_s['SLTSP'], df_unimpaired_data['11319500'], 'sltsp_before_s',
                       '11319500')

    extend_data(df_unimpaired_data['11319500'], df_full_data['11315000'],
               df_extended_data, df_synthetic_data, 1928, i_final_year, False,
               '11315000', i_x_start_year=1922, i_final_year=i_final_year, b_is_COL003=True)
    extend_data(df_unimpaired_data['11319500'], df_unimpaired_data['LBearSS_V1'],
               df_extended_data, df_synthetic_data, 1989, i_final_year, False,
               'LBearSS_V1', i_final_year=i_final_year)
    extend_data(df_unimpaired_data['11319500'], df_unimpaired_data['LBearSS_V2'],
                df_extended_data, df_synthetic_data, 1989, i_final_year, False,
                'LBearSS_V2', i_final_year=i_final_year)
    extend_data(df_unimpaired_data['11319500'], df_unimpaired_data['11316600'],
                df_extended_data, df_synthetic_data, 1986, i_y_end_year=2001,
                b_use_all_y_data=False, s_name='11316600', i_final_year=i_final_year)
# TODO remove seems to be unused by sheet
#    extend_data(df_unimpaired_data['11319500'], df_unimpaired_data['tiger_creek_conduit_accretions'],
#                df_extended_data, df_synthetic_data, 2002, i_y_end_year=i_final_year,
#                b_use_all_y_data=False, s_name='tiger_creek_conduit_accretions', i_final_year=i_final_year)

    # copy synthetic data to extended data where extended data is NaN for 11315000 and
    df_extended_data.fillna({'11315000': df_synthetic_data['11315000']}, inplace=True)
    df_extended_data.fillna({'11316600': df_synthetic_data['11316600']}, inplace=True)

    # save to csv
    df_extended_data.to_csv('./Intermediate/upper_mokelumne_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/upper_mokelumne_synthetic_data.csv')

    # final rim inflows
    df_rim_inflows = pd.DataFrame()

    print("Calculating rim inflows...")

    if b_replicate_sheets:
        I_MFM008(df_full_data, df_rim_inflows)
        I_SFM005(df_extended_data, df_rim_inflows)
        I_COL003(df_after_s[['COL003']].rename(columns={"COL003":"11315000"}), df_rim_inflows)
        I_SLTSP(df_after_s['SLTSP'], df_sv_inputs['I_COL003'], df_rim_inflows)
        I_UBEAR(df_after_s['UBEAR'], df_sv_inputs['I_COL003'], df_rim_inflows)
        I_NFM010(df_after_s['NFM010'], df_rim_inflows)
        I_TGC003(df_sv_inputs['I_NFM010'], df_rim_inflows)
        I_MOK079(df_full_data['11319500'], df_sv_inputs['I_NFM010'], df_sv_inputs['I_MFM008'],
                 df_sv_inputs['I_UBEAR'], df_sv_inputs['I_SLTSP'], df_sv_inputs['I_SFM005'],
                 df_sv_inputs['I_TGC003'], df_sv_inputs['I_COL003'], df_rim_inflows)
    else:
        I_MFM008(df_full_data, df_rim_inflows)
        I_SFM005(df_extended_data, df_rim_inflows)
        I_COL003(df_extended_data, df_rim_inflows)
        I_SLTSP(df_extended_data['LBearSS_V1'], df_extended_data['11315000'], df_rim_inflows)
        I_UBEAR(df_extended_data['LBearSS_V2'], df_extended_data['11315000'], df_rim_inflows)
        I_NFM010(df_extended_data['11316600'], df_rim_inflows)
        I_TGC003(df_rim_inflows['I_NFM010'], df_rim_inflows)
        I_MOK079(df_full_data['11319500'], df_rim_inflows['I_NFM010'], df_rim_inflows['I_MFM008'],
                 df_rim_inflows['I_UBEAR'], df_rim_inflows['I_SLTSP'], df_rim_inflows['I_SFM005'],
                 df_rim_inflows['I_TGC003'], df_rim_inflows['I_COL003'], df_rim_inflows)

    df_rim_inflows.to_csv('./Outputs/upper_mokelumne_rim_inflows.csv')

    # Comparison with Previous Rim Inflow dataset
    if b_compare_data:

        # read in data
        df_reference = pd.read_excel(s_prev_rim_inflows_fn, sheet_name=s_prev_rim_inflow_sheet, skiprows=[0,2,3,4,5,6,7,8,9,10,11],header=0, index_col=0, parse_dates=True)

        # calculate differences
        df_diffs = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows).max().to_frame('Max Difference')

        # Add the datetime where the max occurs per column
        df_diff = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)
        df_diffs['Date of Max Difference'] = df_diff.idxmax()

        df_diffs['Median Value - Original'] = df_reference[df_rim_inflows.columns].mean()
        df_diffs['Max Percent Difference'] = (abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)).max() / df_reference[df_rim_inflows.columns].mean()*100

        print("Maximum differences:")
        print(df_diffs.sort_values(by='Max Difference', ascending=False).to_string())

        print("Date of maximum differences:")
        print(df_diffs['Date of Max Difference'].to_string())

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
