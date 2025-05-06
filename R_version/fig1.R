# Install required packages if not already installed
install.packages(c("tm", "wordcloud", "wordcloud2", "textTinyR", "text", "ggplot2"))
install.packages("tm")
install.packages("wordcloud")
install.packages("wordcloud2")
install.packages("textTinyR")
install.packages("text")

# Load libraries
library(tm)
library(wordcloud)
library(wordcloud2)
library(textTinyR)
library(ggplot2)



# Set working directory
wd <- "/Users/ulviyaabasova/Desktop/xxx"  # Replace with your actual directory

# Set paths
wd_data <- paste0(wd, "/3 Replication Package/data/1_main_datasets")
wd_results <- paste0(wd, "/3 Replication Package/results/main_paper")
wd_aux <- paste0(wd, "/3 Replication Package/data/3_auxiliary_data")
wd_model <- paste0(wd, "/3 Replication Package/models")

# Load word frequencies, model, dictionaries, centroids
freqs <- readRDS(paste0(wd_aux, "/word_freqs.rds"))
w2v <- readRDS(paste0(wd_model, "/w2v-vectors_8_300.rds"))
cognition <- readRDS(paste0(wd_aux, "/dictionary_cognition.rds"))
affect <- readRDS(paste0(wd_aux, "/dictionary_affect.rds"))
affect_centroid <- readRDS(paste0(wd_aux, "/affect_centroid.rds"))
cog_centroid <- readRDS(paste0(wd_aux, "/cog_centroid.rds"))

