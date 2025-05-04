*******************************************************************
*
* Emotion and Reason in Political LanguageL: Replication Package
* Gennaro and Ash
* Table A8
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



// demo appendix - affect only

egen affectstd = std(affect)

eststo clear
eststo m0: reghdfe affectstd dw2_s, absorb(chamberyearfe) cluster(speakerfe)
eststo m1: reghdfe affectstd democrat, absorb(chamberyearfe) cluster(speakerfe)
eststo m2: reghdfe affectstd female, absorb(chamberyearfe miss_female) cluster(speakerfe)
eststo m3: reghdfe affectstd black hispanic asian, absorb(chamberyearfe miss_black miss_asian miss_hispanic) cluster(speakerfe)
eststo m4: reghdfe affectstd catholic jewish, absorb(chamberyearfe miss_catholic miss_jewish) cluster(speakerfe)
eststo m5: reghdfe affectstd dw2_s democrat female black hispanic asian catholic jewish, absorb(chamberyearfe miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)
eststo m6: reghdfe affectstd dw2_s democrat female black hispanic asian catholic jewish, absorb(chamberyearfe topic1_new miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)

esttab m0 m1 m2 m3 m4 m5 m6 using  "../../results/appendix/tabA8a.tex", f label replace booktabs alignment(D{.}{.}{-1}) ///
interaction("*") s(N r2, fmt(0 2) label("Observations" "R-squared")) ///
nomtitles star(* 0.10 ** 0.05 *** 0.01) r2 b(3) se(3) brac nonotes



// demo appendix - cognition only

egen cognitionstd = std(cognition)

eststo clear
eststo m0: reghdfe cognitionstd dw2_s, absorb(chamberyearfe) cluster(speakerfe)
eststo m1: reghdfe cognitionstd democrat, absorb(chamberyearfe) cluster(speakerfe)
eststo m2: reghdfe cognitionstd female, absorb(chamberyearfe miss_female) cluster(speakerfe)
eststo m3: reghdfe cognitionstd black hispanic asian, absorb(chamberyearfe miss_black miss_asian miss_hispanic) cluster(speakerfe)
eststo m4: reghdfe cognitionstd catholic jewish, absorb(chamberyearfe miss_catholic miss_jewish) cluster(speakerfe)
eststo m5: reghdfe cognitionstd dw2_s democrat female black hispanic asian catholic jewish, absorb(chamberyearfe miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)
eststo m6: reghdfe cognitionstd dw2_s democrat female black hispanic asian catholic jewish, absorb(chamberyearfe topic1_new miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)

esttab m0 m1 m2 m3 m4 m5 m6 using "../../results/appendix/tabA8b.tex", f label replace booktabs alignment(D{.}{.}{-1}) ///
interaction("*") s(N r2, fmt(0 2) label("Observations" "R-squared")) ///
nomtitles star(* 0.10 ** 0.05 *** 0.01) r2 b(3) se(3) brac nonotes

