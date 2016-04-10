from time import sleep
import subprocess

def convert_flow(hex_value):
    dec_value = int(hex_value, 16)
    flow_value = 15*((dec_value/16384) - 0.1)/0.8
    return flow_value

def read_sensor():
    """read from the flow sensor. convert hex values to flow values and append the 
    converted value to a data file
    """
    try:
        # get the flow as a hex value
        command = 'sudo i2cget -y 1 {}'.format(self.i2c_bus)
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

        # get the output from the process and convert from 
        # byte code to a string
        hex_value = str(p.communicate()[0])
        print (hex_value)

        if not hex_value == '':
            dec_value = int(hex_value, 16)
            flow_value = 15*((dec_value/16384) - 0.1)/0.8
            print (flow_value)
        elif hex_value == '':
            raise OSError
    except OSError as e:
			#print ("Cant't read sensor: {}".format(e))

    else:
        #self.data_file.write(flow_value)
        return flow_value

if __name__ == '__main__':
    while True:
        value = read_sensor()
        print (value)
        sleep(0.5)
