
shinyUI(dashboardPage(
  skin = "green",
  # Application title
  dashboardHeader(title = "Ink Scrapers"),
  
  # Sidebar with a slider input for number of bins 
  dashboardSidebar(sidebarMenu(id="sideBarMenu",
               menuItem("ReadMe", tabName = "readme", icon = icon("mortar-board"), selected=TRUE
               ),                
               menuItem("Data Exploration", tabName = "xplore", icon = icon("bar-chart-o"),
                        menuSubItem("EDA", tabName = 'rawDataPlt'),
                        menuSubItem("Painting Sample", tabName = 'paintingSam'),
                        menuSubItem("Painting Location", tabName = 'paintingLoc'),
                        menuSubItem("Color Histograms", tabName = 'colorHistograms')),
               menuItem("Exploring similarities", tabName = "kmeans", icon = icon("picture-o")),
               menuItem("Who painted this?", tabName = "game", icon = icon("gamepad")),
               menuItem("Github",icon = icon("github"),
                        badgeLabel = "Like", badgeColor = "green",
                        href = "https://github.com/Tingting-Chang/painting-classifier")
               ),
               hr(),
               conditionalPanel("input.sideBarMenu == 'paintingSam'",
                                selectizeInput(
                                  inputId = 'type',
                                  label = '',
                                  choices = type_col,
                                  options = list(
                                    placeholder = 'Select a type of paintings',
                                    onInitialize = I('function() { this.setValue(""); }')
                                    ))),
               conditionalPanel("input.sideBarMenu == 'kmeans'",
                               selectizeInput(
                                 inputId = 'label',
                                 label = 'Cluster',
                                 choices = label_col,
                                 options = list(
                                   placeholder = 'Select a label of clusters',
                                   onInitialize = I('function() { this.setValue(0); }')
                                 ),
                                 selected=0),
                               sliderInput("kmeans_num_paintings", label = "Number of paintings",
                                           min = 5, max = 50, value = 10))),
               
  dashboardBody(
    tags$head(
      tags$link(rel = "stylesheet", type = "text/css", href = "style.css")
    ),
    tabItems(
      tabItem(tabName = "readme",
              "Introduction"),
      tabItem(tabName = "rawDataPlt",
              fluidRow(
                tabBox( width = 12,
                        tabPanel(h5("Height and Width ratio of images"),
                                 plotOutput("hwratio")
                        ),
                        tabPanel(h5("Image counts per type"),
                                 htmlOutput("imgtype")),
                        tabPanel(h5("Top 20 authors"),
                                 htmlOutput("topauthors")),
                        tabPanel(h5("Per nationality"),
                                 htmlOutput("nations")),
                        tabPanel(h5("Frequent media"),
                                 htmlOutput("medias"))
                ))),
      tabItem(tabName = "paintingLoc",
              leafletOutput("paintingLoc")),
      tabItem(tabName = "paintingSam",
              htmlOutput("paintPlt")
              ),
      tabItem(tabName = "colorHistograms",
              h2("Color Histograms"),
              p("All our non neural network models based their predictions on the color
                histograms of paintings. It is therefore important to learn how these are
                generated, in order to properly understand the advantages and limitations
                of this process."),
              fluidRow(column(6, imageOutput("painting_color_hist")),
                       column(6, htmlOutput("colorHuePlot"),
                              htmlOutput("colorSatPlot"),
                              htmlOutput("colorValPlot"))),
              htmlOutput("colorHistPaintingDesc"),
              actionButton("histogram_reset", "New painting")),
      tabItem(tabName = "kmeans",
              "K-means",
              htmlOutput("kmeansPlt")),
      tabItem(tabName = "game",
              h2("Who painted this?"),
              p("If you know a thing or two about paintings, it's time to put your skills to the test,
                by comparing yourself with the machine learning model we developed."),
              fixedRow(column(8, imageOutput("painting_to_guess")),
                       column(4,
                              htmlOutput("game_points"),
                              radioButtons("game_option", "Select the author",
                                           predictions_choices),
                              actionButton("game_select", "Select"),
                              htmlOutput("game_message"))))
  )
  
  
)))
