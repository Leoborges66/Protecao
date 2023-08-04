import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#oi
root = tk.Tk()
root.title('Gráfico Interativo')

Icc_value = tk.StringVar()
U_value = tk.StringVar()
S_value = tk.StringVar()
Kf_value = tk.StringVar()
RTC_value = tk.StringVar()
Iatf_value = tk.StringVar()
curva_value = tk.StringVar()

curvas = ["Normalmente Inversa", "Muito Inversa",
          "Extremamente Inversa", "Inversa Longa", "Inversa Curta"]
curva_value.set(curvas[0])  # Definir a curva padrão como "Normalmente Inversa"

Icc_label = tk.Label(root, textvariable=Icc_value)
Icc_label.pack()

U_label = tk.Label(root, textvariable=U_value)
U_label.pack()

S_label = tk.Label(root, textvariable=S_value)
S_label.pack()

Kf_label = tk.Label(root, textvariable=Kf_value)
Kf_label.pack()

RTC_label = tk.Label(root, textvariable=RTC_value)
RTC_label.pack()

Iatf_label = tk.Label(root, textvariable=Iatf_value)
Iatf_label.pack()

canvas = None

is_temporizado = tk.BooleanVar()
temporizacao_entry = tk.StringVar()


def plotar_grafico(Icc, U, S, Kf, is_temporizado, tempo_temporizacao, tipo_curva):

    global canvas, Icc_value, U_value, S_value, Kf_value, RTC_label, Iatf_label

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    Fs = 20  # Fator de sobrecarga

    In = S/(np.sqrt(3)*U)
    Itc = Icc/Fs

    if In > Itc:
        quociente = In / 100
        quociente_arredondado = math.ceil(quociente)
        ItcSup = quociente_arredondado * 100
    else:
        quociente = Itc / 100
        quociente_arredondado = math.ceil(quociente)
        ItcSup = quociente_arredondado * 100

    RTC = ItcSup/5
    Itf = (Kf * In)/RTC
    Iatf = Itf * RTC  # Corrente de acionamento

    # M = Icc/Iatf ->                           # Múltiplo da corrente de acionamento para a corrente de curto

    # Funções para achar o valor de Tms
    def Tms_Normalmente_Inversa(T, Icc, Iatf):
        return ((Icc/Iatf)**0.02 - 1)*T/0.14

    def Tms_Muito_Inversa(T, Icc, Iatf):
        return ((Icc/Iatf)-1)*T/13.5

    def Tms_Extremamente_Inversa(T, Icc, Iatf):
        return T*((Icc/Iatf)**2 - 1)/80

    def Tms_Inversa_longa(T, Icc, Iatf):
        return T*((Icc/Iatf) - 1)/120

    def Tms_Inversa_Curta(T, Icc, Iatf):
        return T*((Icc/Iatf)**0.04 - 1)/0.05

    # Atualizar os valores das variáveis
    RTC_value.set(f'RTC: {RTC:.2f}')
    Iatf_value.set(f'Corrente de acionamento: {Iatf:.2f}A')

    if is_temporizado:

        M = np.linspace(1.5, 20, 180)
        fig, ax = plt.subplots()

        if tipo_curva == "Normalmente Inversa":
            Tms = Tms_Normalmente_Inversa(tempo_temporizacao, Icc, Iatf)
            Ts = 0.14*Tms/((M)**0.02 - 1)
            ax.plot(M, Ts, label='Normalmente Inversa')
        elif tipo_curva == "Muito Inversa":
            Tms = Tms_Muito_Inversa(tempo_temporizacao, Icc, Iatf)
            Ts = 13.5*Tms/((M) - 1)
            ax.plot(M, Ts, label='Muito Inversa')
        elif tipo_curva == "Extremamente Inversa":
            Tms = Tms_Extremamente_Inversa(tempo_temporizacao, Icc, Iatf)
            Ts = 80*Tms/((M)**2 - 1)
            ax.plot(M, Ts, label='Extremamente Inversa')
        elif tipo_curva == "Inversa Longa":
            Tms = Tms_Inversa_longa(tempo_temporizacao, Icc, Iatf)
            Ts = 120*Tms/((M) - 1)
            ax.plot(M, Ts, label='Inversa Longa')
        elif tipo_curva == "Inversa Curta":
            Tms = Tms_Inversa_Curta(tempo_temporizacao, Icc, Iatf)
            Ts = 0.05*Tms/((M)**0.04 - 1)
            ax.plot(M, Ts, label='Inversa Curta')

        linha_inicial_x = M[0]
        linha_final_x = M[179]
        linha_inicial_y = Ts[0]
        linha_final_y = Ts[179]
        ax.plot([linha_inicial_x, linha_inicial_x], [
                linha_inicial_y, 0], linestyle='dashed', color='gray')
        ax.text(linha_inicial_x, 0,
                f'{linha_inicial_x:.2f}', ha='center', va='top')
        ax.plot([linha_final_x, linha_final_x], [linha_final_y, 0],
                linestyle='dashed', color='gray')
        ax.hlines(y=0, xmin=20, xmax=30, colors='red',
                  linewidth=3, linestyle='solid')
        ax.set_ylim(0, Ts.max()*1.1)
        ax.set_xlim(0, 30)

        ax.set_xlabel('Múltiplo da corrente')
        ax.set_ylabel('Tempo[s]')
        ax.set_title('Gráfico do tempo de resposta do relé')
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        M = np.linspace(1.5, 20, 180)
        linha_inicial_x = M[0]
        fig, ax = plt.subplots()
        ax.hlines(y=0, xmin=1.5, xmax=30, colors='red',
                  linewidth=3, linestyle='solid')
        ax.text(linha_inicial_x, 0,
                f'{linha_inicial_x:.2f}', ha='center', va='top')
        ax.set_ylim(0, 10)
        ax.set_xlim(0, 30)
        ax.set_xlabel('Múltiplo da corrente')
        ax.set_ylabel('Tempo[s]')
        ax.set_title('Gráfico do tempo de resposta do relé')
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()



def atualizar_rele():
    try:
        Icc = float(Icc_entry.get())
        U = float(U_entry.get())
        S = float(S_entry.get())
        Kf = float(Kf_entry.get())
        is_temporizado_value = is_temporizado.get()
        tempo_temporizacao_value = float(
            temporizacao_entry.get()) if is_temporizado_value else None
        tipo_curva_value = curva_value.get()
        plotar_grafico(Icc, U, S, Kf, is_temporizado_value,
                       tempo_temporizacao_value, tipo_curva_value)
    except ValueError:
        print("Erro: Certifique-se de que os valores estão corretos.")


Icc_label = tk.Label(root, text='Icc:')
Icc_label.pack()
Icc_entry = tk.Entry(root)
Icc_entry.pack()

U_label = tk.Label(root, text='U:')
U_label.pack()
U_entry = tk.Entry(root)
U_entry.pack()

S_label = tk.Label(root, text='S:')
S_label.pack()
S_entry = tk.Entry(root)
S_entry.pack()

Kf_label = tk.Label(root, text='Kf:')
Kf_label.pack()
Kf_entry = tk.Entry(root)
Kf_entry.pack()

temporizado_checkbtn = tk.Checkbutton(
    root, text="Temporizado", variable=is_temporizado)
temporizado_checkbtn.pack()

temporizacao_label = tk.Label(root, text="Tempo de Temporização:")
temporizacao_label.pack()
temporizacao_entry = tk.Entry(root)
temporizacao_entry.pack()

curva_label = tk.Label(root, text="Tipo de Curva:")
curva_label.pack()
curva_menu = tk.OptionMenu(root, curva_value, *curvas)
curva_menu.pack()

atualizar_btn = tk.Button(
    root, text='Atualizar Relé', command=atualizar_rele)
atualizar_btn.pack()


def ao_fechar():
    root.destroy()
    root.quit()


root.protocol("WM_DELETE_WINDOW", ao_fechar)

root.mainloop()
