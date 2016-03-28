from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout 
from kivy.lang import Builder
from kivy.clock import Clock

import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
from kivy.garden.androidtabs import *

from flow_reader import FlowReader

fr = FlowReader()


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

"""

Builder.load_string(kv)

def enter_axes(event):
    print('enter_axes', event.inaxes)
    event.inaxes.patch.set_facecolor('yellow')
    event.canvas.draw()



class PlotTab(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(PlotTab, self).__init__(*args, **kwargs)
        
        self.listener = None
        self.wid, self.ax = self.get_fc(1)
        self.add_widget(self.wid)
        self.add_buttons()



    def get_fc(self, i):
        """
        Build the figure 
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1) 
        wid = FigureCanvas(fig)
        
        fig.canvas.mpl_connect('axes_enter_event', enter_axes)
        
        return wid, ax1

    def plot_flow(self):

        fr.read_sensor()
        xs = [x for x in range(len(fr.values))]

        self.ax.clear()
        self.ax.plot(xs, fr.values, linewidth = 3)

        #plt.axis([len(fr.values)-200, len(fr.values)+10, min(fr.values)-5, max(fr.values) + 2])
        self.ax.figure.canvas.draw()
        print ('Drawing flow')

    def start_flow_listen(self):
        self.listener = Clock.schedule_interval(lambda x: self.plot_flow(), 0.5)

    def stop_flow_listen(self):
        self.listener.cancel()
        print ('Flow Listening canceled')

    def add_buttons(self):

        b = Button(text='Press to read from flow sensor',
                 size_hint = (0.5, 0.1))
        b.bind(on_press = lambda x: self.start_flow_listen())
        self.add_widget(b)

        b = Button(text='Press to stop reading from flow sensor',
                 size_hint = (0.5, 0.1))
        b.bind(on_press = lambda x: self.stop_flow_listen())
        self.add_widget(b)



class OxygenAdjustment(BoxLayout):
    def __init__(self, setting_label, percent,  **kwargs):
        super(OxygenAdjustment, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.setting_label = setting_label
        self.percent = percent


        top = Label(text = setting_label,
                    font_size = 35,
                    color = [0,0,0,1],
                    size_hint = (1,0.4))
        middle = Label(text = str(percent),
                       font_size = 30,
                       color = [0,0,0,1],
                       size_hint = (1, 0.5))
        
        dials = BoxLayout(orientation = 'vertical',
                          padding = [20,5],
                          spacing = 2,
                          size_hint = (1,1))
        
        up_arrow = Button(text = 'UP', 
                          font_size = 20,
                          background_normal = '',
                          background_color = [0.1, 0.3906, 0.70, 1])
        down_arrow = Button(text = 'DOWN',
                          font_size = 20,
                          background_normal = '',
                          background_color = [0.1, 0.3906, 0.70, 1])


        dials.add_widget(up_arrow)
        dials.add_widget(down_arrow)

        self.add_widget(top)
        self.add_widget(middle)
        self.add_widget(dials)



class ParametersTab(BoxLayout):
    def __init__(self, **kwargs):
        super(ParametersTab, self).__init__(**kwargs)
        self.add_widget(OxygenAdjustment(setting_label = 'SPO2 High',
                                         percent = '99 %'))
        self.add_widget(OxygenAdjustment(setting_label = 'SPO2 Low',
                                         percent = '87 %'))


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
		tab.add_widget(ParametersTab())
		tabs.add_widget(tab)

		return tabs

if __name__ == '__main__':
    O2App().run()








