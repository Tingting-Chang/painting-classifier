
shinyUI(dashboardPage(
  
  dashboardHeader(title = "Ink Scrapers"),
  
  dashboardSidebar(sidebarMenu(id="menu",
               menuItem("Data Exploration", tabName = "xplore", icon = icon("bar-chart-o")),
               menuItem("Who painted this?", tabName = "game", icon = icon("gamepad")),
               menuItem("Exploring similarities", tabName = "kmeans", icon = icon("paint-brush")))),
  dashboardBody(
    tabItems(
      tabItem(tabName = "xplore",
              "Introduction"),
      tabItem(tabName = "game",
              h2("Who painted this?"),
              p("If you know a thing or two about paintings, it's time to put your skills to the test,
                by comparing yourself with the machine learning model we developed."),
              p(strong(textOutput("points")), style = 'align:right'),
              fixedRow(column(8, imageOutput("painting", height = 800)),
                       column(4,
                              p("radio buttons")))),
      tabItem(tabName = "kmeans",
              "K-means"))
  )
))
