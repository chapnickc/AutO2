import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas

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
        
    def showWean(self):
        
        #Build Figure
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1) 
        ax2 = ax1.twinx()

        ax1.set_ylabel('O2 LPM')
        ax2.set_ylabel(r'SpO$_2$')
        wid = FigureCanvas(fig)
        
        fig.canvas.mpl_connect('axes_enter_event', enter_axes)
        
        #Calculate Ideal Piecewise Wean
        wean_values = list()
        time_values = list()
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
        
        #Plot Ideal Wean
        self.ax1.clear()
        self.ax1.plot(time_values, wean_values, linewidth = 3)

        #plt.axis([len(fr.values)-200, len(fr.values)+10, min(fr.values)-5, max(fr.values) + 2])
        self.ax1.figure.canvas.draw()
      
   # def startWean(self):
  #      flow = fr.read_sensor()
 #       o2vitals = 97
#        self.ax1.plot(clock, flow, linewidth = 3)
   #     self.ax2.plot(clock, o2vitals, linewidth = 3)
        
