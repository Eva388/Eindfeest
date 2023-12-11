# View.py: plot and csv of arduino experiment
# Eva Bredeweg
# 9-11-23

import matplotlib.pyplot as plt
import csv
from eindfeest.arduino_device2 import list_devices
from eindfeest.diode_experiment2 import DiodeExperiment

# print devices
print(list_devices())

def view():
    # perform DiodeExperiment
    """calls on DiodeExperiment class, plots UI-graph and makes csv file of data
    """
    measurements = DiodeExperiment("ASRL::SIMPV_BRIGHT::INSTR")
    list_V, list_I, list_error_V, list_error_I = measurements.scan(0, 3.3, 2)
    print(list_V[-1])
    # plot average and errorbars
    # print(list_V)
    plt.errorbar(list_V, list_I, list_error_I, list_error_V, fmt='none')
    plt.xlabel("V (volt)")
    plt.ylabel("I (Ampere)")
    plt.title("IU-graph")
    plt.show()

    # make csv file with average and errorbars
    with open('metingen.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['V (Volt)','I (Ampere)', 'V_err (Volt)', 'I_err (Ampere)'])
        for V, I, err_V, err_I in zip(list_V, list_I, list_error_V, list_error_I):
            writer.writerow([V, I, err_V, err_I])
    return


view()




