#!/usr/bin/env python

from graphs import graphs
from graphs import graph_selection
from data_generation import data_generation
from info import info
from ai_models import model_choice
from ExploratoryDataAnalysis import eda
from simulation import Main_function

file_location = input("Where have you saved the non-master data? ")

data_generation(file_location)

function = ''


while function != "stop":
    print("This is case-sensitive! \n\n Type G for graph function \n\n I for variable information \n\n A for AI modelling"
          "\n\n E for eda \n\n S for simulation, or T for graph test "
          "or type stop to quit the program")
    function = input("What do you want to do? ")
    print(f'Input was {function}')
    if function == "G":
        graphs(file_location)
        continue
    if function == "T":
        graph_selection(file_location)
        continue
    if function == "I":
        info(file_location)
        continue
    if function == "A":
        model_choice(file_location)
        continue
    if function == "E":
        eda(file_location)
        continue
    if function == "S":
        Main_function()
        continue
    if function == "stop":
        print("Stopping")
        break
    else:
        print("Invalid input")
        continue

