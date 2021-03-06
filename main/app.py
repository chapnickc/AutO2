from __future__ import division
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import escape_markup

import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
from kivy.garden.androidtabs import *

from flow_reader import FlowReader
from Wean import Wean

kv = """
<PlotTab>:
    orientation: 'vertical'

<AndroidTabs>:
    tab_indicator_height: '8dp'
    tab_indicator_color: 1, 0, 0, 1

<AndroidTabsBar>:
    canvas.before:
        Color:
            rgba: 0.1, 0.3906, 0.70, 1
        Rectangle:
            pos: self.pos
            size: self.size

<ParametersTab>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
"""

Builder.load_string(kv)

def enter_axes(event):
    print('enter_axes', event.inaxes)
    event.inaxes.patch.set_facecolor('yellow')
    event.canvas.draw()



class PlotTab(BoxLayout):
    """
    This class holds the layout for the tab which displays
    data on the plot. It also contains a start button for
    the user to begin the oxygen control
    """
    def __init__(self, *args, **kwargs):
        super(PlotTab, self).__init__(*args, **kwargs)
        self.listener = None              # holds the flow listener
        self.wid, self.ax1, self.ax2 = self.get_fc(1)
        self.add_widget(self.wid)
        self.add_buttons()


    def get_fc(self, i):
        """
        Build the figure. Adds two axes for flow data and
        SpO2 data.
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        ax2 = ax1.twinx()

        #fig.text(1, 0.5, 'SpO2', ha = 'center', va = 'center')
        #fig.text(0.5, 0.04, 'Time', ha = 'center', va = 'center')
        ax1.set_ylabel('Flow Data')
        ax2.set_ylabel(r'SpO$_2$')
        wid = FigureCanvas(fig)

        # fig.canvas.mpl_connect('axes_enter_event', enter_axes)
        return wid, ax1, ax2

    def plot_flow(self):
        """
        Plot the values from the flow sensor on ax1
        and update the figure canvas. Calls the
        read_sensor() function of the FlowReader class
        and then reades from the values in the 'fr' object
        which is an instance of the FlowReader.
        """
        fr.read_sensor()
        xs = [x for x in range(len(fr.values))]

        self.ax1.clear()
        self.ax1.plot(xs, fr.values, linewidth = 3)

        #plt.axis([len(fr.values)-200, len(fr.values)+10, min(fr.values)-5, max(fr.values) + 2])
        self.ax1.figure.canvas.draw()
        print ('Drawing flow')

    def start_flow_listen(self):
        """
        It schedules the flow values to be read every
        0.5 seconds indefinitely by calling the
        plot_flow() method above.
        bound to the "Read from flow sensor button".
        """
        self.listener = Clock.schedule_interval(lambda x: self.plot_flow(), 0.5)

    def stop_flow_listen(self):
        """
        Deschedules the plot_flow() function. Bound to the
        'Stop reading from flow sensor()'
        """
        try:
            self.listener.cancel()
            print ('Flow Listening canceled')
        except AttributeError as e:
            print (e)

    #CHANGED - ADDED wean method - PI 4/22/16
    def plot_wean(self):
        """
        On press will begin and plot a patients weaning according to wean parameters from OxygenParameter() instances made in OxygenPara.
        Will also show the outline of the idealize wean from the start.
        Will call stabilize() if patient goes out of range.

        should all of the wean mechanics be housed in this method, or do we have this method call a Wean class that houses said mechanics
        """
        spo2_high = params_tab.params['SPO2_HIGH'].value
        spo2_low = params_tab.params['SPO2_LOW'].value
        delta_t = params_tab.params['DELT_T'].value
        delta_flow = params_tab.params['DELT_FLOW'].value
        flow_start = params_tab.params['FLOW_START'].value


        w = Wean(spo2_high, spo2_low, flow_start, delta_flow, delta_t)
        time_values, wean_values = w.get_wean()


        self.ax1.set_ylabel('Flow Data')
        self.ax2.set_ylabel(r'SpO$_2$')
        self.ax2.clear()
        self.ax2.plot(time_values, wean_values, 'red', linewidth = 3)

        #plt.axis([len(fr.values)-200, len(fr.values)+10, min(fr.values)-5, max(fr.values) + 2])
        self.ax2.figure.canvas.draw()
        print ('Drawing wean')


        #w = Wean(SpO2_h_widget.value, SpO2_l_widget.value, start_flow_widget.value, delt_flow_widget.value, delt_Tstep.value)
        #w.showWean
        #w.startWean

    def add_buttons(self):
        """
        Adds all the buttons to the screen using
        a BoxLayout
        """
        bl = BoxLayout(size_hint = (1,0.25))

        b = Button(text='Monitoring Mode')                              #CHANGED TEXT - PI 4/22/16
        b.bind(on_press = lambda x: self.start_flow_listen())
        bl.add_widget(b)

        b = Button(text='Pause Monitoring')                             #CHANGED TEXT - PI 4/22/16
        b.bind(on_press = lambda x: self.stop_flow_listen())
        bl.add_widget(b)

        b = Button(text = 'Start Wean')                                 #CHANGED TEXT - PI 4/22/16
        b.bind(on_press = lambda x: self.plot_wean())
        bl.add_widget(b)

        self.add_widget(bl)


class OxygenAdjustment(BoxLayout):
    """
    This is a Parent class which builds a basic oxygen adjustment
    to accept oxygen parameters from the user.
    """
    def __init__(self, setting_label, init_value, min_value = 75, max_value = 100, **kwargs):
        super(OxygenAdjustment, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.setting_label = setting_label
        self.value = float(init_value)
        self.min_value = float(min_value)
        self.max_value = float(max_value)

        # builds it self which it is instantiated
        self.build()

    def build(self):
        top = Label(text = self.setting_label, font_size = 35, color = [0,0,0,1], size_hint = (1,0.4), markup = True)

        self._middle = Label(text = str(self.value), font_size = 30, color = [0,0,0,1], size_hint = (1, 0.5))

        dials = BoxLayout(orientation = 'vertical', padding = [20,5], spacing = 2, size_hint = (1,1))

        up_arrow = Button(text = 'UP', font_size = 20, background_normal = '', background_color = [0.1, 0.3906, 0.70, 1])
        down_arrow = Button(text = 'DOWN', font_size = 20, background_normal = '', background_color = [0.1, 0.3906, 0.70, 1])


        # binding the functions to increase and decrease the values to the buttons
        up_arrow.bind(on_press = lambda x: self.increase_value())
        down_arrow.bind(on_press = lambda x: self.decrease_value())


        dials.add_widget(up_arrow)
        dials.add_widget(down_arrow)

        self.add_widget(top)
        self.add_widget(self._middle)
        self.add_widget(dials)

    def increase_value(self):
        """
        Increases the value of the parameter
        displayed on the tab if the value is
        """
        if self.value < self.max_value:
            self.value += 1
        else:
            self.value = self.max_value
        self._middle.text = str(self.value)

    def decrease_value(self):
        """
        Decreases the value of the parameter
        displayed on the tab if it is greate
        than the minimum.
        """
        if self.value > self.min_value:
            self.value -= 1
        else:
            self.value = self.min_value
        self._middle.text = str(self.value)


class DeltaFlow(OxygenAdjustment):
    """
	"\N{GREEK CAPITAL LETTER DELTA"
    """

    def __init__(self, setting_label = 'Delta \nFlow', **kwargs):
        super(DeltaFlow, self).__init__(setting_label, **kwargs)

    def increase_value(self):
        if self.value < self.max_value:
            # increase by 1/8 L 
            self.value += 0.125
        else:
            self.value = self.max_value
        self._middle.text = str(self.value)

    def decrease_value(self):
        if self.value > self.min_value:
            # decrease by 1/8 L 
            self.value -= 0.125
        else:
            self.value = self.min_value
        self._middle.text = str(self.value)


class ParametersTab(BoxLayout):
    """
    Holds all the parameters

    %CHANGE --> we could store default wean parameters as such below during initialization. 
    These would be "default" because they would not be used again. If we needed to grab
    the current parameter value we would get access it through the OxygenAdjustment class (see def build() comments below).
    self.SpO2_high_default =  float [%]
    self.SpO2_low_default =   float [%]
    self.flow_start_default = float [LPM]
    self.delt_flow_default =  float [LPM]
    self.delt_Tstep_default = int [minutes]
    """
    def __init__(self, params = {},  **kwargs):
        super(ParametersTab, self).__init__(**kwargs)
        self.params = params
        self.SpO2_high = float(99)
        self.SpO2_low = float(86)
        self.flow_start = float(2)
        self.delt_flow = float(1/8)
        self.delt_Tstep = int(30)
        self.build()

    def build(self):
        """
        Builds the page
        WHAT IF we said (assuming we add the attributes seen above in init):
        "
        SpO2_h_widget = OxygenAdjustment(setting_label ='SpO[sub]2[/sub] High', init_value = self.SpO2_high_default)
        SpO2_l_widget = OxygenAdjustment(setting_label ='SpO[sub]2[/sub] Low', init_value = self.SpO2_low_default)
        ....
        self.add_widget(SpO2_h_widget)
        self.add_widget(SpO2_l_widget)
        ...
        "
        Then in PlotTab.wean() (when pressed to start) can grab the needed values as such:
        "
        SpO2_high = SpO2_h_widget.value
        SpO2_low  = SpO2_l_widget.value
        ...
        "
        """

        self.params['SPO2_HIGH'] = OxygenAdjustment(setting_label ='SpO[sub]2[/sub] \nHigh', init_value = self.SpO2_high)
        self.params['SPO2_LOW'] = OxygenAdjustment(setting_label = 'SpO[sub]2[/sub] \nLow', init_value = self.SpO2_low)
        self.params['DELT_T'] = OxygenAdjustment(setting_label = 'Delta \nTime', init_value = self.delt_Tstep , min_value = 0.5, max_value = 10)
        self.params['DELT_FLOW'] = DeltaFlow(init_value = self.delt_flow, min_value = 0, max_value = 1)
        self.params['FLOW_START'] = OxygenAdjustment(setting_label = 'Starting \nFlow', init_value = self.flow_start, min_value = 0, max_value = 15)

        for param in self.params.values():
            self.add_widget(param)


class Tab(BoxLayout, AndroidTabsBase):
    def __init__ (self, **kwargs):
        super(Tab, self).__init__(**kwargs)

class O2App(App):
    def __init__(self, **kwargs):
        super(O2App, self).__init__(**kwargs)

    def build(self):
        tabs = AndroidTabs()
        tab = Tab(text = 'Vitals')
        tab.add_widget(PlotTab())
        tabs.add_widget(tab)

        tab = Tab(text = 'Parameters')
        tab.add_widget(params_tab)
        tabs.add_widget(tab)

        return tabs



if __name__ == '__main__':
    # instantiate params tab so the 
    # values of the parameters can be accessed gloabally
    params_tab = ParametersTab()

    # instantiate the flow reader for the funtions expecting it
    fr = FlowReader()
    print(params_tab.params['SPO2_HIGH'].value)
    O2App().run()


