#Made by Melle Sprey 14026376
import pyvisa
rm = pyvisa.ResourceManager("@py") #Does rm

class ArduinoVISADevice:   
    def __init__(self,port): 
        """Opens the specified port, and sets it as a self attribute

        Arguments: 
            args {[str]} --The port to which the arduino device is connected
        """        
        self.port = port
        self.device = rm.open_resource( self.port, read_termination="\r\n", write_termination="\n") #opens the arduino



    def close(self):
        """Closes the arduino
        """
        self.device.close()


    def get_identification(self):
        """Returns the specifications of the arduino

        Returns:
            [str] --[specifications of the arduino]
        """
        return(self.device.query('*IDN?'))


    def set_output_value(self,value): # Powers arduino, and sets current power as value of the class
        """Sets an output voltage for the arduino in ADC units 

        Arguments: 
            args {[int]} --Value of the output voltage in ADC
        """
        self.device.query(f'OUT:CH0 {value}')
        self.output = value


    def get_output_value(self): #REturns current power (voltage)
        """Returns the current output voltage in adc

        Returns:
            [int] --[The current output voltage over the arduino]
        """
        return(self.output)


    def get_input_value(self,channel):  #Measures channel in ADN
        """Measures the current voltage over the specified channel in ADC

        Arguments: 
            args {[str]} --the channel to measure the voltage over

        Returns:
            [int] --[Voltage over the specified channel (in this case either the resistor or the LED)]
        """
        return(self.device.query(f'MEAS:CH{channel}?'))
    

    def get_input_voltage(self,channel): #Measures channel in Volt

        """Measures the current voltage over a specified channel in Volts

        Arguments: 
            args {[str]} --the channel to measure the voltage over

        Returns:
            [float] --[The value over the given channel in Volt]
        """
        return(float(self.device.query(f'MEAS:CH{channel}?'))*(3.3/1023))


def list_devices(): #lists current resources, I dont know if this works because on my pc this gives a warning and i have to download stuff
    """lists the devices connected to the computer

    Returns:
        [str] --[lists the open devices connected with the PC]
    """
    return(rm.list_resources())
