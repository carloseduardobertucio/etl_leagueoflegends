import csv
import random

# Dados fictícios de jogadores e partidas
dados_jogadores = [
    {"id": 1, "nome": "João", "elo": "Prata", "campeao_mais_jogado": "Yasuo", "partidas_jogadas": 100, "vitorias": 60, "derrotas": 40},
    {"id": 2, "nome": "Maria", "elo": "Ouro", "campeao_mais_jogado": "Ahri", "partidas_jogadas": 120, "vitorias": 80, "derrotas": 40},
    {"id": 3, "nome": "Pedro", "elo": "Diamante", "campeao_mais_jogado": "Lee Sin", "partidas_jogadas": 150, "vitorias": 110, "derrotas": 40},
    {"id": 4, "nome": "Ana", "elo": "Platina", "campeao_mais_jogado": "Jinx", "partidas_jogadas": 80, "vitorias": 50, "derrotas": 30},
    {"id": 5, "nome": "Carlos", "elo": "Ferro", "campeao_mais_jogado": "Teemo", "partidas_jogadas": 60, "vitorias": 25, "derrotas": 35}
]

# Gerar dados adicionais aleatórios para mais jogadores
for i in range(6, 301):
    jogador = {
        "id": i,
        "nome": f"Jogador_{i}",
        "elo": random.choice(["Bronze", "Prata", "Ouro", "Platina", "Diamante"]),
        "campeao_mais_jogado": random.choice(["Jhin", "Lux", "Riven", "Zed", "Vayne"]),
        "partidas_jogadas": random.randint(50, 200),
        "vitorias": random.randint(20, 150),
    }
    jogador["derrotas"] = jogador["partidas_jogadas"] - jogador["vitorias"]
    dados_jogadores.append(jogador)

# Escrever dados para um arquivo CSV
nome_arquivo = 'dados_league_of_legends.csv'
with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    campos = ["id", "nome", "elo", "campeao_mais_jogado", "partidas_jogadas", "vitorias", "derrotas"]
    escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)
    
    escritor_csv.writeheader()
    for jogador in dados_jogadores:
        escritor_csv.writerow(jogador)

print(f"Dados gerados e salvos em '{nome_arquivo}'")
