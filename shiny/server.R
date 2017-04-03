

shinyServer(function(input, output) {
  # Data for 
  # painting.sample <- reactive({
  #   painting_type %>% filter(article_type == input$type)
  # })
  
  
  # Raw Image
  output$hwratio <- renderPlot({
    ggplot(painting_sizes, aes(x = log2(height)-log2(width))) + 
      stat_density(geom = 'line') +
      coord_cartesian(xlim=c(-2, 2)) +
      xlab('') +
      ggtitle('Distribution of Log-Ratio between Height and Width')
  })
  output$imgtype <- renderGvis({
    gvisBarChart(painting_type, options = list(hAxis = "{logScale: true}",
                                               height = 300))
  })
  
  
  

   cur_painter <- -1
   cur_painting <- -1
   
   generate_painting <- function() {
     new_painting <- painting_sizes %>% select(author_id, painting_id) %>% sample_n(1)
     cur_painter <<- new_painting[[1,1]]
     cur_painting <<- new_painting[[1,2]]
   }
   
   output$painting <- renderImage({
     if(cur_painter == -1 || cur_painting == -1) {
       generate_painting()
     }
     
     list(src = image_path(cur_painter, cur_painting),
          filetype = 'image/jpeg')
   })
   
   output$points <- renderText({
     if(cur_painter == -1 || cur_painting == -1) {
       generate_painting()
     }
     paste0('<p align = "right"><strong>', cur_painter, ' ', cur_painting, '</strong></p>')
   })
})
