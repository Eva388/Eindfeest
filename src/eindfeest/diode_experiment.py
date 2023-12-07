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

        R_u2 = 4.7
        Vmosstd = np.empty([abs(high-low)])       #Making empty arrays to put values in later
        Vmosavg = np.empty([abs(high-low)])
        Vzonstd = np.empty([abs(high-low)])
        Vzonavg = np.empty([abs(high-low)])

        for i in range(low,high):       #Beginning the measurement, setting bounds
            self.device.set_output_value(i) #Variating power input from low to high points IN VOLT
            
            Vmos = np.empty([n])    #Arrays which need to be empty for every new input voltage
            Vzon = np.empty([n])         
            for k in range(n):                                  #Measure Vres and Vled n times                #Measure voltage resistor
                Vzon[k] = 3 * self.device.get_input_voltage(1)             #Measure voltage LED
                Vmos[k] = Vzon[k] - self.device.get_input_voltage(2)

            Vmosstd[i-low] =np.std(Vmos)/sqrt(n)   #For all the n measurements, the average and std for Vres and Vled added here
            Vzonstd[i-low] = np.std(Vzon)/sqrt(n)
            Vmosavg[i-low] = np.average(Vmos)
            Vzonavg[i-low] = np.average(Vzon)

        I_u2 = Vmosavg/R_u2     #Calculating Iled and std on Iled
        # Imosstd = Vmosstd/R_u2
        Rzon = Vzonavg / I_u2

        Izonavg = I_u2 + (Vzonavg/3)
        # Imos = I_u2
        # Izon = Vzon / Rzon
        # Izonstd = Vzonstd/R_u2
        self.device.set_output_value(0)
        self.device.close()     #Closes the arduino

        return Vzonavg, Izonavg

rm = pyvisa.ResourceManager("@py") #Does rm
def list_devices(): #lists current resources, I dont know if this works because on my pc this gives a warning and i have to download stuff
    """lists the devices connected to the computer

    Returns:
        [str] --[lists the open devices connected with the PC]
    """
    return(rm.list_resources())

