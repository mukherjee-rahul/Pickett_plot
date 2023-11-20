import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.widgets import Button, Slider, TextBox

class Pickett_plot():
    
    def __init__(self,x,y) -> None:

        self.sat_lines = []
        # print('Object created')
        # Create the figure and the line that we will manipulate
        self.x,self.y = x,y
        self.fig, self.ax = plt.subplots()#figsize=(6,6),dpi=300)
        
        # adjust the main plot to make room for the sliders
        self.fig.subplots_adjust(top=0.75)
        

        rect = (0.125, 0.75, 0.9-0.125-0.125, 0.03)
        self.ax_slider_Rwa = self.fig.add_axes(rect)
        self.ax_textbox_Rwa = self.fig.add_axes([0.85, 0.75, 0.05, 0.05])
        self.ax_slider_a = self.fig.add_axes([0.125, 0.80, 0.15, 0.03])
        self.ax_slider_n = self.fig.add_axes([0.125+0.15+0.1, 0.80, 0.15, 0.03])
        self.ax_slider_m = self.fig.add_axes([0.125+2*(0.15+0.1), 0.80, 0.15, 0.03])
        self.ax_button_save = self.fig.add_axes([0.125, 0.85, 0.15, 0.05])
        

        #Create sliders
        self.slider_Rwa = Slider(
        ax=self.ax_slider_Rwa,
        label='Rwa',
        valmin=0.0001,
        valmax=1,
        valinit=0.033,valstep=0.0001#valstep=np.exp(np.linspace(np.log(0.00001),0,10000))
        )
        self.textbox_Rwa=TextBox(self.ax_textbox_Rwa,' ',initial=self.slider_Rwa.val)

        self.slider_m = Slider(
        ax=self.ax_slider_m,
        label='m',
        valmin=1,
        valmax=3,
        valinit=2,valstep=0.05
        )

        self.slider_n = Slider(
        ax=self.ax_slider_n,
        label='n',
        valmin=1,
        valmax=3,
        valinit=2,valstep=0.05
        )

        self.slider_a = Slider(
        ax=self.ax_slider_a,
        label='a',
        valmin=0.5,
        valmax=2,
        valinit=1,valstep=0.05
        )

        #Save button
        self.button_save = Button(
            self.ax_button_save,label='Save Fig'
            )

        self.plot_saturation(Rwa=self.slider_Rwa.val,m=self.slider_m.val,a=self.slider_a.val,n=self.slider_n.val)
        self.slider_Rwa.on_changed(self.update)
        self.slider_m.on_changed(self.update)
        self.slider_a.on_changed(self.update)
        self.slider_n.on_changed(self.update)

        self.textbox_Rwa.on_submit(self.text_box_submit)
        self.button_save.on_clicked(self.button_clicked)

        plt.show()

    #Plotting of saturation line
    def plot_saturation(self,Rwa,m=2,a=1,n=2,update=0):
        if not(update):
            #Clear the axes of any previous plots
            # self.ax.clear()
            self.ax.set_xlabel('Rt')
            self.ax.set_ylabel('Porosity')
            self.ax.set_xscale('log')
            self.ax.set_yscale('log')
            self.ax.set_xlim(xmin=0.1,xmax=10000)
            #Plotting of saturation line
            # Saturation line draw
            
            sw=(1.0,0.8,0.6,0.4,0.2)
            phie=(0.01,1)
            rt=np.zeros((len(sw),len(phie)))
                            
            for i in range (0,len(sw)):
                for j in range (0,len(phie)):
                    rt_out=((a*Rwa)/(sw[i]**n)/(phie[j]**m))
                    rt[i,j]=rt_out      
            for i in range(0,len(sw)):
                line = self.ax.plot(rt[i],phie, label='SW '+str(int(sw[i]*100))+'%')
                self.sat_lines.append(line)
                self.ax.legend (loc='best')

                self.ax.grid(which='both')
            
            #plot the scatter plot of actual data
            self.ax.scatter(self.x,self.y,marker='.')
        else:
            sw=(1.0,0.8,0.6,0.4,0.2)
            phie=(0.01,1)
            rt=np.zeros((len(sw),len(phie)))

            for i in range (0,len(sw)):
                for j in range (0,len(phie)):
                    rt_out=((a*Rwa)/(sw[i]**n)/(phie[j]**m))
                    rt[i,j]=rt_out      
            for i in range(0,len(sw)):
                # line = self.ax.plot(rt[i],phie, label='SW '+str(int(sw[i]*100))+'%')
                # print(self.sat_lines[i])
                self.sat_lines[i][0].set_xdata(rt[i])
                self.sat_lines[i][0].set_ydata(phie)
                # self.sat_lines[i][0].append(line)
                self.ax.legend (loc='best')

                # self.ax.grid(which='both')
            
            #plot the scatter plot of actual data
            # self.ax.scatter(self.x,self.y,marker='.')


    def update(self,val):
        self.plot_saturation(Rwa=self.slider_Rwa.val,m=self.slider_m.val,a=self.slider_a.val,n=self.slider_n.val,update=1)
        self.textbox_Rwa.set_val(self.slider_Rwa.val.__format__('.4f'))
    
    def text_box_submit(self,text):
        value = float(text)
        self.slider_Rwa.set_val(value)
        self.plot_saturation(Rwa=self.slider_Rwa.val,m=self.slider_m.val,a=self.slider_a.val,n=self.slider_n.val,update=1)

    def button_clicked(self,event):
        self.fig.canvas.draw_idle()
        print('button clicked')
        self.fig.savefig('output_figure_different_dpi.png',dpi=300)


if __name__=='__main__':
    data = pd.read_csv('sample_data.csv')
    print(data.columns)
    Pickett_plot(data[data['PHIT']>0.1]['Rt'], data[data['PHIT']>0.1]['PHIT'])