import time
import matplotlib.pyplot as plt

# this module is currently not used by the class
# so it is okay if it is not loaded
try:
	import RPi.GPIO as GPIO
except RuntimeError as e:
	print (e)



class Wean:

    """
    To take user-specified parameters for patient SpO2 weaning. 
    Parameters are inputs to the class when called in app.py
    
        self.SpO2_high =  float [%]
        self.SpO2_low =   float [%]
        self.flow_start = float [LPM]
        self.delt_flow =  float [LPM] 
        self.delt_Tstep = int [minutes]
    
    """
    
    def __init__(self, SpO2_high, SpO2_low, flow_start, delt_flow, delt_Tstep):
        self.SpO2_high = SpO2_high
        self.SpO2_low = SpO2_low
        self.flow_start = flow_start
        self.delt_flow = delt_flow
        self.delt_Tstep = delt_Tstep
        
    def get_wean(self):
      
        #Calculate Ideal Piecewise Wean
        wean_values = list()
        time_values = list()
        print (self.flow_start, self.delt_flow)
        drops = int(self.flow_start/self.delt_flow)

        for k in range(drops):
            wean_values.append(self.flow_start - k*self.delt_flow)
            wean_values.append(self.flow_start - k*self.delt_flow)
            time_values.append(k*self.delt_Tstep)
            time_values.append((k+1)*self.delt_Tstep)
            
        wean_values.append(0)
        wean_values.append(0)
        time_values.append(drops*self.delt_Tstep)
        time_values.append((drops+1)*self.delt_Tstep)
        
        values = (time_values, wean_values)
      
        return values
   # def startWean(self):
  #      flow = fr.read_sensor()
 #       o2vitals = 97
#        self.ax1.plot(clock, flow, linewidth = 3)
   #     self.ax2.plot(clock, o2vitals, linewidth = 3)
        
