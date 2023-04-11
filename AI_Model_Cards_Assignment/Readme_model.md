# Introduction

This code aims to analyze the neural values of a dataset and present them in a bar graph. The dataset used here is FairFace 1000 which is a facial image dataset. This code reads the neutral values of each image from an output text file and the age values from an Excel file. It then constructs a dictionary with age as keys and neutral values as values. Finally, the average of neutral values for each age group is calculated and plotted on a bar graph.

# Dependencies

- json
- pandas
- nsfw_detector
- matplotlib
- Installation

The required dependencies can be installed via `pip`. Run the following command in the terminal to install the dependencies:

`pip install json pandas nsfw_detector matplotlib`

# Usage

Place the `output.txt` file and `fairface_1000_label_train.xlsx` file in the same directory as the code file.

# Import the necessary libraries:

- import json
- import pandas as pd
- from nsfw_detector import predict
- import matplotlib.pyplot as plt

Run the code by executing it in the terminal or in an IDE.
The bar graph will be displayed, showing the average neutral values for each age group.

# Output

The output of this code is a bar graph showing the average neutral values for each age group.

# Note

The dataset used in this code is only an example, and the same code can be used with other datasets as well, with the necessary modifications to the input file names and formats.
