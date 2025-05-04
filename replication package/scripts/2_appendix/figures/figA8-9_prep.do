***********************************************
*
* Emotion and Reason in Political LanguageL: Replication Package
* Gennaro and Ash
* Data preparation for Fig A8-A9
*
***********************************************


* Working Directory

* Set the folder where to find the replication package
cd "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

global wd "./3 replication package/data/1_main_datasets"
cd "$wd"

* Upload the Data   ***********************************************

use dataset_tables.dta, clear



* Data Cleaning

keep if democrat==1 | republican==1

gen dw2 = nominate_dim1^2
egen dw2_s = std(dw2)

gen loglength = log(length)


* Deal with missings
replace topic1_new=1000 if topic1_new==.

local vars "female black asian hispanic catholic jewish dw2_s"
foreach v in `vars'{
	gen miss_`v' = `v'==.
    replace `v'=0 if `v' ==.
}




* Residualized plot on demographics only

preserve

keep if speech_year>=1914

reghdfe score female black hispanic asian catholic jewish, res(residuals) absorb(miss_female miss_black miss_hispanic miss_asian miss_catholic miss_jewish) cluster(speakerfe)
gen samp = e(sample)

keep if samp==1

summarize score, meanonly
local mean1 = r(mean)
replace residuals = residuals + `mean1'


keep house speech_year residuals score
collapse (mean) res_mean=residuals score_mean=score (sd) res_sd=residuals score_sd=score, by(house speech_year)
export delimited using "../3_auxiliary_data/emotionality_score_res_demo.csv", replace
restore




* Residualized plot on all characteristics


preserve

keep if speech_year>=1914

reghdfe score female black hispanic asian catholic jewish, res(residuals) absorb(topic1_new miss_female miss_black miss_hispanic miss_asian miss_catholic miss_jewish) cluster(speakerfe)
gen samp = e(sample)

keep if samp==1

summarize score, meanonly
local mean1 = r(mean)
replace residuals = residuals + `mean1'


keep house speech_year residuals score
collapse (mean) res_mean=residuals score_mean=score (sd) res_sd=residuals score_sd=score, by(house speech_year)
export delimited using "../3_auxiliary_data/emotionality_score_res_demo_topics.csv", replace
restore

