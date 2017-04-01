

shinyServer(function(input, output) {
   cur_painter <- -1
   cur_painting <- -1
   
   generate_painting <- function() {
     new_painting <- paintings %>% select(author_id, painting_id) %>% sample_n(1)
     cur_painter <<- new_painting[[1,1]]
     cur_painting <<- new_painting[[1,2]]
   }
   
   output$painting <- renderImage({
     if(cur_painter == -1 || cur_painting == -1) {
       generate_painting()
     }
     list(src = image_path(cur_painter, cur_painting),
          filetype = 'image/jpeg')#,
          # width = '100%')
   })
   
   output$points <- renderText({
     if(cur_painter == -1 || cur_painting == -1) {
       generate_painting()
     }
     paste(cur_painter, cur_painting)
   })
})
