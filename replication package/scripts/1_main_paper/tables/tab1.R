####################################################################################
#
# Emotion and Reason in Political Language
# Gennaro & Ash
#
# Description:
# - Reproduce Results in Table 1
####################################################################################


library(dplyr)
library(data.table)
library(tidyr)
library(plyr)
library(stringi)
library(stringr)

# set the folder of the replication package
wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

mainwd <- paste0(wd, "/3 Replication Package/data/2_validation results")

setwd(mainwd)
main_data = read.csv('validation_consolidated.csv')

#####################
## Panel A         ##
#####################

# overall - Full Sample
df = main_data
l = length(df$responseid)
c = length(df$responseid[df$right==1])
w = length(df$responseid[df$right==0])
cr = round(c/(c+w), 3)
n = round(length(df$responseid[is.na(df$right)])/l, 3)
paste0('The full sample has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()

# Overall - English comprehension passed
df = main_data[(main_data$check_w_a==1 & main_data$check_w_c==1), ]
l = length(df$responseid)
c = length(df$responseid[df$right==1])
w = length(df$responseid[df$right==0])
cr = round(c/(c+w), 3)
n = round(length(df$responseid[is.na(df$right)])/l, 3)
paste0('The restricted sample has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()

# Overall - Consistent Coding
temp = aggregate(right ~ unique_set_sent + question, data = main_data, FUN = sum)
temp = temp[temp$right != 1, ]
df = main_data[main_data$unique_set_sent %in% temp$unique_set_sent, ]
l = length(df$responseid)
c = length(df$responseid[df$right==1])
w = length(df$responseid[df$right==0])
cr = round(c/(c+w), 3)
n = round(length(df$responseid[is.na(df$right)])/l, 3)
paste0('The restricted sample has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()



#####################
## Panel B         ##
#####################

# Overall
df = aggregate(right ~ unique_set_sent + question, data = main_data, FUN = sum)
df = main_data[(main_data$unique_set_sent %in% df$unique_set_sent), ]
for (s in sort(unique(df$decade))){
  temp = df[df$decade==s,]
  l = length(temp$responseid)
  c = length(temp$responseid[temp$right==1])
  w = length(temp$responseid[temp$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(temp$responseid[is.na(temp$right)])/l, 3)
  paste0('Decade ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
  }



# Overall - English comprehension passed
df = main_data[(main_data$check_w_a==1 & main_data$check_w_c==1), ]
for (s in sort(unique(df$decade))){
  temp = df[df$decade==s,]
  l = length(temp$responseid)
  c = length(temp$responseid[temp$right==1])
  w = length(temp$responseid[temp$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(temp$responseid[is.na(temp$right)])/l, 3)
  paste0('Decade ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
}


# Overall - Consisntent Coding
df = aggregate(right ~ unique_set_sent + question, data = main_data, FUN = sum)
df = df[df$right != 1, ]
df = main_data[main_data$unique_set_sent %in% df$unique_set_sent, ]
for (s in sort(unique(df$decade))){
  temp = df[df$decade==s,]
  l = length(temp$responseid)
  c = length(temp$responseid[temp$right==1])
  w = length(temp$responseid[temp$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(temp$responseid[is.na(temp$right)])/l, 3)
  paste0('Decade ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
}




#####################
## Panel C         ##
#####################

main_data = read.csv('validation_round2.csv')

# Overall : Set 4 is AC, set 1 is word count
for (s in sort(unique(main_data$setid))){
  df = main_data[main_data$setid==s,]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(df$responseid[is.na(df$right)])/l, 3)
  #  paste0('Set ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
  paste0(s, ' & ', cr, '& ', n , ' & ', l) %>% print()
  
}



# Overall - English comprehension passed
temp = main_data[(main_data$check_w_a==1 & main_data$check_w_c==1), ]
for (s in sort(unique(temp$setid))){
  df = temp[temp$setid==s,]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr =round( c/(c+w), 3)
  n = round(length(df$responseid[is.na(df$right)]) / l, 3)
  # paste0('Set ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
  paste0(s, ' & ', cr, '& ', n , ' & ', l) %>% print()
  
}



# Overall - Consisntent Coding
main_data$unique_set_sent = paste0(main_data$setid, '_', main_data$pair_id)

# Word Count
temp = main_data[main_data$setid==1,]
temp = aggregate(right ~ unique_set_sent + question, data = temp, FUN = sum)
temp = temp[temp$right != 1, ]
temp = main_data[main_data$unique_set_sent %in% temp$unique_set_sent, ]
for (s in sort(unique(temp$setid))){
  d = temp[temp$setid==s,]
  l = length(d$responseid)
  c = length(d$responseid[d$right==1])
  w = length(d$responseid[d$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(d$responseid[is.na(d$right)])/l, 3)
  paste0(s, ' & ', cr, '& ', n , ' & ', l) %>% print()
}


# AC vector
temp = main_data[main_data$setid==4,]
temp = aggregate(right ~ unique_set_sent + question, data = temp, FUN = sum)
temp = temp[temp$right != 1, ]
temp = main_data[main_data$unique_set_sent %in% temp$unique_set_sent, ]
for (s in sort(unique(temp$setid))){
  d = temp[temp$setid==s,]
  l = length(d$responseid)
  c = length(d$responseid[d$right==1])
  w = length(d$responseid[d$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(d$responseid[is.na(d$right)])/l, 3)
  paste0(s, ' & ', cr, '& ', n , ' & ', l) %>% print()
}

