from kivy.app import App
from kivy.base import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.slider import Slider
import tkinter as tk
from tkinter import filedialog
import math
import matplotlib.pyplot as plt
from rigidez_minima import rigidez_minima
from sigmaa import sigmaa
from safeborderline import safeborderline
from SN import SN
import numpy as np
import csv
import io 
from PIL import Image

file = open(".\\files\\MedicaoVibrografoCSV.csv", 'r')
csvreader = csv.reader(file)
rows = []

for row in csvreader:
    rows.append(row)

file.close()
rows_em_array = np.array(rows)

coluna0 = (rows_em_array[:, 0])
coluna1 = (rows_em_array[:, 1])
coluna2 = (rows_em_array[:, 2])
coluna3 = (rows_em_array[:, 3])
coluna4 = (rows_em_array[:, 4])
coluna5 = (rows_em_array[:, 5])
coluna6 = (rows_em_array[:, 6])
coluna7 = (rows_em_array[:, 7])

ciclos_coluna1 = np.sum(coluna1.astype(float))
ciclos_coluna2 = np.sum(coluna2.astype(float))
ciclos_coluna3 = np.sum(coluna3.astype(float))
ciclos_coluna4 = np.sum(coluna4.astype(float))
ciclos_coluna5 = np.sum(coluna5.astype(float))
ciclos_coluna6 = np.sum(coluna6.astype(float))
ciclos_coluna7 = np.sum(coluna7.astype(float))

ciclos = []
for i in range(1, 8):
    nome_variavel = f'ciclos_coluna{i}'
    ciclos.append(locals()[nome_variavel])

array_numpy_ciclos = np.array(ciclos)

T=2586*9.81 
yb=[125,251,376,502,627,753,754]
yb_array=(np.array(yb))/1000
dal, da, na, nal = 3.5, 0, 0, 61
Eal=69000
n=100000
t_instal=30 #tempo de instalação do aparelho em dias
T=5 #Tempo de operação da linha em anos
EI=rigidez_minima(nal,dal,na,da)
Sa = sigmaa(yb_array,T,EI,dal,Eal)
N = safeborderline(Sa)

#mudanca nao ta fazendo nada
#N = SN(N)
#Sa = SN(N)

Di=array_numpy_ciclos/N #Calculo dos danos para ni e Ni
D=np.sum(Di.astype(float))
D_ext_ano=((365/t_instal)*D) #Dano extrapolado para o período de 1 ano
Vida=1/D
Vida_anos=(1/D_ext_ano)-T

#mudar pra grafico barra -> o signmaA é a tensao (ajuste a unidade)

class SplashArt(Screen):
    pass
    
class FirstWindow(Screen):
    pass

class FourthWindow(Screen):
    pass

class fileWidget(BoxLayout):
    #nao funnciona
    def selected(self, filename):
        try:
            # Set the source for the image display
            self.ids.image_display.source = filename[0]
        except Exception as e:
            print(f"Error loading image: {e}")
            self.ids.image_display.source = ""  # Clear image on error


      
            
class SecondWindow(Screen):
    filepathname_text = f"--file.path--" #ataualizer com nome do file
    rigidez_min_text = f"\nA rigidez mínima, Ei, é: {EI:.2f}"#, ciclos {ciclos} vs N {N} e Yb {yb} vs Sa{Sa}"
    dano_text = f"\nO dano á fadiga é: {D}\nO dano varia de 0 a 1."
    vida_anos_text = f"\nA vida útil do cabo é de: {Vida_anos:.2f} anos"
    pass

class ThirdWindow(Screen):

    # Função para plotar a curva SN
    def plotar_SN_curve():
        limite_superior=1e7
        pontos=1000
        """
        Gera uma curva SN a partir de valores simulados de N e Sa.
        
        :param limite_superior: Número máximo de ciclos para a curva (X-axis).
        :param pontos: Quantidade de pontos a serem plotados na curva.
        :return: Arrays para o número de ciclos N e a tensão Sa.
        """
        # Gerando valores para N (eixo X) e calculando Sa (eixo Y)
        #N = np.logspace(3, np.log10(limite_superior), pontos)  # Exemplo de ciclo de 1k a limite_superior
        N = np.linspace(1000, limite_superior, pontos)
        Sa = 450 * (N) ** -0.2  # Equação SN para amplitude de tensão
    
        fig, axs = plt.subplots(2, 1, figsize=(10, 10))  # 2 rows, 1 column

        # Plotando a curva SN
        axs[0].plot(N, Sa, label="Curva SN", color='blue')
        axs[0].set_xlabel("Número de Ciclos até Falha (N)")
        axs[0].set_ylabel("Amplitude de Tensão Alternada (Sa)")
        axs[0].set_title("Curva SN (Ciclos de Fadiga vs Tensão Alternada)")
        axs[0].legend()
        axs[0].grid(True, which="both", linestyle="--", lw=0.5)

        # Plotando o gráfico de barras
        bar_width = (N[-1] - N[0]) / (pontos - 1)  # Largura das barras
        axs[1].bar(N[:100], Sa[:100], width=bar_width, color='orange', label="Dados de SN")  # Plotando apenas os primeiros 50 pontos
        axs[1].set_xlabel("Número de Ciclos até Falha (N)")
        axs[1].set_ylabel("Amplitude de Tensão Alternada (Sa)")
        axs[1].set_title("Gráfico de Barras - Curva SN")
        axs[1].legend()
        axs[1].grid(True, which="both", linestyle="--", lw=0.5)

        # Ajustando o layout
        plt.tight_layout()


    # Plotando a curva SN
    plotar_SN_curve()

        
    fig = plt.gcf() 

    def fig2img(fig): 
        buf = io.BytesIO() 
        fig.savefig(buf) 
        buf.seek(0) 
        img = Image.open(buf) 
        return img 
    
    img = fig2img(fig) 
    img.save('./images/curvaSN.png') 




    pass

class WindowManager(ScreenManager):
    pass

#new changes
class kvappApp(App):
#    def build(self):
#        return Builder.load_file('kvapp.kv')  # Load kv file with same name

#if __name__ == '__main__':
#    kvappApp().run()
    pass

kvappApp().run()
