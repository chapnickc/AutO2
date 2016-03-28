from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout 
from kivy.lang import Builder
from kivy.clock import Clock

import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas

from flow_reader import FlowReader

fr = FlowReader()

fr = FlowReader()


kv = """
<Test>:
    orientation: 'vertical'
"""

Builder.load_string(kv)


class Test(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        
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





class TestApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()








