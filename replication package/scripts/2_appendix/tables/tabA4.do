***********************************************
*
* Emotion and Reason in Political LanguageL: Replication Package
* Gennaro and Ash
* Table A4: Summary Statistics
*
***********************************************


* Working Directory
* Set the folder where to find the replication package
cd "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

global wd "./3 replication package/data/1_main_datasets"
cd "$wd"


* Upload the Data   ***********************************************

use dataset_tables.dta, clear


* Generate decades
egen decade = cut(speech_year), at(1858, 1868, 1878, 1888, 1898, 1908, 1918, 1928, /*
*/1938, 1948, 1958, 1968, 1978, 1988, 1998, 2008, 2016) icodes


* Summary statistics
bys decade: summarize score 

estpost tabstat score, by(decade) statistics(mean sd min max) columns(statistics)
esttab, cells("mean(fmt(%8.2f))" "sd(fmt(%8.2f))" "min(fmt(%8.2f))" "max(fmt(%8.2f))")

