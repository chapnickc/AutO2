import RPi.GPIO as GPIO
import time

class Wean:

    """
    To take user-specified parameters for patient SpO2 weaning. To be called from app.py
    """
    
    def __init__(self):
        self.SpO2_high = 98
        self.SpO2_low = 92
        self.flow_start = 3
        self.deltFlow = .5
        self.deltT_step = 20
        
    def showWean(self):
      
    def startWean(self):
