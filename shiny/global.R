library(googleVis)
library(shiny)
library(ggplot2)
library(dplyr)
library(shinydashboard)


# Author
authors = read.csv('../data/athenaeum_authors.csv')
painting_sizes = read.csv('../data/athenaeum_paintings_sizes.csv')
# painting = read.csv('../data/athenaeum_paintings.csv')

# data for painting type count
painting_type <- painting_sizes %>% group_by(article_type) %>%
  summarise(count = n()) %>%
  arrange(desc(count))
 
# data for painting samples
type_col <- unlist(painting_type %>% select(article_type))
names(type_col) <- NULL

# function(article_type) {
#   sample_painting = paintings[paintings['article_type'] == article_type].sample(8)
# 
# }
# 
# sample_painting = paintings[paintings['article_type'] == article_type].sample(8)
# 
# par(mfrow=c(2,2))
# plot(wt,mpg, main="Scatterplot of wt vs. mpg")
# plot(wt,disp, main="Scatterplot of wt vs disp")
# hist(wt, main="Histogram of wt")
# boxplot(wt, main="Boxplot of wt")
# 
# 
# f, ax = plt.subplots(2, 4, figsize = (18,9))
# for i in range(8):
#   im = Image.open('data/images_athenaeum/full/%d/%d.jpg' % (sample_painting.iloc[i]['author_id'],
#                                                             sample_painting.iloc[i]['painting_id']))
# curAxis = ax[i / 4, i % 4]
# curAxis.imshow(im)
# curAxis.set_xticks([])
# curAxis.set_yticks([])
# In [16]:
  








 
image_path <- function(author_id, painting_id) {
  return(paste0('../data/images_athenaeum/full/', author_id, '/', painting_id, '.jpg'))
}
