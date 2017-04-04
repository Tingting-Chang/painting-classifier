library(googleVis)
library(shiny)
library(ggplot2)
library(dplyr)
library(shinydashboard)

addResourcePath(prefix = 'images', '../data/images_athenaeum/full')

# Author
authors = read.csv('../data/athenaeum_authors.csv')
painting_sizes = read.csv('../data/athenaeum_paintings_sizes.csv')
kmeans_centers = read.csv('../data/kmeans_centers.csv')
color_hist = read.csv('../data/color_hist_kmeans_206552.csv')
# painting = read.csv('data/athenaeum_paintings.csv')

# data for painting type count
painting_type <- painting_sizes %>% group_by(article_type) %>%
  summarise(type_count = n()) %>%
  arrange(desc(type_count))

# data for top authors
author_painting <- merge(authors, painting_sizes, by=c("author_id"), all = FALSE)
top_authors <- author_painting %>% group_by(author_id, last_name) %>%
  summarise(num_work = n()) %>%
  arrange(desc(num_work)) %>%
  head(20)

# data for nationality
author_num_work <- author_painting %>% group_by(author_id) %>%
  summarise(num_works = n())
author_painting <- merge(author_num_work, author_painting, by=c("author_id"), all = FALSE)
nations <- author_painting %>% group_by(nationality) %>%
  summarise(num_authors = n(), num_paintings = sum(num_works)) %>%
  arrange(desc(num_paintings)) %>%
  head(30)

# data for media
medias <- author_painting %>% group_by(medium) %>%
  summarise(num_paintings = n()) %>%
  arrange(desc(num_paintings)) %>%
  head(20)
 
# data for painting samples
type_col <- unlist(painting_type %>% select(article_type))
names(type_col) <- NULL


# data for sample paintings
SamplePainting <- function(article_type) {
  p <- painting_sizes[painting_sizes$article_type == article_type, ]
  #sample_painting = p[sample(nrow(p), 8), ]
  sample_painting = sample_n(p, min(8, nrow(p)), replace = F)
  
  return(sample_painting)
}


# data for kmeans
kmeans_data <- read.csv('../data/color_hist_kmeans_distance.csv')
label_col <- seq(0,6)

KmeansPainting <- function(label, num_paintings = 10) {
  return(kmeans_data %>% filter(kmeans_labels == label) %>%
           arrange(distance_to_centroid) %>% head(num_paintings))
}

# kmeans.10 <- kmeans_data %>% group_by(kmeans_labels) %>%
#   arrange(distance_to_centroid) %>%
#   top_n(10)



image_path <- function(author_id, painting_id) {
  return(paste0('../data/images_athenaeum/full/', author_id, '/', painting_id, '.jpg'))
}
image_path_html <- function(author_id, painting_id) {
  return(paste0('images/', author_id, '/', painting_id, '.jpg'))
}
