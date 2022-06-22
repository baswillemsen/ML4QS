##############################################################
#                                                            #
#    Mark Hoogendoorn and Burkhardt Funk (2017)              #
#    Machine Learning for the Quantified Self                #
#    Springer                                                #
#    Chapter 2                                               #
#                                                            #
##############################################################

# Import the relevant classes.
from Chapter2.CreateDataset import CreateDatasets
from util_own.VisualizeDataset_own import VisualizeDataset_own
from util_own import util_own
from pathlib import Path
import copy
import os
import sys

# Chapter 2: Initial exploration of the dataset.

DATASET_PATH = Path('./datasets/own/')
RESULT_PATH = Path('./intermediate_datafiles_own/')
RESULT_FNAME = 'chapter2_result_own.csv'

# Set a granularity (the discrete step size of our time series data). We'll use a course-grained granularity of one
# instance per minute, and a fine-grained one with four instances per second.
GRANULARITIES = [15000, 100] # 60000 refers to 1 min and 250 refers to 0.25 second

# We can call Path.mkdir(exist_ok=True) to make any required directories if they don't already exist.
[path.mkdir(exist_ok=True, parents=True) for path in [DATASET_PATH, RESULT_PATH]]

print('Please wait, this will take a while to run!')

datasets = []
for milliseconds_per_instance in GRANULARITIES:
    print(f'Creating numerical datasets from files in {DATASET_PATH} using granularity {milliseconds_per_instance}.')

    # Create an initial dataset object with the base directory for our data and a granularity
    dataset = CreateDataset(DATASET_PATH, milliseconds_per_instance)

    # Add the selected measurements to it.

    # We add the accelerometer data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    dataset.add_numerical_dataset('accelerometer.csv', 'timestamps', ['x','y','z'], 'avg', 'acc_phone_')

    # We add the gyroscope data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    dataset.add_numerical_dataset('gyroscope.csv', 'timestamps', ['x','y','z'], 'avg', 'gyr_phone_')

    # We add the labels provided by the users. These are categorical events that might overlap. We add them
    # as binary attributes (i.e. add a one to the attribute representing the specific value for the label if it
    # occurs within an interval).
    dataset.add_event_dataset('labelsOwn.csv', 'label_start', 'label_end', 'label', 'binary')

    # We add the amount of light sensed by the phone (continuous numerical measurements) and aggregate by averaging

    # We add the magnetometer data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    dataset.add_numerical_dataset('magnetometer.csv', 'timestamps', ['x','y','z'], 'avg', 'mag_phone_')

    # We add the pressure sensed by the phone (continuous numerical measurements) and aggregate by averaging again
    # dataset.add_numerical_dataset('pressure.csv', 'timestamps', ['pressure'], 'avg', 'press_phone_')

    # Get the resulting pandas data table
    dataset = dataset.data_table

    # Plot the data
    DataViz = VisualizeDataset_own(__file__)

    # Boxplot
    # DataViz.plot_dataset_boxplot(dataset, ['acc_phone_x','acc_phone_y','acc_phone_z','acc_watch_x','acc_watch_y','acc_watch_z'])
    DataViz.plot_dataset_boxplot(dataset, ['acc_phone_x','acc_phone_y','acc_phone_z'])

    # Plot all data
    # DataViz.plot_dataset(dataset, ['acc_', 'gyr_', 'hr_watch_rate', 'light_phone_lux', 'mag_', 'press_phone_', 'label'],
    #                                 ['like', 'like', 'like', 'like', 'like', 'like', 'like','like'],
    #                                 ['line', 'line', 'line', 'line', 'line', 'line', 'points', 'points'])
    
    DataViz.plot_dataset(dataset, ['acc_', 'gyr_', 'mag_', 'label'],
                                    ['like', 'like', 'like', 'like'],
                                    ['line', 'line', 'line', 'points'])


    # And print a summary of the dataset.
    util_own.print_statistics(dataset)
    datasets.append(copy.deepcopy(dataset))

    # If needed, we could save the various versions of the dataset we create in the loop with logical filenames:
    # dataset.to_csv(RESULT_PATH / f'chapter2_result_{milliseconds_per_instance}')


# Make a table like the one shown in the book, comparing the two datasets produced.
util_own.print_latex_table_statistics_two_datasets(datasets[0], datasets[1])

# Finally, store the last dataset we generated (250 ms).
dataset.to_csv(RESULT_PATH / RESULT_FNAME)

# Lastly, print a statement to know the code went through

print('The code has run through successfully!')



