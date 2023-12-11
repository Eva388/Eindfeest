# arduino_device.py: setting output and getting input from arduino
# Eva Bredeweg
# 9-11-23


try:
    from nsp2visasim import sim_pyvisa as pyvisa
except ModuleNotFoundError:
    import pyvisa

# set output and get input from arduino
class ArduinoVISADevice:
    def __init__(self, port):
        """ defines which port is used

        Args:
            port (str): sets port as a self
        """
        self.port = port
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(port, read_termination="\n", write_termination="\n")

    def get_identification(self):
        """ defines contents of arduino

        Returns:
            str: contents
        """
        return(self.device.query("*IDN?"))

    # set output on channel 0
    def set_output_value(self, value):
        """ sets output on channel 0

        Args:
            value (int): ADC value as output value
        """
        self.device.query(f"OUT:CH0 {value}")
        self.output = value
    
    def get_output_value(self):
        """ returns output value in ADC that was set in set_output

        Returns:
            int: output value
        """
        return(self.output)
    
    # measure ADC on channel
    def get_input_value(self, channel):
        """ measures and returns voltage in ADC on a channel

        Args:
            channel (str): channel to measure voltage in ADC

        Returns:
            int: amount of voltage in ADC measured
        """
        return(int(self.device.query(f"MEAS:CH{channel}?")))

    # measure voltage on channel
    def get_input_voltage(self, channel):
        """measures and returns voltage in volt on a channel

        Args:
            channel (str): channel to measure voltage in volt

        Returns:
            int: amount of voltage in volt measured
        """
        return(int(self.device.query(f"MEAS:CH{channel}?"))*3.3/1023)
    
    def close(self):
        self.device.close()

# return list of resources
def list_devices():
    """ returns list of devices 

    Returns:
        list with str: with devices
    """
    rm = pyvisa.ResourceManager("@py")
    return(rm.list_resources())