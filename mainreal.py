from kivy.app import App
from kivy.base import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
import tkinter as tk
from tkinter import filedialog
import math
import matplotlib.pyplot as plt
from rigidez_minima import rigidez_minima
from sigmaa import sigmaa
from safeborderline import safeborderline
import numpy as np
import csv
import io 
from PIL import Image


class SplashArt(Screen):
    pass
    
class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    file = open("C:\\Users\\Evelyn Soares\\Documents\\Codes\\fatiguecheck-app\\MedicaoVibrografoCSV.csv", 'r')
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
    Sa=sigmaa(yb_array,T,EI,dal,Eal)
    N=safeborderline(Sa)
    Di=array_numpy_ciclos/N #Calculo dos danos para ni e Ni
    D=np.sum(Di.astype(float))
    D_ext_ano=((365/t_instal)*D) #Dano extrapolado para o período de 1 ano
    Vida=1/D
    Vida_anos=(1/D_ext_ano)-T

    rigidez_min_text = f"A rigidez mínima, Ei, é: {EI:.2f}"
    dano_text = f"O dano á fadiga é: {D}\nO dano varia de 0 a 1."
    vida_anos_text = f"A vida útil do cabo é de: {Vida_anos:.2f} anos"
    pass

class ThirdWindow(Screen):
    #grafico curva SN
    xaxis = np.array([2, 8])
    yaxis = np.array([4, 9])
    plt.plot(xaxis, yaxis)
    plt.title("Curva S-N")
    plt.xlabel('Numero de ciclos') 
    plt.ylabel("Tensão (N)") 
    
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


class testsApp(App):
    pass

testsApp().run()