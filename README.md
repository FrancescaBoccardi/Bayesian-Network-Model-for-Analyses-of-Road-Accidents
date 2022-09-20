# Bayesian-Network-Model-for-Analyses-of-Road-Accidents

Road traffic injuries represent an important public health problem. Preventive strategies are 
one of the most effective methods in reducing the number of road accidents and, as a consequence,
of injuries. For the purpose of analyzing road accidents causes, the Bayesian network is a powerful
tool, able to predict the probability of injuries in certain road traffic conditions and to find the
critical states combination which may leads to unsafe situations. 

This repository contains a model for road accidents, formulated through a Bayesian network, starting from a suitable data set.
Then, some inferential analyses on accident severities have been conducted, using both exact and approximate inference methods. 

## Repository structure

````
.
├── dataset                      
|   ├── data.csv                        # Final dataset
├── resources                      
|   ├── crashdata2021.csv               # Original dataset about car accidents
|   ├── vehiclecrashdata2021.csv        # Original dataset about vehicles and drivers involved      
├── src                      
|   ├── Road_Accidents_BN.ipynb         # Bayesian Network implementation and analysis
|   ├── dataset_preprocessing.py        # .py file containing the preprocessing function
├── README.md
├── Report.pdf                          # Report of the whole project
````

In particular, ````Road_Accidents_BN.ipynb```` is a Jupiter Notebook containing the whole work's code, with brief comments to help understanding the different steps. 
Firstly, ````crashdata2021.csv```` and ````vehiclecrashdata2021.csv```` datasets have been manipulated and merged through the 
preprocessing function, contained in ````dataset_preprocessing.py````, obtaining the final dataset ````data.csv````.
Then, the Bayesian Network model and the inferential analyses have been developed. 

The entire project is presented and explained in ````Report.pdf```` file.

## Requirements

In order to successfully reproduce the results on ````Road_Accidents_BN.ipynb```` notebook, the following installations are required:

* [Python](https://www.python.org/)
* [pgmpy](https://pgmpy.org/)
* [NumPy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/)
* [pandas](https://pandas.pydata.org/)
* [pathlib](https://pypi.org/project/pathlib/)
* [NetworkX](https://networkx.org/)

## Authors

The project has been realized by:

* Francesca Boccardi ([FrancescaBoccardi](https://github.com/FrancescaBoccardi))
* Luigi Podda ([lupodda](https://github.com/lupodda))
