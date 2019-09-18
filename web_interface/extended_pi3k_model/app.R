#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(ggplot2)
library(stringi)
library(Stack)

#install.packages('Stack')



#todo use the instructions to build a
#  dynamic UI (https://shiny.rstudio.com/articles/dynamic-ui.html)


# APP_DIR = file.path(WEB_DIR, 'extended_pi3k_model')
APP_DIR = getwd() # /home/ncw135/Documents/QualitativeModelFitting/web_interface/extended_pi3k_model
WEB_DIR = file.path(dirname(APP_DIR))
WD = dirname(WEB_DIR)
# WD = '/home/ncw135/Documents/QualitativeModelFitting'


MODEL_DIR = file.path(WD, 'example_networks')
NETWORK_FNAME = file.path(WEB_DIR, 'network.png')
NETWORK_FNAME
SIMULATION_SCRIPT = file.path(WEB_DIR, 'run_timeseries.py')
# PYTHON_PATH = "/home/ncw135/miniconda3/envs/py36/bin/python"
PYTHON_PATH = "python"
DATA_FILENAME = file.path(WD, 'data_file.csv')
PLOTTABLE_SPECIES = file.path(WEB_DIR, 'plottable_species.txt')

DEFAULT_OUTPUTS = c('TSC2', 'pmTORC1', 'TSC2_Rag')

print('working dir is')
print(getwd())
# check filenames exist
for (i in c(SIMULATION_SCRIPT, NETWORK_FNAME,
            PYTHON_PATH, DATA_FILENAME, 
            PLOTTABLE_SPECIES)) {
  if (!file.exists(i)) {
    message(paste(i, 'does not exist'))
  }
}

# check directories exist
directories = c(WD, MODEL_DIR, WEB_DIR, APP_DIR)
for (i in directories) {
  if (!dir.exists(i)) {
    message(paste('warning: ', i, 'does not exist'))
  }
}

get_data = function(start, stop, step, inputs) {
  inputs_vec = as.vector(unlist(inputs))
  inputs_names = names(inputs)
  string = ''
  for (i in 1:length(inputs)) {
    s = paste0(inputs_names[i], '=', inputs_vec[i])
    if (string == '') {
      string = s
    } else{
      string = paste(string, s)
    }
  }
  str = paste(
    PYTHON_PATH,
    SIMULATION_SCRIPT,
    start,
    stop,
    step,
    '--file',
    DATA_FILENAME,
    '-i',
    string
  )
  message('string passed to python "', str, '"')
  system(str)
  data = read.csv(DATA_FILENAME)
  return (data)
  
}
plottable_species = read.csv(PLOTTABLE_SPECIES)
plottable_species = as.character(plottable_species[, 1])

#get_data(0, 100, 101, list(Insulin=1, AA=1))

# Define UI for application that draws a histogram
ui <- fluidPage(
  theme = 'cyborg.css',
  
  # Application title
  titlePanel("Extended PI3K Model Simulations"),
  
  fluidRow(column(12,
                  wellPanel(
                    checkboxGroupInput(
                      'input_checkboxes',
                      'Inputs',
                      choices = c(
                        'Insulin',
                        'AA',
                        'EGF',
                        'Rapamycin',
                        'Wortmannin',
                        'MK2206',
                        'Ca2',
                        'AZD',
                        'PMA'
                      ),
                      selected = c('Insulin', 'AA'),
                      inline = T
                    )
                  ))),
  
  fluidRow(
    column(2, 
           textAreaInput('inputs_text', label = 'Inputs', rows = 7, value = 'Insulin = 1\nAA = 1'),
           selectizeInput('output_selection', label = 'Outputs', 
                          selected = DEFAULT_OUTPUTS, 
                       choices = plottable_species, multiple = T, 
                       options = list(
                         selectOnTab = T
                       )) 
    ),
    column(10, plotOutput('plot_output'))
    ),
  fluidRow(
    column(3, textInput(
        'start', label = 'Start', value = 0
      )),
      column(3, textInput(
        'stop', label = 'Stop', value = 100
      )),
      column(3, textInput(
        'step', label = 'Step',  value = 101
      )),
      column(3, actionButton('go_btn', 'Simulate', width = 100))
    ),
  fluidRow(
    column(2,
           actionButton('mTORC1Output', 'mTORC1 Output'))
  ),
  fillRow(column(12, imageOutput("network_image")))
)



# Define server logic required to draw a histogram
server <- function(input, output, session) {
  output$network_image <- renderImage({
    fname = NETWORK_FNAME
    list(src = fname, alt = paste("Network"))
  }, deleteFile = F)
  
  observe({
    input_string = ''
    for (i in input$input_checkboxes) {
      if (input_string == '') {
        input_string = paste0(i, ' = 1')
      }
      else {
        input_string = paste0(input_string, '\n', i, ' = 1')
      }
    }
    updateTextAreaInput(session, "inputs_text", value = input_string)

  })
  

  
  
  data_input = eventReactive(input$go_btn,
                             
                             {
                               inputs_string = stri_split_lines1(input$inputs_text)
                               # print('here')
                               # print(inputs_string)
                               # print(class(inputs_string))
                               inputs_list = list()
                               for (i in inputs_string){
                                 split_input = strsplit(i, '=')
                                 k = trimws(split_input[[1]][1])
                                 v = trimws(split_input[[1]][2])
                                 v = as.integer(v)
                                 inputs_list[k] = v
                               }
                               print(inputs_list)
                               get_data(
                                 start = input$start,
                                 stop = input$stop,
                                 step = input$step,
                                 inputs = inputs_list
                               )
                             }, ignoreNULL = FALSE)
  mTOR_outputs = eventReactive(inputs$mTORC1Output, {
      mtorc1_output = c('pmTORC1', 'mTORC1Cyt', 'mTORC1Lys')
    observe({
      updateSelectizeInput(session, 'output_selection', selected = mtorc1_output)
    })
  })
  
  output$plot_output = renderPlot({
    
    df = data_input()
    time = data_input()$time
    data = df[, input$output_selection]
    data2 = df[,c('time', input$output_selection)]
    # print(df)
    # print(stack(data2))
    # print(data2)
    data = reshape::melt(data = data2, id = 'time')
    colnames = c('time', 'Variable', 'Amount (AU)')
    # ggplot(data = data_input(), aes(x = time, y = IRS1)) + geom_line(size = 2) +
    ggplot(data = data, aes(x = time, y = value, colour = variable)) + geom_line(size = 2) +
      theme_bw() +
      theme(
        plot.background = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        text = element_text(size = 20)
        
      ) +
      theme(axis.line = element_line(color = 'black'))
  })
  
  
  
  # output$table_output = renderTable({data_input()})
  
}

# Run the application
shinyApp(ui = ui, server = server)
