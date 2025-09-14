import tkinter as tk
import random
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk

# --- CONFIGURAÇÕES ---
limite_velocidade = 60
largura_tela, altura_tela = 800, 600
linha_radar_y = altura_tela // 2
radar_ligado = False  # começa desligado

# --- BANCO DE DADOS SQLITE ---
conn = sqlite3.connect("radar.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS ocorrencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT,
    velocidade INTEGER,
    limite INTEGER,
    data TEXT,
    hora TEXT
)
''')
conn.commit()

# --- FUNÇÕES ---
def gerar_placa():
    letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numeros = ''.join(random.choices('0123456789', k=4))
    return f"{letras}-{numeros}"

def registrar_veiculo(placa, velocidade):
    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")
    cursor.execute('''
        INSERT INTO ocorrencias (placa, velocidade, limite, data, hora)
        VALUES (?, ?, ?, ?, ?)
    ''', (placa, velocidade, limite_velocidade, data, hora))
    conn.commit()
    print(f"Radar: Placa={placa}, Velocidade={velocidade} km/h registrada!")

def toggle_radar():
    global radar_ligado
    radar_ligado = not radar_ligado
    status.set("Radar: Ligado" if radar_ligado else "Radar: Desligado")

# --- TKINTER ---
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

# --- CARREGAR IMAGENS ---
img_azul = Image.open("carro_azul.png").resize((90,120))
img_vermelho = Image.open("carro_vermelho.jpg").resize((90,120))
carro_azul = ImageTk.PhotoImage(img_azul)
carro_vermelho = ImageTk.PhotoImage(img_vermelho)

# Armazenar referências globais para evitar garbage collection
imagens_carro = {"azul": carro_azul, "vermelho": carro_vermelho}

# --- CLASSE CARRO ---
class Carro:
    def __init__(self, canvas):
        self.canvas = canvas
        self.imagem_azul = imagens_carro["azul"]
        self.imagem_vermelho = imagens_carro["vermelho"]
        self.imagem_atual = self.imagem_azul
        self.reset_carro()

    def reset_carro(self):
        self.placa = gerar_placa()
        self.velocidade = random.randint(40, 120)
        self.x = random.randint(50, largura_tela-50)
        self.y = -30
        self.passou_radar = False
        self.imagem_atual = self.imagem_azul

        # Cria a imagem do carro
        if hasattr(self, 'carro_id'):
            self.canvas.itemconfig(self.carro_id, image=self.imagem_atual)
            self.canvas.coords(self.carro_id, self.x, self.y)
        else:
            self.carro_id = self.canvas.create_image(self.x, self.y, image=self.imagem_atual, anchor="center")

        # Placa e velocidade
        if hasattr(self, 'placa_fundo'):
            # self.canvas.coords(self.placa_fundo, self.x-20, self.y-30, self.x+20, self.y-15)
            self.canvas.coords(self.texto, self.x, self.y-22)
            self.canvas.coords(self.vel_texto, self.x, self.y-35)
            self.canvas.itemconfig(self.texto, text=self.placa)
            self.canvas.itemconfig(self.vel_texto, text=f"{self.velocidade} km/h")
        else:
            self.placa_fundo = self.canvas.create_rectangle(self.x-20, self.y-30, self.x+20, self.y-15, fill="white")
            self.texto = self.canvas.create_text(self.x, self.y-22, text=self.placa, fill="black", font=("Arial", 10))
            self.vel_texto = self.canvas.create_text(self.x, self.y-35, text=f"{self.velocidade} km/h", fill="white", font=("Arial", 14))

    def mover(self):
        y_ant = self.y
        self.y += self.velocidade / 10  # movimento vertical

        if self.y > altura_tela + 30:
            self.reset_carro()

        # Atualiza posição da imagem
        self.canvas.coords(self.carro_id, self.x, self.y)
        # Atualiza placa e velocidade
        self.canvas.coords(self.placa_fundo, self.x-20, self.y-30, self.x+20, self.y-15)
        self.canvas.coords(self.texto, self.x, self.y-22)
        self.canvas.coords(self.vel_texto, self.x, self.y-35)

        # Troca a imagem de acordo com a velocidade
        if self.velocidade > limite_velocidade:
            self.imagem_atual = self.imagem_vermelho
        else:
            self.imagem_atual = self.imagem_azul
        self.canvas.itemconfig(self.carro_id, image=self.imagem_atual)

        # Verificação do radar
        if radar_ligado and not self.passou_radar:
            if y_ant < linha_radar_y <= self.y:
                if self.velocidade > limite_velocidade:
                    registrar_veiculo(self.placa, self.velocidade)
                self.passou_radar = True

# --- SIMULAÇÃO ---
def atualizar():
    canvas.delete("linha_radar")
    canvas.create_line(0, linha_radar_y, largura_tela, linha_radar_y, fill="green", width=2, tags="linha_radar")
    for carro in carros:
        carro.mover()
    root.after(30, atualizar)

# Criar carros
carros = [Carro(canvas) for _ in range(5)]

# Iniciar simulação
atualizar()
root.mainloop()

# Fechar conexão com o banco
conn.close()
