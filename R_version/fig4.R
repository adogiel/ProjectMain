# Install required libraries if not already installed
install.packages(c("ggplot2", "dplyr", "readr", "tidyr"))

# Load libraries
library(ggplot2)
library(dplyr)
library(readr)
library(tidyr)
# Set working directory
wd <- "/path/to/your/directory"  # Replace with your actual directory

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

# Load and process topic labels
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

# Filter dataset to start from 1900 (Congress 56)
df <- df %>%
  filter(congress >= 56)
# Panel A - Plotting
data <- df %>%
  select(congress, speech_year, topic_macro, score)

# Extract the first speech year for each congress
lab <- data %>%
  group_by(congress) %>%
  summarize(labyear = first(speech_year))

# Merge to get labyear column in the dataset
data <- left_join(data, lab, by = "congress")

# Compute mean score by topic and year
t1 <- data %>%
  group_by(topic = topic_macro, labyear) %>%
  summarize(score = mean(score, na.rm = TRUE))

# Compute standard error of the mean
t2 <- data %>%
  group_by(topic = topic_macro, labyear) %>%
  summarize(score_std = sd(score, na.rm = TRUE) / sqrt(n()))

# Merge the data
topics <- left_join(t1, t2, by = c("topic", "labyear"))
topics <- topics %>%
  filter(topic != "")

# Plot
labels <- unique(topics$topic)
ggplot() +
  geom_line(data = topics, aes(x = labyear, y = score, color = topic, size = (topic == "Economy")), show.legend = TRUE) +
  scale_size_manual(values = c(1, 2)) +
  scale_color_manual(values = c("red", "blue", "green", "purple", "orange", "pink", "brown", "yellow")) +
  scale_x_continuous(breaks = seq(1900, 2015, 4)) +
  theme_minimal(base_size = 20) +
  theme(
    axis.text.x = element_text(angle = 90, size = 20),
    axis.text.y = element_text(size = 20),
    legend.text = element_text(size = 20),
    legend.title = element_text(size = 24),
    plot.title = element_text(size = 40, hjust = 0),
    plot.subtitle = element_text(size = 25, hjust = 0)
  ) +
  labs(
    title = "Panel A",
    x = "Year",
    y = "Average Emotionality",
    subtitle = "Emotionality by Topic over Time"
  ) +
  theme(legend.position = "upper left") +
  ggsave(paste0(wd_results, "/fig4a.png"), width = 30, height = 15)
# Panel B - Plotting
data <- df %>%
  select(congress, speech_year, topic_broad, score)

# Extract the first speech year for each congress
lab <- data %>%
  group_by(congress) %>%
  summarize(labyear = first(speech_year))

# Merge to get labyear column in the dataset
data <- left_join(data, lab, by = "congress")

# Compute mean score by topic and year
t1 <- data %>%
  group_by(topic = topic_broad, labyear) %>%
  summarize(score = mean(score, na.rm = TRUE))

# Compute standard error of the mean
t2 <- data %>%
  group_by(topic = topic_broad, labyear) %>%
  summarize(score_std = sd(score, na.rm = TRUE) / sqrt(n()))

# Merge the data
topics <- left_join(t1, t2, by = c("topic", "labyear"))

# Select relevant topics for Panel B
labels <- c('Economic Policy', 'Monetary Policy', 'Fiscal Policy')

# Plot
ggplot() +
  geom_line(data = topics %>% filter(topic %in% labels), aes(x = labyear, y = score, color = topic)) +
  scale_x_continuous(breaks = seq(1900, 2015, 4)) +
  scale_color_manual(values = c("red", "green", "blue")) +
  theme_minimal(base_size = 20) +
  theme(
    axis.text.x = element_text(angle = 90, size = 20),
    axis.text.y = element_text(size = 20),
    legend.text = element_text(size = 20),
    legend.title = element_text(size = 24),
    plot.title = element_text(size = 40, hjust = 0),
    plot.subtitle = element_text(size = 25, hjust = 0)
  ) +
  labs(
    title = "Panel B",
    x = "Year",
    y = "Average Emotionality",
    subtitle = "Emotionality by Subtopic over Time"
  ) +
  theme(legend.position = "upper left") +
  ggsave(paste0(wd_results, "/fig4b.png"), width = 30, height = 15)
