library(dplyr)
library(shiny)
library(shinydashboard)


authors <- read.csv('../data/athenaeum_authors.csv')

paintings <- read.csv('../data/athenaeum_painting_filtered.csv')

image_path <- function(author_id, painting_id) {
  return(paste0('../data/images_athenaeum/full/', author_id, '/', painting_id, '.jpg'))
}
