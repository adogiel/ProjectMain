*******************************************************************
*
* Emotion and Reason in Political LanguageL: Replication Package
* Gennaro and Ash
* Table A9
*
*******************************************************************

* Working Directory   *********************************************


* Set the folder where to find the replication package
cd "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

global wd "./3 replication package/data/1_main_datasets"
cd "$wd"

* Upload the Data   ***********************************************

use dataset_tables.dta, clear


* Upload the Data
use dataset_tables.dta, clear


* Subset
keep if democrat==1 | republican==1

* Deal with missing values: replace with a missing dummy
replace topic1_new=1000 if topic1_new==.

local vars "female black asian hispanic catholic jewish"
foreach v in `vars'{
	gen miss_`v' = `v'==.
    replace `v'=0 if `v' ==.
}


gen dw2 = nominate_dim1^2
egen dw2_s = std(dw2)

gen loglength = log(length)

* Opposition      ***********************************************


est clear

eststo m1: reghdfe scorestd minor, absorb(chamberyearfe) cluster(speakerfe)
eststo m2: reghdfe scorestd minor, absorb(chamberyearfe topic1_new) cluster(speakerfe)
eststo m3: reghdfe scorestd minor, absorb(topic1_new chamberyearfe speakerfe) cluster(speakerfe)
eststo m4: reghdfe scorestd minor divided_govt, absorb(topic1_new chamberyearfe speakerfe) cluster(speakerfe)
eststo m5: reghdfe scorestd minor divided_govt loglength, absorb(topic1_new chamberyearfe speakerfe) cluster(speakerfe)
eststo m6: reghdfe scorestd minor divided_govt loglength sentiment, absorb(topic1_new chamberyearfe speakerfe) cluster(speakerfe)


esttab m1 m2 m3 m4 m5 m6 using "../../results/appendix/tabA9.tex", f label replace booktabs alignment(D{.}{.}{-1}) ///
s(N r2, fmt(0 2) label("Observations" "R-squared")) ///
nomtitles star(* 0.10 ** 0.05 *** 0.01) r2 b(3) se(3) brac nonotes

