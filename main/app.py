from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout 
from kivy.lang import Builder

import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas


kv = """
<Test>:
    orientation: 'vertical'
"""

Builder.load_string(kv)


class Test(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        
        self.wid, self.ax = self.get_fc(1)
        self.add_widget(self.wid)



    def get_fc(self, i):
        """
        Build the figure 
        """
        fig = plt.figure()
        ax1 = fig1.add_subplot(1,1,1) 
        wid = FigureCanvas(fig)
        
        return wid, ax1

    def add_buttons(self):

        b = Button(text='Press to read from flow sensor',
                 size_hint = (0.5, 0.1))
#        b.bind(on_press = lambda x: self.start_flow_listen())
        self.add_widget(b)

        b = Button(text='Press to stop reading from flow sensor',
                 size_hint = (0.5, 0.1))
#        b.bind(on_press = lambda x: self.stop_flow_listen())
        self.add_widget(b)





class TestApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()








