***********************************************
*
* Emotion and Reason in Political Language
* -- Replication Package
* Gennaro and Ash
* 2021
*
* Table 2: How Emotionality Varies by Politician Characteristics
*
***********************************************


clear all


* Set the folder where to find the replication package/data/1_main_datasets
cd "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

global wd "./3 replication package/data/1_main_datasets"
cd "$wd"



* Upload the Data
use dataset_tables.dta, clear


* Subset
keep if democrat==1 | republican==1

gen dw2 = nominate_dim1^2
egen dw2_s = std(dw2)

* Deal with missing values: replace with a missing dummy
replace topic1_new=1000 if topic1_new==.

local vars "female black asian hispanic catholic jewish dw2_s"
foreach v in `vars'{
	gen miss_`v' = `v'==.
    replace `v'=0 if `v' ==.
}


* Table

eststo m0: reghdfe scorestd dw2_s, absorb(miss_dw2 chamberyearfe) cluster(speakerfe)
eststo m1: reghdfe scorestd democrat, absorb(chamberyearfe) cluster(speakerfe)
eststo m2: reghdfe scorestd female, absorb(chamberyearfe miss_female) cluster(speakerfe)
eststo m3: reghdfe scorestd black hispanic asian, absorb(chamberyearfe miss_black miss_asian miss_hispanic) cluster(speakerfe)
eststo m4: reghdfe scorestd catholic jewish, absorb(chamberyearfe miss_catholic miss_jewish) cluster(speakerfe)
eststo m5: reghdfe scorestd dw2_s democrat female black hispanic asian catholic jewish, absorb(chamberyearfe miss_dw2 miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)
eststo m6: reghdfe scorestd dw2_s democrat female black hispanic asian catholic jewish, absorb(chamberyearfe miss_dw2 topic1_new miss_female miss_black miss_asian miss_hispanic miss_catholic miss_jewish) cluster(speakerfe)

esttab m0 m1 m2 m3 m4 m5 m6 using "../../results/main_paper/tab2.tex", f label replace booktabs alignment(D{.}{.}{-1}) ///
interaction("*") s(N r2, fmt(0 2) label("Observations" "R-squared")) ///
nomtitles star(* 0.10 ** 0.05 *** 0.01) r2 b(3) se(3) brac nonotes

