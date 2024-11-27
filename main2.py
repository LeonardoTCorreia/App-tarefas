import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage
import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect("tarefas.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL
)
""")
conn.commit()

# Funções para o banco de dados
def carregar_tarefas():
    cursor.execute("SELECT id, descricao FROM tarefas")
    return cursor.fetchall()

def salvar_tarefa_no_banco(descricao):
    cursor.execute("INSERT INTO tarefas (descricao) VALUES (?)", (descricao,))
    conn.commit()
    return cursor.lastrowid

def atualizar_tarefa_no_banco(id_tarefa, nova_descricao):
    cursor.execute("UPDATE tarefas SET descricao = ? WHERE id = ?", (nova_descricao, id_tarefa))
    conn.commit()

def deletar_tarefa_no_banco(id_tarefa):
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
    conn.commit()

frame_em_edicao = None
# Função para adicionar tarefa
def adicionar_tarefa():
    global frame_em_edicao
    tarefa = entrada_tarefa.get().strip()
    if tarefa and tarefa != "Escreva sua tarefa aqui":
        if frame_em_edicao is not None:
            atualizar_tarefa(tarefa)
            frame_em_edicao = None
        else:
            id_tarefa = salvar_tarefa_no_banco(tarefa)
            adicionar_item_tarefa(id_tarefa, tarefa)
            entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrada inválida", "Por favor, insira uma tarefa!")

# Adicionar item de tarefa na interface
def adicionar_item_tarefa(id_tarefa, tarefa):
    frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)

    label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=("Garamond", 16), bg="white", width=25, height=2, anchor="w")
    label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

    botao_editar = tk.Button(frame_tarefa, image=icon_editar,
                             command=lambda f=frame_tarefa, l=label_tarefa, id=id_tarefa: preparar_edicao(f, l, id),
                             bg="white", relief=tk.FLAT)
    botao_editar.pack(side=tk.RIGHT, padx=5)

    botao_deletar = tk.Button(frame_tarefa, image=icon_deletar,
                              command=lambda f=frame_tarefa, id=id_tarefa: deletar_tarefa(f, id),
                              bg="white", relief=tk.FLAT)
    botao_deletar.pack(side=tk.RIGHT, padx=5)

    frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

    checkbutton = ttk.Checkbutton(frame_tarefa, command=lambda label=label_tarefa: alternar_sublinhado(label))
    checkbutton.pack(side=tk.RIGHT, padx=5)

    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def preparar_edicao(frame_tarefa, label_tarefa, id_tarefa):
    global frame_em_edicao
    frame_em_edicao = (frame_tarefa, id_tarefa)
    entrada_tarefa.delete(0, tk.END)
    entrada_tarefa.insert(0, label_tarefa.cget("text"))

def atualizar_tarefa(nova_tarefa):
    global frame_em_edicao
    frame_tarefa, id_tarefa = frame_em_edicao
    for widget in frame_tarefa.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(text=nova_tarefa)
            atualizar_tarefa_no_banco(id_tarefa, nova_tarefa)

def deletar_tarefa(frame_tarefa, id_tarefa):
    frame_tarefa.destroy()
    deletar_tarefa_no_banco(id_tarefa)
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def alternar_sublinhado(label):
    fonte_atual = label.cget("font")
    if "overstrike" in fonte_atual:
        nova_fonte = fonte_atual.replace(" overstrike", "")
    else:
        nova_fonte = fonte_atual + " overstrike"
    label.config(font=nova_fonte)

# Interface
janela = tk.Tk()
janela.title("Gerenciador de Tarefas")
janela.configure(bg="#F0F0F0")
janela.geometry("500x600")

icon_editar = PhotoImage(file="imgs/edit.png").subsample(23, 23)
icon_deletar = PhotoImage(file="imgs/delete.png").subsample(10, 10)

fonte_cabecalho = font.Font(family="Garamond", size=24, weight="bold")
rotulo_cabecalho = tk.Label(janela, text="Meu App de Tarefas", font=fonte_cabecalho, bg="#F0F0F0", fg='#333').pack(pady=20)

frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)

entrada_tarefa = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT, bg="White", fg="grey", width=30)
entrada_tarefa.pack(side=tk.LEFT, padx=10)
entrada_tarefa.bind("<Return>", lambda event: adicionar_tarefa())

botao_adicionar = tk.Button(frame, command=adicionar_tarefa, text="Adicionar Tarefa", bg="#4CAF50", fg="white",
                             height=1, width=15, font=("Arial", 11), relief=tk.FLAT)
botao_adicionar.pack(side=tk.LEFT, padx=10)

# Criar lista de tarefas com rolagem
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(frame_lista_tarefas, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame_lista_tarefas, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Carregar tarefas do banco de dados
for id_tarefa, descricao in carregar_tarefas():
    adicionar_item_tarefa(id_tarefa, descricao)

janela.mainloop()
