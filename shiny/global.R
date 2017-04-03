library(googleVis)
library(shiny)
library(ggplot2)
library(dplyr)
library(shinydashboard)


# Author
authors = read.csv('../data/athenaeum_authors.csv')
painting_sizes = read.csv('../data/athenaeum_paintings_sizes.csv')

ggplot(painting_sizes, aes(x = log2(height)-log2(width))) + 
  stat_density(geom = 'line') +
  # coord_cartesian(xlim=c(-2, 2)) +
  xlab('') +
  ggtitle('Distribution of Log-Ratio between Height and Width of images')

image_path <- function(author_id, painting_id) {
  return(paste0('../data/images_athenaeum/full/', author_id, '/', painting_id, '.jpg'))
}
