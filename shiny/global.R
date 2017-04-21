library(googleVis)
library(shiny)
library(ggplot2)
library(dplyr)
library(shinydashboard)
library(leaflet)

addResourcePath(prefix = 'images', '../data/images_athenaeum/full')
print("dependencies loaded")

# Author
authors <- read.csv('../data/athenaeum_authors.csv')
print("authors loaded")
painting_sizes <- read.csv('../data/athenaeum_paintings_sizes.csv')
print("paintings loaded")
kmeans_centers <- read.csv('../data/kmeans_centers.csv')
print("k-means centroids loaded")
color_hist <- read.csv('../data/color_hist_kmeans_206552.csv')
color_hist_repr <- unlist(read.csv('../data/histogram_color_representatives.csv', header = F,
                                    stringsAsFactors = F))
print("painting color histograms loaded")
# painting = read.csv('data/athenaeum_paintings.csv')
print("main tables loaded")

# data for painting type count
painting_type <- painting_sizes %>% group_by(article_type) %>%
  summarise(type_count = n()) %>%
  arrange(desc(type_count))
print("painting type counts loaded")

# data for top authors
author_painting <- merge(authors, painting_sizes, by=c("author_id"), all = FALSE)
top_authors <- author_painting %>% group_by(author_id, last_name) %>%
  summarise(num_work = n()) %>%
  arrange(desc(num_work)) %>%
  head(20)
print("top authors data loaded")

# data for nationality
author_num_work <- author_painting %>% group_by(author_id) %>%
  summarise(num_works = n())
author_painting <- merge(author_num_work, author_painting, by=c("author_id"), all = FALSE)
nations <- author_painting %>% group_by(nationality) %>%
  summarise(num_authors = n(), num_paintings = sum(num_works)) %>%
  arrange(desc(num_paintings)) %>%
  head(30)
print("nationality data loaded")

# data for media
medias <- author_painting %>% group_by(medium) %>%
  summarise(num_paintings = n()) %>%
  arrange(desc(num_paintings)) %>%
  head(20)
print("media data loaded")

# data for painting samples
type_col <- unlist(painting_type %>% select(article_type))
names(type_col) <- NULL
print("painting samples prepared")

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
print("k-means data loaded")

KmeansPainting <- function(label, num_paintings = 10) {
  return(kmeans_data %>% filter(kmeans_labels == label) %>%
           arrange(distance_to_centroid) %>% head(num_paintings))
}


# geolocation map
geolocation <- read.csv('../data/geolocation_map.csv') %>% na.omit() %>%
  arrange(desc(num_paintings))
# geolocation <- geolocation %>% na.omit() %>% mutate(
#   latlon = sprintf("%.2f:%.2f", as.numeric(latitude), as.numeric(longitude)))
# geolocation['latlon'] = apply(geolocation, 1, function(row) {
#   sprintf("%.2f:%.2f", as.numeric(row['latitude']), as.numeric(row['longitude']))
# })
print("locations map data loaded")

# data for predictions game
painting_predictions <- read.csv('../data/net1_ensemble_stacking_table.csv')
predictions_authors <- painting_predictions %>% select(author_id) %>% unique() %>%
  inner_join(authors, by = 'author_id') %>%
  mutate(pretty_name = paste(last_name, first_name, sep = ', '))
predictions_choices <- c(predictions_authors$author_id)
names(predictions_choices) <- predictions_authors$pretty_name
print("predictions game data loaded")

image_path <- function(author_id, painting_id) {
  return(paste0('../data/images_athenaeum/full/', author_id, '/', painting_id, '.jpg'))
}
image_path_html <- function(author_id, painting_id) {
  return(paste0('images/', author_id, '/', painting_id, '.jpg'))
}

game_answer_message <- function(author_id, correct = F) {
  if(correct) {
    return('<p style = "color:green;">You guessed right!</p>')
  } else {
    author_id_ <- author_id
    return(paste0('<p style = "color:red;">You guessed wrong! The correct painter was ',
                 (predictions_authors %>%
                    filter(author_id == author_id_) %>%
                    select(pretty_name))[[1,1]], '!</p>'))
  }
}

get_sample_painting_histogram <- function() {
  return(unlist(color_hist %>% sample_n(1)))
}