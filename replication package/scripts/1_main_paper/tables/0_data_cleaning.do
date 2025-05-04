***********************************************
*
* Emotion and Reason in Political Language
* -- Replication Package
* Gennaro and Ash
* 2021
*
* Prepare the main dataset to be used with stata
*
***********************************************


* Working Directory   *********************************************

clear all

* Set the folder where to find the replication package/data/1_main_datasets
cd "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

global wd "./3 replication package/data/1_main_datasets"
cd "$wd"


* Upload the Data   ***********************************************

insheet using  main_dataset.csv


* Data cleaning for tables  ***************************************

drop v1 

* Female
gen female = 1 if gender == "F"
replace female = 0 if gender == "M"
drop gender

* Party
gen democrat = 1 if party == "Democrat"
replace democrat = 0 if party != "Democrat" & party!= ""
gen republican = 1 if party== "Republican"
replace republican = 0 if party != "Republican" & party!= ""
drop party

* Chamber
gen house = chamber == "house"
gen senate = chamber == "senate"
drop chamber 

* Race
tab race
gen black = race == "African American"
gen hispanic = race == "Hispanic"
gen asian = race == "Asian American"
gen native = race == "Native American"
gen white = race == "White"
local vars "black hispanic asian native white"
foreach v in `vars'{
     replace `v' = . if race==""
}


* Religion
gen catholic = religion == "Roman Catholic"
gen jewish = religion == "Jewish"
local vars "catholic jewish"
foreach v in `vars'{
     replace `v'=. if religion==""
}

* Fixed effects
* egen speakerfe = group(chamber last start)
egen speakerfe = group(member tenure_end tenure_start)
egen chamberyearfe = group(house speech_year)
egen partyyearfe = group(democrat speech_year)
egen partychamberfe = group(democrat senate)

* Experience
bys speakerfe: egen start_year = min(speech_year)
gen experience = speech_year - start_year

* Age
split birthday, g(birth_year) p(-) l(1)
destring birth_year, replace force 
g age = speech_year - birth_year



* DW nominate
gen absnom = abs(nominate_dim1)
gen absnom2 = abs(nominate_dim2)

* Majorities
gen s_dem_maj = s_maj_party == "D"
gen h_dem_maj = h_maj_party == "D"
gen pres_dem_maj = (pres_party == "D" | pres_party == "Democratic/National Union")

gen dem_control = s_dem_maj + h_dem_maj + pres_dem_maj
gen divided_govt = dem_control == 1 | dem_control == 2

gen rep_control = 3 - dem_control

* minority parties
gen minority_party = 0
replace minority_party = 1 if dem_control >= 2 & republican
replace minority_party = 1 if dem_control <= 1 & democrat

gen minor = 1 if (democrat==1 & h_dem_maj==0 & house==1) | (democrat==1 & s_dem_maj==0 & senate==1) | ///
	(republican==1 & h_dem_maj==1 & house==1) | (republican==1 & s_dem_maj==1 & senate==1)
replace minor = 0 if (democrat==1 & h_dem_maj==1 & house==1) | (democrat==1 & s_dem_maj==1 & senate==1) | ///
	(republican==1 & h_dem_maj==0 & house==1) | (republican==1 & s_dem_maj==0 & senate==1)

gen your_pres = 1 if (democrat==1 & pres_dem_maj==1) | (republican==1 & pres_dem_maj==0)
replace your_pres = 0 if (democrat==1 & pres_dem_maj==0) | (republican==1 & pres_dem_maj==1)
gen minority_pres = 1 - your_pres


* Measures
gen cognition = 1-cognition_d
gen affect = 1-affect_d

egen scorestd = std(score)


compress
save dataset_tables.dta, replace

