from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout        
from kivy.uix.button import Button
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
from kivy.clock import Clock, ClockEvent


import matplotlib.pyplot as plt

from time import sleep
from data_handler import *
from flow_reader import FlowReader


def enter_axes(event):
    print('enter_axes', event.inaxes)
    event.inaxes.patch.set_facecolor('yellow')
    event.canvas.draw()


def leave_axes(event):
    print('leave_axes', event.inaxes)
    event.inaxes.patch.set_facecolor('white')
    event.canvas.draw()


def enter_figure(event):
    print('enter_figure', event.canvas.figure)
    event.canvas.figure.patch.set_facecolor('red')
    event.canvas.draw()


def leave_figure(event):
    print('leave_figure', event.canvas.figure)
    event.canvas.figure.patch.set_facecolor('grey')
    event.canvas.draw()


kv = """
<Test>:
    orientation: 'vertical'
    # Button:
    #     size_hint_y: None
    #     height: 100
"""

Builder.load_string(kv)


host = socket.gethostname()
port = 50000

# instantiate a data handler 
dh = DataHandler(host, port)

fr = FlowReader()
fr.create_data_file()


class Test(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

        self.wid, self.ax = self.get_fc(1)
        self.add_widget(self.wid)
        self.add_mybuttons()
        self.listener = None


    def get_fc(self, i):
        """
        Build the figure and connect events to the canvas
        """
        fig1 = plt.figure(facecolor = [0.2,0.2,0.2])
        fig1.suptitle('mouse hover over figure or axes to trigger events' +
                      str(i))
        ax1 = fig1.add_subplot(1,1,1, axisbg = [0.17,0.17,0.17])
        wid = FigureCanvas(fig1)
        fig1.canvas.mpl_connect('figure_enter_event', enter_figure)
        fig1.canvas.mpl_connect('figure_leave_event', leave_figure)
        fig1.canvas.mpl_connect('axes_enter_event', enter_axes)
        fig1.canvas.mpl_connect('axes_leave_event', leave_axes)

        return wid, ax1 #, fig1


    def animate(self):
        """
        Read data from the socket and update the graph
        """
        try:
            #values, count = dh.listen()
            dh.listen()
        except:
            pass
            #print ("We're having issues")
        else:
            #print (dh.values)
            xs = [x for x in range(len(dh.values))]

            self.ax.clear()
            self.ax.plot(xs, dh.values, linewidth = 3)

            # dh.values[-200::].... need to implement something to adjust the axes
            plt.axis([len(dh.values)-200, len(dh.values)+10, min(dh.values)-5, max(dh.values) + 2])
            self.ax.figure.canvas.draw()
#            self.fig.canvas.draw()
            print ("Drawing")

    def plot_flow(self):
        try:
            fr.read_sensor()
        except:
            print ('Got an error..')
        else:
            xs = [x for x in range(len(fr.values))]

            self.ax.clear()
            self.ax.plot(xs, fr.values, linewidth = 3)

            #plt.axis([len(fr.values)-200, len(fr.values)+10, min(fr.values)-5, max(fr.values) + 2])
            self.ax.figure.canvas.draw()
            print ('Drawing flow')
  
    def start_sock_listen(self):
        """
        This will be called by a button press. Subseqently
        this function will call the animate() function in 
        this class every 0.5 seconds to update the graph.
        """
        Clock.schedule_interval(lambda x: self.animate(), 0.5)
        print ('sock listening')

    def stop_sock_listen(self):
        Clock.unschedule(lambda x: self.animate())
        dh.disconnect()

    def start_flow_listen(self):
        self.listener = Clock.schedule_interval(lambda x: self.plot_flow(), 0.5)

    def stop_flow_listen(self):
        #Clock.unschedule(lambda x: self.plot_flow())
        self.listener.cancel()
        #Clock.schedule_once(lambda x: self.plot_flow(), 0.5)
        print ('unscheduled')

    def add_mybuttons(self):
        """
        Build the buttons 
        """
        b = Button(text = 'Press to connect',
                 size_hint = (0.5, 0.1))
        b.bind(on_press = lambda x: dh.connect())
        self.add_widget(b)

        b = Button(text='Press to get data from socket',
                 size_hint = (0.5, 0.1))
        #b.bind(on_press = lambda x: self.animate())
        b.bind(on_press = lambda x: self.start_sock_listen())
        self.add_widget(b)

        b = Button(text='Press to disconnect from socket',
                 size_hint = (0.5, 0.1))
        b.bind(on_press = lambda x: self.stop_sock_listen())
        self.add_widget(b)

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

def main():
    TestApp().run()
    

if __name__ == '__main__':
    main()