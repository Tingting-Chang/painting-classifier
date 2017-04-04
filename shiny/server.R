

shinyServer(function(input, output) {
  
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
                                               height = 500,
                                               title="Number of paintings per type",
                                               titleTextStyle="{color:'green',fontName:'Courier',fontSize:16}"))
  })
  
  # top 20 authors
  output$topauthors <- renderGvis({
    gvisBarChart(top_authors,
                 xvar = "last_name",
                 yvar = "num_work",
                 options = list(hAxis = "{logScale: true}",
                                height = 500,
                                title="Number of paintings per author",
                                titleTextStyle="{color:'green',fontName:'Courier',fontSize:16}"))
  })
  
  # num of authors & paintings per nationality
  output$nations <- renderGvis({
    gvisBarChart(nations,
                 xvar = "nationality",
                 yvar = c("num_authors", "num_paintings"),
                 options = list(hAxis = "{logScale: true}",
                                height = 500,
                                title="Number of paintings and authors per nationality",
                                titleTextStyle="{color:'green',fontName:'Courier',fontSize:16}"))
  })
  
  # num of  paintings per media
  output$medias <- renderGvis({
    gvisBarChart(medias,
                 xvar = "medium",
                 yvar = c("num_paintings"),
                 options = list(hAxis = "{logScale: true}",
                                height = 500,
                                title="Most frequent art media",
                                titleTextStyle="{color:'green',fontName:'Courier',fontSize:16}"))
  })
  
  # Painting Samples
  output$paintPlt <- renderText({
    if(input$type == '') {
      return(paste0("<p>Please select an art type</p><image src=\"", image_path_html(13, 4010),"\" class=\"default-image\">"))
    }
    sample_painting <- SamplePainting(input$type)
    #list(src = image_path(sample_painting$author_id, sample_painting$painting_id))
    #list(src = sample_painting$painting_url, filetype = 'image/jpeg')
    outHtml <- "<div class=\"sample-wrapper\">"
    for(i in 1:nrow(sample_painting)) {
      outHtml <- paste0(outHtml, "<div class=\"cell\"><image src=\"",
                        image_path_html(sample_painting$author_id[i], sample_painting$painting_id[i]),
                        "\" class = \"sample-sizes\"></div>")
    }
    paste0(outHtml, "</div>")
    
  })
  
  # Painting Kmeans
  output$kmeansPlt <- renderText({
    kmean_painting <- KmeansPainting(input$label)
    
    outHtml
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
