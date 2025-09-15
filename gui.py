import tkinter as tk
from PIL import Image, ImageTk
from config import largura_tela, altura_tela, linha_radar_y, radar_ligado
from carro import Carro
from database import fechar_conexao

# --- Função para alternar radar ---
def toggle_radar():
    global radar_ligado
    radar_ligado = not radar_ligado
    status.set("Radar: Ligado" if radar_ligado else "Radar: Desligado")

# --- Inicialização da janela ---
root = tk.Tk()
root.title("Simulação Radar")
canvas = tk.Canvas(root, width=largura_tela, height=altura_tela, bg="white")
canvas.pack()

btn = tk.Button(root, text="Ligar/Desligar Radar", command=toggle_radar)
btn.pack(pady=5)

status = tk.StringVar()
status.set("Radar: Desligado")
label_status = tk.Label(root, textvariable=status)
label_status.pack()

# --- Carregar imagens ---
img_azul = Image.open("img/carro_azul.png").resize((90,120))
img_vermelho = Image.open("img/carro_vermelho.jpg").resize((90,120))
carro_azul = ImageTk.PhotoImage(img_azul)
carro_vermelho = ImageTk.PhotoImage(img_vermelho)
imagens_carro = {"azul": carro_azul, "vermelho": carro_vermelho}

# --- Criar carros ---
carros = [Carro(canvas, imagens_carro) for _ in range(5)]

# --- Função de atualização ---
def atualizar():
    canvas.delete("linha_radar")
    canvas.create_line(0, linha_radar_y, largura_tela, linha_radar_y, fill="green", width=2, tags="linha_radar")
    for carro in carros:
        carro.mover()
    root.after(30, atualizar)

atualizar()
root.mainloop()
fechar_conexao()
