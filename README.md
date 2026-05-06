### CalSim Rim Inflow Extension

Python code to do an extension on the CalSim Rim Inflows.
Methods are the same as the previous Excel sheet methods. A few issues around multiple version of the same data from the sheets have been updated.


## To calculate the rim inflows

### To create an environment

`conda env create -f environment.yml`

`conda activate extension`

### To recreate the rim inflows with the data in the repository:

Run: `python calculate_rim_inflows.py`

The calculated flows will be in the *Outputs* folder in *rim_inflows.csv*.

### To do an extension:
1. Update any data that cannot be automatically pulled. Put this into the *Inputs* folder. You may need to add reading this data in to the code.
2. In *calculate_rim_inflows.py*, update `i_final_year` to the final water year to include.
3. Run `python calculate_rim_inflows.py`.

The calculated flows will be in the *Outputs* folder in *rim_inflows.csv*.

### To incorporate additional locations
Every location is different so the process to  incorporate a new location is going to look different every time. Generally, the following this must be added:
1. Any data from the previous extension should be added, in TAF, to *Inputs/2022_extension_data.csv*
2. Any USGS or CDEC stations should be added to *sl_usgs_stations* and *sl_cdec_stations* in *calculate_rim_inflows.py*
3. If any new reservoirs are needed, an evaporation function should be created in *evaporation_functions.py* and called in *calculate_rim_inflows.py*
4. If data needs to be unimpaired, a function should be created in *unimpairment_functions.py* and called in *calculate_rim_inflows.py*
5. If data needs to be extended, a call to *extend_data* should be added in *calculate_rim_inflows.py*
6. A final rim inflow function should be created in *rim_inflow_functions.py* and called in *calculate_rim_inflows.py*

## Reference Documentation
For more information on the methods used to calculate the rim inflows see chapter 5 of the CalSim 3 Hydrology Report on the [CalSim website](https://water.ca.gov/Library/Modeling-and-Analysis/Central-Valley-models-and-tools/CalSim-3).
Specific documentation for the transition to using Python is in the process of being created.