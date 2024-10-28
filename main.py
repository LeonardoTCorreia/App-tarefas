import tkinter as tk 
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage


# criando janela do app
janela = tk.Tk()
janela.title("Gerenciador de Tarefas")
janela.configure(bg="#F0F0F0")
janela.geometry("500x600")


fonte_cabecalho = font.Font(family="Garamond", size=24, weight="bold")
rotulo_cabecalho = tk.Label(janela, text="Meu App de Tarefas",  font=fonte_cabecalho, bg="#F0F0F0", fg='#333').pack(pady=20)

frame = tk.Frame(janela, bg="#F0F0F0").pack(pady=10)

entrada_tarefa = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT, bg="White", fg="grey", width=30)
entrada_tarefa.pack(side=tk.LEFT, padx=10)

botao_adicionar = tk.Button(frame, text="Adicionar Tarefa", bg="#4CAF50", fg="white", height=1, width=15, font=("Arial", 11), relief=tk.FLAT)
botao_adicionar.pack(side=tk.LEFT, padx=10)

# Criando um frame para a lista de tarefas com rolagem
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=BOTH, expand=True, padx=10, pady=10)

janela.mainloop()