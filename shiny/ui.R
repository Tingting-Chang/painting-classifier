#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(shinydashboard)

# Define UI for application that draws a histogram
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
              "Game"),
      tabItem(tabName = "kmeans",
              "K-means"))
  )
  
  
))
