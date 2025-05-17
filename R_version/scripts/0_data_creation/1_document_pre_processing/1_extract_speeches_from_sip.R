dane_sample <- read.csv("C:\\Users\\Wercia\\OneDrive\\Desktop\\2025\\RR\\replication package ALL\\data\\1_main_datasets\\main_dataset.csv", header = TRUE, sep = ",", nrows = 1000)
head(dane_sample)

install.packages("haven")
library(haven)

dane <- read_dta("C:\\Users\\Wercia\\OneDrive\\Desktop\\2025\\RR\\replication package ALL\\data\\1_main_datasets\\dataset_tables.dta")
head(dane)

set.seed(123)
sampled <- dane[sample(nrow(dane), 1000), ]
View(sampled)