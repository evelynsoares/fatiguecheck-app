import math
import matplotlib.pyplot as plt

#Calculo do EImin
pi = math.pi

print("Qual o tipo do cabo?")
tipo_cabo = input() 

if tipo_cabo == "ACSR" or tipo_cabo == "acsr":
    print("Qual o numero de cabos da camada de aço?")
    num_aco = int(input())
    E_aco = 200 #200 GPa
    print("Qual o diametro do fio de aço? (milimetro)")
    diam_aco = int(input())

    print("Qual o numero de cabos da camada de aluminio?")
    num_alu = int(input())
    E_alu = 69 #69 GPa
    print("Qual o diametro do fio de aluminio? (milimetro)")
    diam_alu = int(input())

    EImin = num_aco*E_aco*pi*(diam_aco**4) + num_alu*E_alu*pi*(diam_alu**4) #(10^(-3))^4 = 10^-12, ao multiplicar por GPa -> 0.001 = 10^(-3)
else:
    print("Qual o numero de cabos da camada de aluminio?")
    num_alu = int(input())
    E_alu = 69 #69 GPa
    print("Qual o diametro do fio de aluminio? (milimetro)")
    diam_alu = int(input())
    
    EImin = num_alu*E_alu*pi*(diam_alu**4) #(10^(-3))^4 = 10^-12, ao multiplicar por GPa -> 0.001 = 10^(-3)

EImin *= 0.001
print("A rigidez a flexão minima é: EImin =", EImin, "N*m^2") # m^3*kg / s^2 = N*m^2

print("Para calcular a vida útil do cabo " + tipo_cabo + " digite o valor da força de tração em Newtons ou carga de ruptura\n") #REVISAO
#Cabo de aluminio
T = float(input())
t_u = 0.2*T

x = 89 #mm
p = math.sqrt(T/EImin)

K = (E_alu*diam_alu*pow(p, 2))/(4*(math.exp(-p*x)-1+p*x))

#Leitura da tabela
print("Insira os valores da amplitude") # exemplo de 10 valores
n = 10
Yb = [int(input()) for i in range(n)]
S = [0,0,0,0,0,0,0,0,0,0]

for j in range(n):
    S[j] = K*(Yb[j])

#exemplos
N = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]

#tabela = tabula.read_pdf("TabelaVibrografo.pdf", pages="all")
#print(len(tabela))
#for tabela in r:
#	display(tabela)

plt.xlabel('N - numero de ciclos')
plt.ylabel('S')
plt.title("Curva SN")
plt.plot(N, S)
plt.show()
