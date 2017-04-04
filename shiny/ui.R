
shinyUI(dashboardPage(
  skin = "green",
  # Application title
  dashboardHeader(title = "Ink Scrapers"),
  
  # Sidebar with a slider input for number of bins 
  dashboardSidebar(sidebarMenu(id="sideBarMenu",
               menuItem("ReadMe", tabName = "readme", icon = icon("mortar-board"), selected=TRUE
               ),                
               menuItem("Data Exploration", tabName = "xplore", icon = icon("bar-chart-o"),
                        menuSubItem("Raw Data", tabName = 'rawDataPlt'),
                        menuSubItem("Painting Sample", tabName = 'paintingSam')),
               menuItem("Who painted this?", tabName = "game", icon = icon("gamepad")),
               menuItem("Exploring similarities", tabName = "kmeans", icon = icon("picture-o")),
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
                                    ),
                                  selected=1)),
               onditionalPanel("input.sideBarMenu == 'kmeans'",
                               selectizeInput(
                                 inputId = 'label',
                                 label = '',
                                 choices = label_col,
                                 options = list(
                                   placeholder = 'Select a label of clusters',
                                   onInitialize = I('function() { this.setValue(""); }')
                                 ),
                                 selected=1))),
               
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
      tabItem(tabName = "paintingSam",
              htmlOutput("paintPlt")
              ),
      tabItem(tabName = "kmeans",
              "K-means",
              htmlOutput("kmeansPlt"))),
      tabItem(tabName = "game",
              h2("Who painted this?"),
              p("If you know a thing or two about paintings, it's time to put your skills to the test,
                by comparing yourself with the machine learning model we developed."),
              htmlOutput("points"),
              fixedRow(column(8, imageOutput("painting")),
                       column(4,
                              p("radio buttons"))))
  )
  
  
))
