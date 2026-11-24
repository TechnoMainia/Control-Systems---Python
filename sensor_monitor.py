#Notes

# Error scenarios for alert threshold for when using old values.
# Threshold line in histogram
# Errors for string with ints and vice versa

# ========== IMPORTS ==========
import random
import numpy as np
import matplotlib.pyplot as plt
import csv
from pathlib import Path
# ========== GLOBAL VAIRABLES ==========

random.seed(1) # Used to ensure all random numbers are the same every run

file_name = Path(__file__).resolve().parent / "saved_values.csv"

sensor_values = []  #List of sensor values

user_continue = True  #variable for whether the the program should loop depending on user input

# Function used to validate integers from the users input
def integer_validation(variable):
    while True:
        try:
            return int(variable)
        except ValueError:
            variable = input("ERROR. Please input a valid number: ")

# A function taken from "Python session 2" used to read the values from the csv file to make use of the old values instead of generating new values.
def load_readings(filename):
    readings = []
    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                readings.append(float(row["sensor_values"]))
    
    except OSError as error:
        print("Could not access the file:", error)

    return readings

# Function used at the start of the program to ask the user whether they want to use the last saved data written to the csv file or not.
def value_choice ():
    choice = input("Would you like to use old values?: ").strip().lower() # strip and lower are used to get a common base variable to compare to the preset answer list
    
    while choice not in ("y", "yes", "sure", "please", "n", "no", "nope"):  #List of possible answers
        choice = input("Your input is not within our scope. Please try again (Y/N): ").strip().lower()

    if choice in ("y", "yes", "please", "sure"):
        sensor_values = load_readings(file_name)
        print("Values have been loaded: ", sensor_values)

        no_generated = 0
        print("Number of values:", len(sensor_values))
        alert_thresh = integer_validation(input("Alert threshold: "))

        
    else:
        sensor_type, no_generated, min_val, max_val, alert_thresh = get_user_input()

        print("\n")

        print("Conditions:")
        print_vals(sensor_type, no_generated, alert_thresh)

        print("\n")

        sensor_values = generate_readings(min_val, max_val, no_generated)

    return(sensor_values, no_generated, alert_thresh)

# Function for user inputs (sensor type, number of generated values, minimum and maximum value and alert threshold.)
def get_user_input(): 
    sensor_type = input("Sensor type (temperature, light): ").strip()
    while sensor_type.lower() not in ("temp", "temperature", "light"):
        sensor_type = input("This sensor type isn't in our database. Please try again: ")

    no_generated = (integer_validation(input("Number of readings to generate: ")))
    while no_generated < 1:
        no_generated = integer_validation(input("This number is below the minimum (1). Please try again: "))

    min_val = integer_validation(input("Minimum value: "))
    max_val = integer_validation(input("Maximum value: "))
    while max_val <= min_val:
        max_val = integer_validation((input("This maximum value is below the minimum. Please input a larger value: ")))

    alert_thresh = integer_validation(input("Alert threshold: "))
    return(sensor_type, no_generated, min_val, max_val, alert_thresh)

# Function to print out the users values for clarification
def print_vals(sensor_type, no_generated, alert_thresh):
    print("Sensor Type: ", sensor_type)
    print("Number of generated numbers: ",no_generated)
    print("Alert threshold: ",alert_thresh)

#Function to artificially generate the sensors values taking into account the minimum and maximum values and the total number to generate.
def generate_readings(min_val, max_val, no_generated):
    sensor_values = []
    for x in range(int(no_generated)):
        sensor_values.append(random.randint(min_val, max_val))
    return (sensor_values)

# This function is used along with numpy to calculate all of the statistis on our sensor values.
def calculate_statistics(sensor_values):

    mean = np.mean(sensor_values)
    print("Mean: ", mean)

    lowest_val = min(sensor_values)
    print("Lowest value: ", lowest_val)

    highest_val = max(sensor_values)
    print("Highest value: ", highest_val)

    standard_dev = np.std(sensor_values)
    print("Standard deviation: ", standard_dev)

    return(mean, sensor_values, lowest_val, highest_val, standard_dev)

# Function to sort out the numbers above or less/equal to the threshold value. Keeps temporary lists to show this data back to the user.
def find_outliers(sensor_values, alert_thresh):
    sensor_values_above_threshold = []
    sensor_values_below_threshold = []
    for i in range(len(sensor_values)):
        if sensor_values[i] > alert_thresh:
            sensor_values_above_threshold.append(sensor_values[i])
        elif sensor_values[i] <= alert_thresh:
            sensor_values_below_threshold.append(sensor_values[i])
    
    print("Total number of readings: ", len(sensor_values))
    print("Number of readings above threshold: ", len(sensor_values_above_threshold))
    print("Number of readings below threshold: ", len(sensor_values_below_threshold))
    print("List of above values: ",sensor_values_above_threshold)
    print("List of below values: ",sensor_values_below_threshold)

# This is a function taken from "Python session 2" to save the relevant data within the functino brackets to the csv file.
def save_readings(filename, sensor_values):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["sample", "sensor_values"])

            for sample_number, value in enumerate(sensor_values, start=1):
                writer.writerow([sample_number, value])

        print("=== CSV file has been saved ===")

    except OSError as error:
        print("Could not access the file:", error)

# Function that uses matplot to plot the data from the users input and the values generated. Also helps with dispaying the statistical analysis in visual format.
# This funciton displays both the line plot and histrogram diagrams.
def plotting_readings(sensor_values, alert_thresh):
    plt.plot(range(1, int(len(sensor_values))+1), sensor_values, label="Sensor Values")  # Sensor value line
    plt.axhline(y=int(alert_thresh), color="r", linestyle="--", label="Alert Threshold")  #Threshold line
    plt.title("Sensor Readings (Line Plot)")
    plt.grid()
    plt.xlabel("List position")
    plt.ylabel("Sensor Value")
    plt.legend()
    plt.show()

    sensor_values_sorted = sorted(sensor_values) # Values were sorted to have a cleaner histogram
    plt.hist(sensor_values_sorted, label="Sensor Values (Sorted)")  # Plotted sensor values
    plt.title("Sensor Readings (Histogram)")
    plt.grid()
    plt.xlabel("Sensor value")
    plt.ylabel("Number of readings")
    plt.axvline(x=alert_thresh, color="r", linestyle="--", label="Alert Threshold") # Alert threshold line
    plt.legend()
    plt.show()

# A function to ask the user whether they want to continue the loop again or end the program all
def continue_request():
    user_continue = input("Would you like to repeat this process (Y/N): ").strip().lower()

    while user_continue not in ("y", "yes", "n", "no") :
        user_continue = input("ERROR. Not within scope. Please isert a valid input: ").strip().lower()

    return user_continue in ("y", "yes")

# The main function to be ran upon startup
def main(user_continue):
    while user_continue == True:
    
        sensor_values, no_generated, alert_thresh = value_choice()
    
        print("Sensor value list: ", sensor_values, "\n")
    
        mean, sensor_values, lowest_val, highest_val, standard_dev = calculate_statistics(sensor_values) 
    
        find_outliers(sensor_values, alert_thresh)
    
        print("\n")
    
        save_readings(file_name, sensor_values)
    
        plotting_readings(sensor_values, alert_thresh)
    
        print("\n")
    
        user_continue = continue_request()


# ========== MAIN PROGRAM ==========

# Code taken from Python sessions, used to run on startup
if __name__ == "__main__":
    main(user_continue)