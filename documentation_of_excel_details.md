

MOK079



in sheet "Mokelumne FNF EBMUD Mok Hill"



"7/16-09/21 calculated values using C3 evaporation rates

For WY 1922-1927 calculated as FNF at Camanche minus I\_PARDE"

Stopping MOK079 for now, working on NHGAN, which is needed for PARDE and CMCHE, which feed into MOK079



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







NFM010



The SV Input at the end of Stantec's sheet is not exactly the same as the one in CS3\_SJR\_Read...xlsm. They differ in a few locations by 0.01.



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

