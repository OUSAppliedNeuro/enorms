from statistics import mean, stdev, median, variance
import numpy as np

### @Author Tomasz Szczepanski
###
### Python library of various generalizable functions.

### Method for computing useful statistical properties of a dataset.
def get_statistics(a_dataset):
    i_mean = mean(a_dataset)
    i_sd = stdev(a_dataset)
    t_rf = (i_mean - 2*i_sd, i_mean + 2*i_sd) # traditional way of computing medical reference limits
    i_median = median(a_dataset)
    i_q3, i_q1 = np.percentile(a_dataset, [75 ,25])
    i_iqr = i_q3 - i_q1
    return i_mean, i_sd, t_rf, i_median, i_q1, i_q3, i_iqr

### Returns the number of items in a dataset that has the value less than i_cutoff.
def get_n_less_than_from_set(a_dataset, i_cutoff):
    i_n = 0
    for i in a_dataset:
        if i < i_cutoff:
            i_n += 1
    return i_n

### Converts a ordered list of numbers into a ordered moving-statistic-list with the specified window size i_window and statistic s_statistics.
###
### s_statistics=None -> mean is used on the window data
### s_statistics="var" -> variance is used on the window data
def get_moving_average(a_dataset, i_window, s_statistics=None):
    a_average = []
    if i_window < 1:
        print("warning in Tools.get_moving_average - window size less than 1")
        for i in a_dataset:
            a_average.append(0)
        return a_average
    if i_window > len(a_dataset):
        print("warning in Tools.get_moving_average - window size greater than len(dataset)")
        for i in a_dataset:
            a_average.append(0)
        return a_average
    i_counter = 0
    while i_counter < round((i_window-1)/2):
        a_average.append(0)
        i_counter += 1
    i_counter = 0
    while i_counter < len(a_dataset)-(i_window-1):
        sum = 0
        a_bucket = []
        i_counter_inner = 0
        while i_counter_inner < i_window:
            sum += a_dataset[i_counter+i_counter_inner]
            a_bucket.append(a_dataset[i_counter+i_counter_inner])
            i_counter_inner += 1
        if s_statistics is None:
            a_average.append(sum/i_window)
        elif s_statistics == "var":
            a_average.append(variance(a_bucket))
        i_counter += 1
    while len(a_average) < len(a_dataset):
        a_average.append(0)
    return a_average