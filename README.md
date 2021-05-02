# EGM722 Final Assingment Programming for GIS and Remote Sensing

This is where you start

## Overview 

The following code will provide various information about Crete island such as attribute tables, calculations, and map visualization 

in features

*   Object oriented
*   Geopandas DataFrame, Pandas, Cartopy, Matplotlib, Contextily
*   Functions, Methods, Objects
*   Polygons, Lines, Points, transformation and map projection 
*   Vector data analysis and Geopandas capabilities with shapefiles 

Documentations can be found:

*   Geopandas  [details here](https://geopandas.org/docs.html)
*   Pandas     [details here](https://pandas.pydata.org/docs/)
*   Cartopy    [details here](https://scitools.org.uk/cartopy/docs/latest/)
*   Matplotlib [details here](https://matplotlib.org/stable/contents.html#)
*   Contextily [details here](https://contextily.readthedocs.io/en/latest/intro_guide.html)

## 1. Installations and conda environment

1.1 Getting started download 'Conda' on your local computer to set the `environment.yml` provided above. First, [click here](https://docs.anaconda.com/anaconda/install/) to download the 'anaconda' and while you have done the installation open 'anaconda navigator' and on the left side screen click 'Environments'.  On the bottom-left of your screen click the 'import' and add a 'Name' and for 'Specification File' add the environment.yml which have been provided and click import. While is done more than 160 packages should be added to your environment ![](../E:/GIS/GIS_Practicals/GIS_Course EGM722/Practicals/GitHub/image1)

1.2 Another option is to run the command prompt from the anaconda navigator in order to get access to the anaconda environment. Navigate to cmd and type the following command:
 `(NataliSuportman) C:\Users\NataliSuportman> conda env create -f environment.yml`

1.3 For the python code, the PyCharm IDE recommended and can be found [here](https://www.jetbrains.com/pycharm/)

1.4 To get the GitHub Desktop for windows or mac [click here](https://desktop.github.com/)

1.5 For contextily package launch anaconda environment and run the cmd to your environment base. Type "conda install contextily" or "conda install –c conda-forge contextily" . For running issues such as channel not installed, type a new command "conda config –appened channels conda-forge" and try again "conda install contextily. Final option type "contextily==1.0rc2 ". For cotextily dependecies [click here](https://contextily.readthedocs.io/en/latest/) 

1.6 If you are unfamiliar with PyCharm and you want to observe each DataFrame 

## 2. Download or clone this repository

You can download this repository after installations or clone to your main computer following the steps

1.  Go upper to green 'code', open and select Download ZIP to your local computer. Once you have downloaded unzip the file and double click the final_assignment_egm722.py to observe the code 

2.  On the upper right window, you will find the 'Fork' button, click to create a fork this repository to your account. Once is done open the GitHub Desktop and from 'File' select 'Clone a repository', copy this URL: `gh repo clone NataliSupportMan/Final_Assignment_EGM722` and paste it to your GitHub Desktop URL, choose the local path and final push the clone button.                           

Overall step 1 is recommended in order to observe and work with this code but you can go for option 2 and fork this repository to your account