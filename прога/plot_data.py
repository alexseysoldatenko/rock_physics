import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

class plot_object():

    def __init__(self, component_number, component_data, grid_x1, grid_x2):
        self.component_number = component_number
        self.component_data = component_data
        self.grid_x1 = grid_x1
        self.grid_x2 = grid_x2

    def plot_slice(self, slice_number, axes_info):
        fig, ax = plt.subplots()
        if axes_info == "phi":
            ax.plot(self.grid_x1, self.component_data[:,slice_number])
            ax.set_title(f"k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}, {axes_info}, const = {self.grid_x2[slice_number]}")
        elif axes_info == "tetta":
            ax.plot(self.grid_x2, self.component_data[slice_number])
            ax.set_title(f"k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}, {axes_info}, const = {self.grid_x1[slice_number]}")
        else:
            raise Exception('Unknown name of ax only tetta and phi')
       
        ax.set_xlabel(axes_info)
        ax.set_ylabel("component value")
        plt.show()

    def plot_3d(self):
        # ПРОИСХОДИТ ТРАНСПОНИРОВАНИЕ РЕЗУЛЬТАТА ДЛЯ ОТОБРАЖЕНИЯ 
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
        self.grid_x1, self.grid_x2 = np.meshgrid(self.grid_x1, self.grid_x2)
        ax.plot_surface(self.grid_x1, self.grid_x2, self.component_data.T, cmap=cm.coolwarm)
        ax.set_title(f"k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}")
        ax.set_xlabel("phi")
        ax.set_ylabel("tetta")
        plt.show()
    
    def save_slice(self, slice_number, axes_info):
        fig, ax = plt.subplots()
        if axes_info == "phi":
            slice_number = int(slice_number*self.component_data.shape[1])
            ax.plot(self.grid_x1, self.component_data[:,slice_number])
            ax.set_title(f"k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}, phi const = {np.round(self.grid_x2[slice_number],2)}")
        elif axes_info == "tetta":
            slice_number = int(slice_number*self.component_data.shape[0])
            ax.plot(self.grid_x2, self.component_data[slice_number])
            ax.set_title(f"k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}, tetta const = {np.round(self.grid_x1[slice_number],2)}")
        else:
            raise Exception('Unknown name of ax only tetta and phi')
        
        ax.set_ylabel("component value")
        if axes_info == "tetta":
            axes_info = "phi"
        elif axes_info == "phi":
            axes_info = "tetta"
        ax.set_xlabel(axes_info)
        if axes_info == "tetta":
            axes_info = "phi"
        elif axes_info == "phi":
            axes_info = "tetta"
        plt.savefig(f'''test29.05.2022(1000,1000,1)//k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}, {axes_info} = {slice_number}.png''')


    def save_3d(self):
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
        self.grid_x1, self.grid_x2 = np.meshgrid(self.grid_x1, self.grid_x2)
        ax.plot_surface(self.grid_x1, self.grid_x2, self.component_data.T, cmap=cm.coolwarm)
        ax.set_title(f"k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}")
        ax.set_xlabel("tetta")
        ax.set_ylabel("phi")
        # plt.savefig(f'''test09.05.2022(1,1000,1000, 4 grid)//k = {self.component_number[0]}, m = {self.component_number[1]}, l = {self.component_number[2]}, n = {self.component_number[3]}//k = {self.component_number[0]}, m = {self.component_number[1]}, l = {self.component_number[2]}, n = {self.component_number[3]}.png''')
        plt.savefig(f'''all01.06.2022(1,1,1)//test1000k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}.png''')

    def plot6(self):
        fig, ax = plt.subplots(2,3, figsize= (20,10))
        for axes_info in ["phi", "tetta"]:
            if axes_info == "phi":
                num2 = 0
            else:
                num2 = 1
            for slice_number in [.25, .5, .75]:
                num1 = int(slice_number/0.25 - 1)
       
                
                

                
                if axes_info == "phi":
                    slice_number = int(slice_number*self.component_data.shape[1])
                    ax[num2, num1].plot(self.grid_x1, self.component_data[:,slice_number])
                    ax[num2, num1].set_title(f"k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}, phi const = {np.round(self.grid_x2[slice_number],2)}")
                elif axes_info == "tetta":
                    slice_number = int(slice_number*self.component_data.shape[0])
                    ax[num2, num1].plot(self.grid_x2, self.component_data[slice_number])
                    ax[num2, num1].set_title(f"k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}, tetta const = {np.round(self.grid_x1[slice_number],2)}")
                else:
                    raise Exception('Unknown name of ax only tetta and phi')
                
                ax[num2, num1].set_ylabel("component value")
                if axes_info == "tetta":
                    axes_info = "phi"
                elif axes_info == "phi":
                    axes_info = "tetta"
                ax[num2, num1].set_xlabel(axes_info)
                if axes_info == "tetta":
                    axes_info = "phi"
                elif axes_info == "phi":
                    axes_info = "tetta"
        plt.savefig(f'''six01.06.2022(1,1,1)//k = {self.component_number[0]+1}, m = {self.component_number[1]+1}, l = {self.component_number[2]+1}, n = {self.component_number[3]+1}.png''')