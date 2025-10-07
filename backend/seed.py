import psycopg2
import uuid

# Configuração de conexão
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="pspd-db",
    user="pspd-user",
    password="pspd123"
)

cur = conn.cursor()

# Criação das tabelas (caso não existam)
cur.execute("""
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS produto (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nome TEXT NOT NULL,
  descricao TEXT,
  preco FLOAT NOT NULL,
  criado_em TIMESTAMP DEFAULT NOW(),
  atualizado_em TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS estoque (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  produto_id UUID REFERENCES produto(id) ON DELETE CASCADE,
  quantidade INT NOT NULL,
  localizacao TEXT
);
""")

# Dados de exemplo
produtos = [
    ("Camiseta Básica", "Camiseta 100% algodão", 59.90),
    ("Calça Jeans", "Calça jeans azul escuro", 129.90),
    ("Tênis Esportivo", "Tênis leve para corrida", 249.90)
]

# Inserindo produtos e capturando IDs
produto_ids = []
for nome, descricao, preco in produtos:
    cur.execute(
        "INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s) RETURNING id",
        (nome, descricao, preco)
    )
    produto_ids.append(cur.fetchone()[0])

# Inserindo estoques correspondentes
estoques = [
    (produto_ids[0], 50, "Centro de Distribuição - São Paulo"),
    (produto_ids[1], 30, "Centro de Distribuição - Rio de Janeiro"),
    (produto_ids[2], 20, "Centro de Distribuição - Curitiba")
]

for produto_id, quantidade, localizacao in estoques:
    cur.execute(
        "INSERT INTO estoque (produto_id, quantidade, localizacao) VALUES (%s, %s, %s)",
        (produto_id, quantidade, localizacao)
    )

conn.commit()
print("✅ Banco de dados populado com sucesso!")
cur.close()
conn.close()
