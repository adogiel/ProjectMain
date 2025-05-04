***********************************************
*
* Emotion and Reason in Political LanguageL: Replication Package
* Gennaro and Ash
* Fig A21
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


egen affectstd = std(affect)
egen cognitionstd = std(cognition)



// DW-NOMINATE binscatters
*grstyle init
*grstyle set plain, horizontal grid


* NEW FIG HERE
gen nominate_clipped = nominate_dim1 if abs(nominate_dim1) <= .6

binscatter score nominate_clipped,  linetype(qfit) ytitle("Emotionality Score") xtitle("DW-NOMINATE") xline(0, lpattern(dash) lcolor(gray) lwidth(thin)) nquantiles(17) xticks(-.6 -.3 0 .3 .6)

cmogram score nominate_clipped,  qfitci graphopts(ytitle("Emotionality Score") xtitle("DW-NOMINATE") xline(0, lpattern(dash) lcolor(gray) lwidth(thin)) )  histopts(bin(17))

graph export "../../results/appendix/figA21.png", replace

