import random
from tkinter import Canvas
from PIL import Image, ImageTk
from config import limite_velocidade, altura_tela, largura_tela, linha_radar_y, radar_ligado
from database import registrar_veiculo

# --- FUNÇÃO AUXILIAR ---
def gerar_placa():
    letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numeros = ''.join(random.choices('0123456789', k=4))
    return f"{letras}-{numeros}"

# --- CLASSE CARRO ---
class Carro:
    def __init__(self, canvas: Canvas, imagens_carro: dict):
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

        if hasattr(self, 'carro_id'):
            self.canvas.itemconfig(self.carro_id, image=self.imagem_atual)
            self.canvas.coords(self.carro_id, self.x, self.y)
        else:
            self.carro_id = self.canvas.create_image(self.x, self.y, image=self.imagem_atual, anchor="center")

        if hasattr(self, 'placa_fundo'):
            self.canvas.coords(self.texto, self.x, self.y-22)
            self.canvas.coords(self.vel_texto, self.x, self.y-35)
            self.canvas.itemconfig(self.texto, text=self.placa)
            self.canvas.itemconfig(self.vel_texto, text=f"{self.velocidade} km/h")
        else:
            self.placa_fundo = self.canvas.create_rectangle(self.x-20, self.y-30, self.x+20, self.y-15, fill="white")
            self.texto = self.canvas.create_text(self.x, self.y-22, text=self.placa, fill="black", font=("Arial", 10))
            self.vel_texto = self.canvas.create_text(self.x, self.y-35, text=f"{self.velocidade} km/h", fill="white", font=("Arial", 14))

    def mover(self):
        global radar_ligado
        y_ant = self.y
        self.y += self.velocidade / 10

        if self.y > altura_tela + 30:
            self.reset_carro()

        self.canvas.coords(self.carro_id, self.x, self.y)
        self.canvas.coords(self.placa_fundo, self.x-20, self.y-30, self.x+20, self.y-15)
        self.canvas.coords(self.texto, self.x, self.y-22)
        self.canvas.coords(self.vel_texto, self.x, self.y-35)

        self.imagem_atual = self.imagem_vermelho if self.velocidade > limite_velocidade else self.imagem_azul
        self.canvas.itemconfig(self.carro_id, image=self.imagem_atual)

        if radar_ligado and not self.passou_radar:
            if y_ant < linha_radar_y <= self.y:
                if self.velocidade > limite_velocidade:
                    registrar_veiculo(self.placa, self.velocidade)
                self.passou_radar = True
