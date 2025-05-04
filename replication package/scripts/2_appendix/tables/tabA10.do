*******************************************************************
*
* Emotion and Reason in Political LanguageL: Replication Package
* Gennaro and Ash
* Table A10
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

* Demographics      ***********************************************

// demo appendix - with additional controls

eststo m0: reghdfe scorestd dw2_s democrat female black hispanic asian catholic jewish loglength, absorb(chamberyearfe topic1_new miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)
eststo m1: reghdfe scorestd dw2_s democrat female black hispanic asian catholic jewish loglength sentiment, absorb(chamberyearfe topic1_new miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)
eststo m2: reghdfe scorestd dw2_s democrat female black hispanic asian catholic jewish if inrange(speech_year, 1950, 1975), absorb(chamberyearfe topic1_new miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)
eststo m3: reghdfe scorestd dw2_s democrat female black hispanic asian catholic jewish if inrange(speech_year, 1975, 2000), absorb(chamberyearfe topic1_new miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)
eststo m4: reghdfe scorestd dw2_s democrat female black hispanic asian catholic jewish if speech_year>2000, absorb(chamberyearfe topic1_new miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)

esttab m0 m1 m2 m3 m4 using "../../results/tabA10.tex", f label replace booktabs alignment(D{.}{.}{-1}) ///
interaction("*") s(N r2, fmt(0 2) label("Observations" "R-squared")) ///
nomtitles star(* 0.10 ** 0.05 *** 0.01) r2 b(3) se(3) brac nonotes

