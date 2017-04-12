

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
  
  # Painting Locations
  # output$paintingLoc <- renderGvis({
  #   gvisMap(geolocation,locationvar="latlon",tipvar="location_str",
  #                    options=list(displayMode = "Markers", 
  #                                 mapType='normal', 
  #                                 colorAxis = "{colors:['red', 'grey']}",
  #                                 useMapTypeControl=TRUE, enableScrollWheel=TRUE))
  #   
  # })
  
  output$paintingLoc <- renderLeaflet({
    color_map <- colorNumeric('BrBG', log(geolocation$num_paintings))
    leaflet(geolocation) %>% addTiles() %>%
      addCircles(lng = ~longitude, lat = ~latitude, weight = 0,
                 radius = ~sqrt(num_paintings) * 1000,
                 popup = ~paste0(location_str, '<br>', num_paintings, ' paintings'),
                 fillColor = ~color_map(log(num_paintings)),
                 #color = ~color_map(log(num_paintings)),
                 opacity = 1,
                 fillOpacity = 0.6)
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
    kmean_painting <- KmeansPainting(input$label, input$kmeans_num_paintings)
    
    outKHtml <- "<div class=\"sample-wrapper\">"
    # outKHtml <- paste0(outKHtml, "<p>", nrow(kmean_painting), "</p>")
    for(i in 1:nrow(kmean_painting)) {
      outKHtml <- paste0(outKHtml, "<div class=\"cell\"><image src=\"",
                        image_path_html(kmean_painting$author_id[i], kmean_painting$painting_id[i]),
                        "\" class = \"sample-sizes\"></div>")
    }
    paste0(outKHtml, "</div>")
  })
  
  #############################
  # Paintings color histogram #
  #############################
  cur_histogram_painting <- reactiveValues(hist = get_sample_painting_histogram())
  
  observeEvent(input$histogram_reset, {
    cur_histogram_painting$hist <- get_sample_painting_histogram()
  })
  
  output$painting_color_hist <- renderImage({
    list(src = image_path(cur_histogram_painting$hist['author_id'],
                          cur_histogram_painting$hist['painting_id']),
         filetype = 'image/jpeg')
  }, deleteFile = FALSE)
  
  output$colorHistPaintingDesc <- renderText({
    painting_record <- painting_sizes %>%
      filter(author_id == cur_histogram_painting$hist['author_id'],
             painting_id == cur_histogram_painting$hist['painting_id']) %>%
      select(author_id, painting_title) %>%
      inner_join(authors %>% select(author_id, first_name, last_name), by = 'author_id')
      
    result <- paste0('<p><strong>Author:</strong> ', painting_record[[1, 'last_name']])
    if(!is.null(painting_record[[1, 'first_name']]) &&
       length(painting_record[[1, 'first_name']]) > 0) {
      result <- paste0(result, ', ', painting_record[[1, 'first_name']])
    }
    result <- paste0(result, '<br><strong>Title:</strong> ',
                     painting_record[[1, 'painting_title']],
                     '</p>')
  })
  
  color.hist.options <- list(bar = '{groupWidth: "100%"}',
                             legend = '{ position: "none" }',
                             hAxis = '{textPosition: "none"}',
                             vAxis = '{textPosition: "none", gridlines: {count: 0}}',
                             backgroundColor = '{fill: "transparent"}',
                             theme = 'maximized',
                             titlePosition = 'in'
                             #chartArea = '{left:"3%",top:"3%",width:"94%",height:"94%"}'
                             )
  
  output$colorHuePlot <- renderGvis({
    to.plot <- data.frame(x = 1:20,
                          frequency = cur_histogram_painting$hist[3:22],
                          frequency.style = color_hist_repr[1:20])
    gvisColumnChart(to.plot, xvar = 'x', yvar = c('frequency', 'frequency.style'),
                    options = c(color.hist.options,
                                list(title = 'Hue',
                                     height = 200)))
  })
  
  output$colorSatPlot <- renderGvis({
    to.plot <- data.frame(x = 1:5,
                          frequency = cur_histogram_painting$hist[23:27],
                          frequency.style = color_hist_repr[21:25])
    gvisColumnChart(to.plot, xvar = 'x', yvar = c('frequency', 'frequency.style'),
                    options = c(color.hist.options,
                                list(title = 'Saturation',
                                     height = 100)))
  })
  
  output$colorValPlot <- renderGvis({
    to.plot <- data.frame(x = 1:5,
                          frequency = cur_histogram_painting$hist[28:32],
                          frequency.style = color_hist_repr[26:30])
    gvisColumnChart(to.plot, xvar = 'x', yvar = c('frequency', 'frequency.style'),
                    options = c(color.hist.options,
                                list(title = 'Value',
                                     height = 100)))
  })
  
  #########################
  # Painter guessing game #
  #########################
  cur_painting <- reactiveValues(painter = -1, painting = -1, prediction = -1)
  
  game_state <- reactiveValues(user_guessed = 0, model_guessed = 0, total_attempts = 0,
                               message = NULL)
  
  observeEvent(game_state$total_attempts,{
    new_painting <- painting_predictions %>%
      select(author_id, painting_id, predicted_author) %>%
      sample_n(1)
    cur_painting$painter <- new_painting[[1,1]]
    cur_painting$painting <- new_painting[[1,2]]
    cur_painting$prediction <- new_painting[[1,3]]
  })
   
   output$painting_to_guess <- renderImage({
     if(cur_painting$painting == -1) {
       return(NULL)
     }
     list(src = image_path(cur_painting$painter, cur_painting$painting),
          filetype = 'image/jpeg')
   }, deleteFile = FALSE)
   
   output$game_points <- renderText({
     if(game_state$total_attempts == 0) {
       return('<p align = "right"><strong>No attempts made</strong></p>')
     } else {
       return(paste0('<p align = "right"><strong>User: ', game_state$user_guessed, '/',
                     game_state$total_attempts, ' (',
                     round(game_state$user_guessed / game_state$total_attempts * 100),
                     '%)<br>Our model: ', game_state$model_guessed, '/',
                     game_state$total_attempts,' (',
                     round(game_state$model_guessed / game_state$total_attempts * 100),
                     '%)</strong></p>'))
     }
   })
   
   observeEvent(input$game_select, {
     game_state$message = game_answer_message(cur_painting$painter,
                                              input$game_option == cur_painting$painter)
     if(input$game_option == cur_painting$painter) {
       game_state$user_guessed <- game_state$user_guessed + 1
     }
     if(cur_painting$prediction == cur_painting$painter) {
       game_state$model_guessed <- game_state$model_guessed + 1
     }
     game_state$total_attempts <- game_state$total_attempts + 1
   })
   
   output$game_message <- renderText({
     paste(game_state$message, cur_painting$painter, cur_painting$painting)
   })
})
