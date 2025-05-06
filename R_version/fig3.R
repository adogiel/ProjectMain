# Install required libraries if not already installed
install.packages(c("ggplot2", "dplyr", "readr", "tidyr"))

# Load libraries
library(ggplot2)
library(dplyr)
library(readr)
library(tidyr)
# Set working directory
wd <- "/Users/ulviyaabasova/Desktop/xxx"  # Replace with your actual directory

# Set data and results paths
wd_data <- paste0(wd, "/3 Replication Package/data/1_main_datasets")
wd_results <- paste0(wd, "/3 Replication Package/results/main_paper")
wd_aux <- paste0(wd, "/3 Replication Package/data/3_auxiliary_data")

# Load dataset
df <- read_csv(paste0(wd_data, "/main_dataset.csv"))
# Add demeaned score and adjust some variables
df <- df %>%
  rename(topic_num = topic1_new) %>%
  mutate(
    topic_num = as.integer(topic_num),
    score_demeaned = score - ave(score, congress, FUN = mean)
  )
# Load topic labels
topic_labels <- read_csv(paste0(wd_aux, "/topics_numbers.csv"), col_names = FALSE)
topic_labels <- topic_labels %>%
  mutate(
    topic_num = as.integer(X1),
    topic = X2,
    theme = X3
  ) %>%
  separate(topic, into = c("topic_broad", "topic_detail"), sep = " - ", fill = "right") %>%
  mutate(
    topic_macro = case_when(
      topic_broad %in% c("Economic Policy", "Fiscal Policy", "Monetary Policy") ~ "Economy",
      topic_broad == "Governance" ~ "Governance",
      topic_broad %in% c("Immigration", "Social Issues") ~ "Society",
      topic_broad == "Foreign Policy" ~ "Foreign Affairs",
      topic_broad == "Procedure" ~ "Procedure",
      topic_broad == "National Narrative" ~ "National Narrative",
      topic_broad %in% c("Party Politics", "Tribute") ~ "Party Politics",
      TRUE ~ NA_character_
    )
  )

# Merge topic labels with main dataset
df <- left_join(df, topic_labels, by = "topic_num")

# Filter dataset to start from 1970
df <- df %>%
  filter(speech_year >= 1970)


# Panel A - Plotting
topics <- df %>%
  group_by(topic_broad) %>%
  summarize(score = mean(score_demeaned, na.rm = TRUE)) %>%
  filter(topic_broad != "Miscellaneous") %>%
  arrange(desc(score))

# Create bar plot
ggplot(topics, aes(x = reorder(topic_broad, score), y = score, fill = score > 0)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  coord_flip() +
  scale_fill_manual(values = c("purple", "darkgreen")) +
  labs(
    title = "Panel A",
    x = "Average Topic Emotionality",
    y = "",
    subtitle = "Emotionality per Topic"
  ) +
  theme_minimal(base_size = 20) +
  theme(
    axis.text.y = element_text(size = 28),
    axis.text.x = element_text(size = 20),
    plot.title = element_text(size = 45, hjust = 0),
    plot.subtitle = element_text(size = 25, hjust = 0)
  ) +
  ggsave(paste0(wd_results, "/fig3a.png"), width = 15, height = 20)
# Panel B - Plotting
topics_party <- df %>%
  group_by(party, topic_broad) %>%
  summarize(score = mean(score_demeaned, na.rm = TRUE)) %>%
  filter(topic_broad != "Miscellaneous")

# Separate data for Republicans and Democrats
dati1 <- filter(topics_party, party == "Republican") %>%
  arrange(topic_broad)
dati2 <- filter(topics_party, party == "Democrat") %>%
  arrange(topic_broad)

# Calculate ratio of Republican to Democrat emotionality
dati1$ratio <- dati1$score / dati2$score - 1

# Merge back for proper sorting and labeling
dati1$Rank <- match(dati1$topic_broad, topics$topic_broad)
dati1 <- dati1 %>% arrange(Rank)

# Create bar plot
ggplot(dati1, aes(x = reorder(topic_broad, Rank), y = ratio, fill = ratio > 0)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  scale_fill_manual(values = c("red", "blue")) +
  labs(
    title = "Panel B",
    x = "Average Topic Emotionality for Republicans over Democrats",
    y = "",
    subtitle = "Difference in Emotionality between Republicans and Democrats"
  ) +
  theme_minimal(base_size = 20) +
  theme(
    axis.text.y = element_text(size = 28),
    axis.text.x = element_text(size = 20),
    plot.title = element_text(size = 45, hjust = 0),
    plot.subtitle = element_text(size = 25, hjust = 0)
  ) +
  annotate("rect", xmin = 0, xmax = 2, ymin = -Inf, ymax = Inf, fill = "red", alpha = 0.1) +
  annotate("rect", xmin = -2, xmax = 0, ymin = -Inf, ymax = Inf, fill = "blue", alpha = 0.1) +
  ggsave(paste0(wd_results, "/fig3b.png"), width = 15, height = 20)



