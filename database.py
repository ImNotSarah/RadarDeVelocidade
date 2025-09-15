import sqlite3
from datetime import datetime
from config import limite_velocidade

# Conexão com o banco
conn = sqlite3.connect("bd/radar.db")
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

def fechar_conexao():
    conn.close()
