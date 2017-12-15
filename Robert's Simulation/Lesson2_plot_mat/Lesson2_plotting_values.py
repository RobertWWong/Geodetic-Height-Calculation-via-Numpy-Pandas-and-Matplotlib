import numpy as np # This library is necessary to create a matrix for operations
import matplotlib.pyplot as plot # This is necessary to control the Figure() object that our plot will create.
from mpl_toolkits.mplot3d import Axes3D #This is necessary to create a 3d model given the required datapoints (x,y,z)

from Lesson1_reading_writing import read_write_YSFIL_Mat #We will be reusing lesson 1 to convert files those with labels.

# Lesson 2 is about learning how to plot a 3d line given x, y, and z
'''
Lesson 2  will show another way to load and use a matrix with label names from header files
It will show you how to create vector columns for plotting purposes
It will show you how to create a 3D-plot given the required datapoints
'''
# Global file of importance
f1 = 'YSFIL_Mat_Label.txt'
f2 = 'YSMTHF_Mat_Label.txt'

def get_matrix_from_file(text_file : str):
    '''
    This function will return a matrix from a properly formatted file
    The return type is a matrix that is accessible through header name or index notation
    i.e. matrix['Time'] or matrix[:][0]
    But not matlab notation ie matrix[0,1]
    '''
    # asc_matrix = np.loadtxt(text_file , skiprows=0)   #This is the original way to load a file into a matrix
    asc_matrix = np.genfromtxt(fname=text_file, dtype=float, names= True)
    return asc_matrix

def plot_matrix(file_to_use : str, line_width :float =1.0):
    '''
    This function will plot a diagram of pE vs pF vs pG
    It will load a file into matrix form first

    Important introduction of the Axes3D function from the mpl_toolkits.mplot3d library
    We will define the size of our Figure
    Plot a line diagram of the datapoints
    And display the feature once complete with their
    '''

    # This statement will load a file into our matrix variable
    matrix = get_matrix_from_file("YSFIL_Mat_Label.txt")

    # These statements will pull the specific force E, F, and G
    pE= matrix["pE_f"]
    pF= matrix["pF_f"]
    pG= matrix["pG_f"]

    # Similar matlab conventions apply here
    fig = plot.figure(figsize=(7,7))    # This denotes a figure with dimensions W x L in inches on the screen

    # Important setup and drawing process
    ax = Axes3D # Reassigning the Axes3d function to the variable ax, which is important for drawing 3d diagrams
    ax = fig.add_subplot(111,projection = '3d') # This is the specific statement required to make our figure 3d

    # USE PLOT, IT IS A 3D LINE GRAPH. ANIMATION IS MUCH SMOOTHER OVER SCATTER PLOT
    # Python does not simulate 47k datapoints very well, on a 3d plane

    # There is a keyword argument label 'linewidth' which could help you with format size  if needed.
    ax.plot(pE,pF,pG, c='r', marker = 'o', linewidth =line_width)      # This statement calls the plot function to create a line diagrame of our datapoints

    ax.tick_params( labelsize =60)
    # Labeling our graph is done here
    ax.set_xlabel('pE Label')
    ax.set_ylabel('pF Label')
    ax.set_zlabel('pG Label')

    plot.show() # Here is a familiar function call

def init_file_headers():
    #This function will create a text file from our filter files with headers on them.

    # Small check to our directory to see if our header files already exists
    import os
    all_file_dir = os.listdir() #This function will import all the files and folders of our current directory
    file1 = 'YSFIL.ASC'
    file2 = 'YSMTHF.ASC'

    # If our files already exists, don't repeat making it.
    if not (f1 in all_file_dir):
        read_write_YSFIL_Mat(file1,True)
    if not (f2 in all_file_dir):
        read_write_YSFIL_Mat(file2,True)

def demo_graphing(fname, line_width):
    init_file_headers()
    plot_matrix(fname, line_width)

# f1 = 'YSFIL_Mat_Label.ASC'
# f2 = 'YSMTHF_Mat_Label.ASC'
demo_graphing(f2,0.3)
