#Made by Melle Sprey 14026376
from eindfeest.arduino_device import ArduinoVISADevice
import numpy as np
from math import sqrt
import pyvisa


class DiodeExperiment:
    """The model part of the Arduino code. The next step in performing measurements over the cirquit with the arduino
    """

    def __init__(self,port): 
        """sets self.device as an ArduinoVisaDevice class, with the right port

        Arguments: 
        args {['str]} --The port to open the arduino
        """

        self.port = port
        self.device = ArduinoVISADevice(self.port)
        

    def scan(self,low,high,n):
        """Sets the output voltages between given points, measures the voltage over the LED and resistor a given number of times, and from that calculates the V and I over the LED with errors

    Arguments: 
        [int] --the minimum of output voltage for the arduino in ADC
        [int] --the maximum of output voltage for the arduino in ADC
        [int] --the number of measurements taken for each output voltage

    Returns:
        [list] --[The average values of V over domain[low,high]]
        [list] --[The error values of V over domain[low,high]]
        [list] --[The average values of I over domain[low,high]]
        [list] --[The erro values of I over domain[low,high]]
    """

        Rres =220
        Vrstd = np.empty([abs(high-low)])       #Making empty arrays to put values in later
        Vravg = np.empty([abs(high-low)])
        Vstd = np.empty([abs(high-low)])
        Vavg = np.empty([abs(high-low)])

        for i in range(low,high):       #Beginning the measurement, setting bounds
            self.device.set_output_value(i) #Variating power input from low to high points IN VOLT
            
            Vres = np.empty([n])    #Arrays which need to be empty for every new input voltage
            Vled = np.empty([n])       
            for k in range(n):                                  #Measure Vres and Vled n times:
                Vres[k] = self.device.get_input_voltage(2)               #Measure voltage resistor
                Vled[k] = self.device.get_input_voltage(1) - Vres[k]             #Measure voltage LED


            Vrstd[i-low] =np.std(Vres)/sqrt(n)   #For all the n measurements, the average and std for Vres and Vled added here
            Vstd[i-low] = np.std(Vled)/sqrt(n)
            Vravg[i-low] = np.average(Vres)
            Vavg[i-low] = np.average(Vled)

        Iavg = Vravg/Rres     #Calculating Iled and std on Iled
        Istd = Vrstd/Rres
        self.device.set_output_value(0)
        self.device.close()     #Closes the arduino

        return Vavg, Vstd, Iavg, Istd

rm = pyvisa.ResourceManager("@py") #Does rm
def list_devices(): #lists current resources, I dont know if this works because on my pc this gives a warning and i have to download stuff
    """lists the devices connected to the computer

    Returns:
        [str] --[lists the open devices connected with the PC]
    """
    return(rm.list_resources())

print(list_devices())
nj