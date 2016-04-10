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
        command = 'sudo i2cget -y 1 {}'.format('0x49')
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

        # get the output from the process and convert from 
        # byte code to a string
        hex_value = str(p.communicate()[0])

        if not hex_value == '':
            dec_value = int(hex_value, 16)
            flow_value = 15*((dec_value/16384) - 0.1)/0.8
        elif hex_value == '':
            raise OSError
    except OSError as e:
	pass
    else:
        return flow_value, hex_value

if __name__ == '__main__':
    while True:
        flow_value, hex_value  = read_sensor()
        
        result = 'Flow value: {}\tHex Value: {}'.format(flow_value, hex_value)
        print (result)

        sleep(0.5)
