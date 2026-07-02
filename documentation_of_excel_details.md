CMP014



USGS 11335000 UNIMP

&#x09;Same as JNKSN





JNKSN



MODELA - don't use WY55 in y data set, labeled as "impacted by dam"



USGS 11335000 UNIMP

&#x09;Does not use interpolated Dec 1965 Jenkinson storage. DIFFERENT from CMP001

&#x09;

CMP001



Export

&#x09;Source: At bottom of the table for USGS 11333000, Camp Creek near Somerset

&#x09;09/04-12/08 from reports to SWRCB, 01/09-09/21 CDEC CCN

JNKSN Storage

&#x09;Missing data: 12/65 - estimated by linear interpolation

&#x09;Storage began 1955

&#x09;01/55-09/55 estimate based on DWR unimpaired flow data from Cosumnes River at Michigan Bar

JNKSN Evaporation

&#x09;Area capacity table - the zero acre-feet elevation is labeled as "3,350 ft -- guess"



I\_JNKSN 

&#x09;This version differs from our CS3\_SJR\_ReadAllInflowDatatoDSS\_05.17.23 on the following dates:

&#x09;10/2012, 10/2015-09/2016, 10/2017, 10/2018-07/2019

&#x09;I have added the CMP001 version of this data into upper\_mokelumne\_2022\_sv\_inputs.csv

USGS 11335000 UNIMP

&#x09;Uses the interpolated Dec 1965 Jenkinson storage. DIFFERENT from JNKSN and CMP014



MOK079



in sheet "Mokelumne FNF EBMUD Mok Hill"



"7/16-09/21 calculated values using C3 evaporation rates

For WY 1922-1927 calculated as FNF at Camanche minus I\_PARDE"



Sheet Mokelumne 11319500: This data is different that the 11319500 used in COL003. It says on the README sheet that

it's the USGS data. The two data sets are quite different. This may be an area to improve.



I\_CMCHE sheet doesn't match SV INPUT I\_CMCHE. I don't see clues about where the MOD079 version comes from.



PARDE and CMCHE have a rounding difference because excel rounds down and pandas uses bankers rounding. This is the only difference.



NHGAN



Data sets:

USACE NH Release: USACE NEW HOGAN RESERVOIR RELEASE

&#x09;COE Data

&#x09;USACE data from Juricich old files

&#x09;10/09-09/15 from CDEC NHG

New Hogan Storage: NEW HOGAN DAM END OF MONTH STORAGE

&#x09;Note: Storage in New Hogan Reservoir began December 1963.

&#x09;USACE data from Juricich old files

Old Hogan Storage: OLD HOGAN END OF MONTH STORAGE

&#x09;Period of Record: 02/61-09/90 **<-** **WRONG, data from 1948 (WY'49) to 1962**

&#x09;Missing data: 10/62-09/63

&#x09;Source: DWR planning records

&#x09;Prior to 1949, no records were kept on the storage of Old Hogan Reservoir.

&#x09;Since there were no gates prior to 1949 with which to regulate Hogan Reservoir, the only effect

&#x09;on the runoff was a short-term delay in heavy flood runoff. Unimpaired runoff of the

&#x09;Calaveras River then was assumed to be the same as the measured flow.

&#x09;Old Hogan Reservoir was inundated in the fall of 1963. No records of Old Hogan storage

&#x09;operation could be found from November 1, 1962 to December 1963.

New Hogan Evaporation Rate

&#x09;Source: CS3\_ER\_NHGAN.xlsm

&#x09;NOTE TO SELF: used to calculate "New Hogan Evaporation" and "Old Hogan Evaporation"

NOTE: evaporation rate for old hogan and area capacity table is all from new hogan.



In sheet "Watershed" there is a calculation of total volume of precipitation from 1971-2000 on two watersheds to create a scaling factor. The watersheds are "USGS 11309500 Calaveras River at Jenny Lind" and "USGS 11308900 Calaveras River below New Hogan Dam"  It looks like the calculation was done in the early 2000s and then redone in 2020 by Sam Price, with almost no change to the watershed factor. John S is not sure how to reproduce or update this calculation (where to get the data, basically) so he's using the same watershed factor for now.



Blw Camanche FNF EBMUD: UNIMPAIRED USGS 11323500 MOKELUMNE R BW CAMANCHE DAM CA

&#x09;Source: UFDataset\_forSacWAM\_team.xlsx





NFM010



The SV Input at the end of Stantec's sheet is not exactly the same as the one in CS3\_SJR\_Read...xlsm. They differ in a few locations by 0.01. This is the source of the difference between the python and the excel.



COL003



added flag to extend\_data and s\_curve\_disaggreation called b\_is\_COL003.

this flag makes monthly average go from 1944 to present (x watershed),

even though we have data from 1922 - present. but because we're missing 1943, that's how the sheet did

the monthly data.



The s-curve is run for x watershed from 1922 to present, but using the monthly averages from 1944 to present.



1943 in y watershed is filled manually from the synthetic data after the scurve process.



SLTSP



&#x20;# true on this b\_reproduce\_error\_lbear\_ss reproduces two errors in the sheets. 1) time shifts the monthly averages

&#x20;   # relative to where they belong by 3 months to replicate sheet. 2) calculates monthly averages with an incorrect

&#x20;   # denominator. The flag is set at the top of this document. Set this to false to run a more correct version of

&#x20;   # I\_SLTSP.



UBEAR and SLTSP use different versions of Lower Bear Salt Springs FNF. TODO clarify difference.

