#Made by Melle Sprey 14026376
from matplotlib import pyplot as plt
import csv  
from eindfeest.diode_experiment import DiodeExperiment




def do_your_thing_python():
    """The View part of the arduino code. Takes from the model DiodeExperiment, and performs the measurements (with low = 0, high =1023 , n = 10),
     plots the measurements and saves them to a csv file called 'metingen'
    """
    data = DiodeExperiment("ASRL11::INSTR")                #Does the thing
    V, I = data.scan(0,1023,10)    
    plt.plot(V,I)
    # plt.errorbar(Vav,Iav,Ierr,Verr,fmt='none')      #Plotting with our errorbars
    plt.title('UI curve of LED')
    plt.ylabel('I (Ampere)')
    plt.xlabel('U (Volt)')
    plt.show()

    # zippert = zip(Vav,Verr,Iav,Ierr)        #zips arrays
    # with open('metingen.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['V','Verr','I','Ierr'])  #First line, and the rest of the data trough for loop
    #     for i in zippert:                   
    #         writer.writerow(i)

do_your_thing_python()
