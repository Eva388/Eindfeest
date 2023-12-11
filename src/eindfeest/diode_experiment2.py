# Diode_experiment: perform experiment using data from arduino device
# Eva Bredeweg
# 9-11-23

from eindfeest.arduino_device2 import ArduinoVISADevice,list_devices
import math
import numpy as np

# perform DiodeExperiment
class DiodeExperiment():

    def __init__(self, port):
        self.device = ArduinoVISADevice(port)
        """ calls on specified device

        Args:
            port (str): which device and port used
        """
    
    def scan(self, low, high, n):
        # make lists of I and V and errors to fill
        """makes lists of voltages and currents and lists containing their errors

        Args:
            low (int): lowest voltage value
            high (int): highest voltage value
            n (int): number of repeats diode experiment

        Returns:
            lists with int: lists of V, I, error V, error I
        """
        list_error_I = []
        list_error_V = []
        list_I = []
        list_V = []

        # make ADC from voltage input
        low_ADC = int(np.floor(low * 1023 / 6.091935483870968))
        high_ADC = int(np.floor(high * 1023 / 6.091935483870968))
        
        # increase ADC and make (error)lists of V and I
        for ADC in range(low_ADC, high_ADC):
            self.device.set_output_value(ADC)

            short_list_I = []
            short_list_V = []

            # repeat experiment 5 times
            for i in range (n):
                V_zon = 3*self.device.get_input_voltage(1)
                I_zon = self.device.get_input_voltage(2)/4.7

                short_list_I.append(I_zon)
                short_list_V.append(V_zon)
            
            # determine error per experiment, add to list
            error_I = np.std(short_list_I)/math.sqrt(len(short_list_I))
            error_V = np.std(short_list_V)/math.sqrt(len(short_list_V))
            list_error_I.append(error_I)
            list_error_V.append(error_V)

            # determine average per experiment, add to list
            av_I = np.average(short_list_I)
            av_V = np.average(short_list_V)
            list_I.append(av_I)
            list_V.append(av_V)

            self.device.set_output_value(0)
  
        self.device.close()
  
        return(list_V, list_I, list_error_V, list_error_I)



