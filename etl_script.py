import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# Configurações do banco de dados
db_url = 'sqlite:///dados_league_of_legends.db'
table_name = 'jogadores_lol'

# Função para gerar nomes aleatórios usando Faker
def generate_random_names(num_names):
    fake = Faker()
    names = [fake.name() for _ in range(num_names)]
    return names

# Carregar dados do arquivo CSV
def extract_data(file_path):
    return pd.read_csv(file_path)

# Transformar dados conforme necessário
def transform_data(data):
    # Remover dados duplicados, se houver
    data = data.drop_duplicates()

    # Gerar nomes aleatórios para jogadores com nomes numéricos
    numeric_names_mask = data['nome'].str.isdigit()
    num_numeric_names = numeric_names_mask.sum()

    if num_numeric_names > 0:
        random_names = generate_random_names(num_numeric_names)
        data.loc[numeric_names_mask, 'nome'] = random_names

    # Preencher valores ausentes com a média das partidas jogadas
    data['partidas_jogadas'] = data['partidas_jogadas'].fillna(data['partidas_jogadas'].mean())

    # Converter coluna 'elo' para maiúsculas
    data['elo'] = data['elo'].str.upper()

    # Criar uma nova coluna 'taxa_vitoria' baseada em vitorias / partidas_jogadas
    data['taxa_vitoria'] = data['vitorias'] / data['partidas_jogadas']

    return data

# Carregar dados transformados para o banco de dados
def load_data_to_db(data, db_url, table_name):
    engine = create_engine(db_url)
    conn = engine.connect()

    # Criar tabela no banco de dados (se não existir)
    metadata = MetaData()
    players_table = Table(table_name, metadata,
                          Column('id', Integer, primary_key=True),
                          Column('nome', String),
                          Column('elo', String),
                          Column('campeao_mais_jogado', String),
                          Column('partidas_jogadas', Integer),
                          Column('vitorias', Integer),
                          Column('derrotas', Integer),
                          Column('taxa_vitoria', Integer)
                          )
    metadata.create_all(engine)

    # Inserir dados no banco de dados
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)

    print(f"Dados carregados para o banco de dados '{table_name}'")

if __name__ == "__main__":
    # Caminho para o arquivo CSV
    file_path = 'data/dados_league_of_legends.csv'

    # Extração dos dados
    data = extract_data(file_path)

    # Transformação dos dados
    transformed_data = transform_data(data)

    # Carregamento dos dados para o banco de dados
    load_data_to_db(transformed_data, db_url, table_name)
