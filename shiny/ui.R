
shinyUI(dashboardPage(
  skin = "green",
  # Application title
  dashboardHeader(title = "Ink Scrapers"),
  
  # Sidebar with a slider input for number of bins 
  dashboardSidebar(sidebarMenu(id="sideBarMenu",
               menuItem("ReadMe", tabName = "readme", icon = icon("mortar-board"), selected=TRUE
               ),                
               menuItem("Data Exploration", tabName = "xplore", icon = icon("bar-chart-o"),
                        menuSubItem("Raw Data", tabName = 'rawDataPlt')),
               menuItem("Who painted this?", tabName = "game", icon = icon("gamepad")),
               menuItem("Exploring similarities", tabName = "kmeans", icon = icon("picture-o")))),
  dashboardBody(
    tabItems(
      tabItem(tabName = "xplore",
              "Introduction"),
      tabItem(tabName = "game",
              h2("Who painted this?"),
              p("If you know a thing or two about paintings, it's time to put your skills to the test,
                by comparing yourself with the machine learning model we developed."),
              htmlOutput("points"),
              tags$head(tags$style(
                type="text/css",
                "#painting img {max-height: 400px; max-width: 100%; height: auto, width: auto}"
              )),
              fixedRow(column(8, imageOutput("painting")),
                       column(4,
                              p("radio buttons")))),
      tabItem(tabName = "kmeans",
              "K-means"))
  )
  
  
))
