####################################################################################
#
# Emotion and Reason in Political Language
# Gennaro & Ash
#
# Description:
# - Reproduce Table A6
####################################################################################



library(dplyr)
library(data.table)
library(tidyr)
library(plyr)


wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

mainwd <- paste0(wd, "/3 Replication Package/data/2_validation results")

setwd(mainwd)
main_data = read.csv('validation_round1.csv')


#################
## Panel A     ##
#################

data = main_data[main_data$setid %in% c(1,2,3,4),]

# Overall 
for (s in sort(unique(data$setid))){
  df = data[data$setid==s,]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr = c/(c+w)
  n = length(df$responseid[is.na(df$right)])/l
  # paste0('Set ', s, ' has ', c, ' correct answers vs ', w, ' wrong and ', n , ' nulls') %>% print()
  paste0('Set ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
}


# Overall - English comprehension passed
temp = data[(data$check_w_a==1 & data$check_w_c==1), ]
for (s in sort(unique(temp$setid))){
  df = temp[temp$setid==s,]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr = c/(c+w)
  n = length(df$responseid[is.na(df$right)]) / l
  paste0('Set ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
}


# Overall - Consistent Coding
data$unique_set_sent = paste0(data$setid, '_', data$pair_id)
temp = aggregate(right ~ unique_set_sent + question, data = data, FUN = sum)
temp = temp[temp$right != 1, ]
temp = data[data$unique_set_sent %in% temp$unique_set_sent, ]

for (s in sort(unique(temp$setid))){
  d = temp[temp$setid==s,]
  l = length(d$responseid)
  c = length(d$responseid[d$right==1])
  w = length(d$responseid[d$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(d$responseid[is.na(d$right)])/l, 3)
  paste0('Set ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
  
}




#################
## Panel C     ##
#################


data = main_data[main_data$setid %in% c(6, 7),]

# Overall 
for (s in sort(unique(data$setid))){
  df = data[data$setid==s,]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr = c/(c+w)
  n = length(df$responseid[is.na(df$right)])/l
  # paste0('Set ', s, ' has ', c, ' correct answers vs ', w, ' wrong and ', n , ' nulls') %>% print()
  paste0('Set ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
}


# Overall - English comprehension passed
temp = data[(data$check_w_a==1 & data$check_w_c==1), ]
for (s in sort(unique(temp$setid))){
  df = temp[temp$setid==s,]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr = c/(c+w)
  n = length(df$responseid[is.na(df$right)]) / l
  paste0('Set ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
}

# Overall - Consistent Coding
data$unique_set_sent = paste0(data$setid, '_', data$pair_id)
temp = aggregate(right ~ unique_set_sent + question, data = data, FUN = sum)
temp = temp[temp$right != 1, ]
temp = data[data$unique_set_sent %in% temp$unique_set_sent, ]

for (s in sort(unique(temp$setid))){
  d = temp[temp$setid==s,]
  l = length(d$responseid)
  c = length(d$responseid[d$right==1])
  w = length(d$responseid[d$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(d$responseid[is.na(d$right)])/l, 3)
  paste0('Set ', s, ' has ', cr, ' correct rate and ', n , ' nulls. Out of a total of ', l, ' sentences') %>% print()
  
}




#################
## Panel B     ##
#################

main_data = read.csv('validation_round2.csv')
main_data$unique_set_sent = paste0(main_data$setid, '_', main_data$pair_id)
main_data = main_data[main_data$setid==3,] 


# Overall
temp = main_data
temp = as.data.table(temp)
temp$id = paste0(temp$responseid, temp$pair_id)
setkey(temp, id) # important for ordering
temp = temp[,prova_lag:=shift(score, 1), by=id]
temp = temp[,prova_lead:=shift(score, 1, type='lead'), by=id]
temp$other_score = ifelse(is.na(temp$prova_lag), temp$prova_lead, temp$prova_lag)
temp$delta = abs(temp$other_score - temp$score)
temp$delta[temp$right==1] %>% mean(na.rm=TRUE)
temp$delta[temp$right==0] %>% mean(na.rm=TRUE)
sd = temp$delta %>% sd()
for (s in 0:5){
  df = temp[(temp$delta >= sd*s & temp$delta < sd*(s+1)),]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(df$responseid[is.na(df$right)])/l, 3)
  paste0(' & ' , cr, ' & ', n,  ' & ' , l ) %>% print()
}


# Overall - English comprehension passed
temp = main_data[(main_data$check_w_a==1 & main_data$check_w_c==1), ]
temp = as.data.table(temp)
temp$id = paste0(temp$responseid, temp$pair_id)
setkey(temp, id) # important for ordering
temp = temp[,prova_lag:=shift(score, 1), by=id]
temp = temp[,prova_lead:=shift(score, 1, type='lead'), by=id]
temp$other_score = ifelse(is.na(temp$prova_lag), temp$prova_lead, temp$prova_lag)
temp$delta = abs(temp$other_score - temp$score)
temp$delta[temp$right==1] %>% mean(na.rm=TRUE)
temp$delta[temp$right==0] %>% mean(na.rm=TRUE)
sd = temp$delta %>% sd()
for (s in 0:5){
  df = temp[(temp$delta >= sd*s & temp$delta < sd*(s+1)),]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(df$responseid[is.na(df$right)])/l, 3)
  paste0(' & ' , cr, ' & ', n,  ' & ' , l ) %>% print()
}



# Overall - Consistent Coding
temp = aggregate(right ~ unique_set_sent + question, data = main_data, FUN = sum)
temp = temp[temp$right != 1, ]
temp = main_data[main_data$unique_set_sent %in% temp$unique_set_sent, ]

temp = as.data.table(temp)
temp$id = paste0(temp$responseid, temp$pair_id)
setkey(temp, id) # important for ordering
temp = temp[,prova_lag:=shift(score, 1), by=id]
temp = temp[,prova_lead:=shift(score, 1, type='lead'), by=id]
temp$other_score = ifelse(is.na(temp$prova_lag), temp$prova_lead, temp$prova_lag)
temp$delta = abs(temp$other_score - temp$score)
temp$delta[temp$right==1] %>% mean(na.rm=TRUE)
temp$delta[temp$right==0] %>% mean(na.rm=TRUE)
sd = temp$delta %>% sd()

for (s in 0:5){
  df = temp[(temp$delta >= sd*s & temp$delta < sd*(s+1)),]
  l = length(df$responseid)
  c = length(df$responseid[df$right==1])
  w = length(df$responseid[df$right==0])
  cr = round(c/(c+w), 3)
  n = round(length(df$responseid[is.na(df$right)])/l, 3)
  paste0(' & ' , cr, ' & ', n,  ' & ' , l ) %>% print()
  }



