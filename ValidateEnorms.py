import numpy as np
import matplotlib.pyplot as plt
import EnormsDashboard

### @Author: Tomasz Szczepanski
### 
### Script for validating the E-norms algorithm on historical neurophysiological data.
###
###
### Produces a csv file with the following output:
###
### dataset:        description of the dataset
### mean:           mean calculated from the transformed dataset
### sd:             standard deviation calculated from the transformed dataset
### median:         median calculated from the transformed dataset
### iqr:            interquartile range calculated from the transformed dataset
### n:              number of datapoints in the plateau set selected from the e-norms method
### best_transform: best transformation to normalize the dataset according to the Shaphiro test
### ref_lim_2sd:    reference limit calculated using mean +/- 2sd
### disease_%_2sd:  % patients classified as diseased by the ref_lim_2sd reference limit
### ref_lim_2sd:    reference limit calculated using mean +/- 2.5sd
### disease_%_2sd:  % patients classified as diseased by the ref_lim_25sd reference limit
### ref_lim_2sd:    reference limit calculated using mean +/- 3sd
### disease_%_2sd:  % patients classified as diseased by the ref_lim_3sd reference limit
### coord_x1:       position of the left most line in the e-norms method
### coord_x2:       position of the right most line in the e-norms method






### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
###                                                   USER EDIT START                                                   ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

### Using this script you need to define an output result file:
s_csv_results = "X:/path/to/file/results.csv"

### You also need a list of numbers for the e-norms method and a small text describing the list (without ","):
s_user_list_title = "Example title for current dataset"
a_user_list = np.random.normal(50, 4, 1000)

### Lastly, you need to define if the reference limit should be "greater than" or "less than".
### conduction velocity or amplitudes are typically "less than" reference limits (small values = pathology)
### latency is typically a "more than" reference limit (high values = pathology)
b_greater_than = False 

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
###                                                    USER EDIT END                                                    ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 






### Runs the e-norms method
def run(s_title, a_list, b_lat):
    f_results = open(s_csv_results, 'a')
    ### Write the first line to the results csv file
    f_results.write('dataset,mean,sd,median,iqr,n,best_transform,ref_lim_2sd,disease_%_2sd,ref_lim_25sd,disease_%_25sd,ref_lim_3sd,disease_%_3sd,coord_x1,coord_x2\n')
    fig, ax = plt.subplots(1, 1)
    s_result = s_title+","
    s_result += EnormsDashboard.draw(s_title, b_lat, a_list, fig, ax)
    f_results.write(s_result+"\n")
    f_results.close()

run(s_user_list_title, a_user_list, b_greater_than)