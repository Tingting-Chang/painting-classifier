library(googleVis)
library(shiny)
library(ggplot2)

# Author
authors = read.csv('data/athenaeum_authors.csv')
painting_sizes = read.csv('data/athenaeum_paintings_sizes.csv')

names(authors)
names(painting_sizes)

ggplot(painting_sizes, aes(x = log2(height)-log2(width))) + 
  stat_density(geom = 'line') +
  coord_cartesian(xlim=c(-2, 2)) +
  xlab('') +
  ggtitle('Distribution of Log-Ratio between Height and Width of images')
