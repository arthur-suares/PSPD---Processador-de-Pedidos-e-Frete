import psycopg2
import os
import uuid

# Configuração de conexão
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 5432)),
    database=os.getenv("DB_NAME", "pspd-db"),
    user=os.getenv("DB_USER", "pspd-user"),
    password=os.getenv("DB_PASSWORD", "pspd123"),
)

cur = conn.cursor()

print("🗑️  Limpando tabelas existentes...")
cur.execute("DROP TABLE IF EXISTS estoque CASCADE;")
cur.execute("DROP TABLE IF EXISTS produto CASCADE;")

print("🔧 Criando tabelas...")
cur.execute(
    """
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE produto (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nome TEXT NOT NULL,
  descricao TEXT,
  preco FLOAT NOT NULL,
  estoque INT DEFAULT 0,
  "criado_em" TIMESTAMP DEFAULT NOW(),
  "atualizado_em" TIMESTAMP DEFAULT NOW()
);

CREATE TABLE estoque (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "produto_id" UUID NOT NULL REFERENCES produto(id) ON DELETE CASCADE,
  quantidade INT NOT NULL,
  localizacao TEXT
);

CREATE INDEX idx_estoque_produto ON estoque("produto_id");
"""
)

print("📦 Inserindo produtos de exemplo...")

# Produtos com preços e descrições realistas
produtos = [
    ("iPhone 13", "iPhone 13 256GB - Azul Meia-Noite", 3500.00),
    ("Notebook Dell Inspiron", "Notebook Dell Inspiron 15 i5 8GB 256GB SSD", 3299.90),
    ("Mouse Logitech MX Master", "Mouse sem fio Logitech MX Master 3S", 549.99),
    ("Teclado Mecânico Keychron", "Teclado Mecânico Keychron K2 RGB Hot-Swap", 799.90),
    ("Xiaomi Mi 14", "Xiaomi Mi 14 512GB - Preto", 4599.00),
    ("Monitor LG UltraWide", "Monitor LG UltraWide 29 IPS Full HD", 1299.00),
    ("Headset HyperX Cloud", "Headset Gamer HyperX Cloud II 7.1", 499.90),
    ("Webcam Logitech C920", "Webcam Full HD 1080p Logitech C920", 389.90),
    ("SSD Samsung 1TB", "SSD Samsung 980 PRO 1TB NVMe M.2", 699.00),
]

produto_ids = []
for nome, descricao, preco in produtos:
    cur.execute(
        "INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s) RETURNING id",
        (nome, descricao, preco),
    )
    produto_id = cur.fetchone()[0]
    produto_ids.append(produto_id)
    print(f"  ✅ {nome} - R$ {preco:.2f}")

print(f"\n📊 Total de produtos inseridos: {len(produto_ids)}")

print("\n🏭 Inserindo estoque em múltiplas localizações...")

# Estoques distribuídos em diferentes centros de distribuição
localizacoes = [
    "CD São Paulo - SP",
    "CD Rio de Janeiro - RJ",
    "CD Belo Horizonte - MG",
    "CD Curitiba - PR",
    "CD Porto Alegre - RS",
]

estoques_data = [
    # iPhone 13 - Alto estoque (produto popular)
    (produto_ids[0], 150, localizacoes[0]),
    (produto_ids[0], 120, localizacoes[1]),
    (produto_ids[0], 80, localizacoes[2]),
    # Notebook Dell - Médio estoque
    (produto_ids[1], 45, localizacoes[0]),
    (produto_ids[1], 35, localizacoes[1]),
    (produto_ids[1], 25, localizacoes[3]),
    # Mouse Logitech - Alto estoque (acessório)
    (produto_ids[2], 200, localizacoes[0]),
    (produto_ids[2], 150, localizacoes[1]),
    (produto_ids[2], 100, localizacoes[2]),
    (produto_ids[2], 80, localizacoes[4]),
    # Teclado Keychron - Médio estoque
    (produto_ids[3], 60, localizacoes[0]),
    (produto_ids[3], 40, localizacoes[1]),
    (produto_ids[3], 30, localizacoes[3]),
    # Xiaomi Mi 14 - Baixo estoque (novo lançamento)
    (produto_ids[4], 25, localizacoes[0]),
    (produto_ids[4], 15, localizacoes[1]),
    # Monitor LG - Médio estoque
    (produto_ids[5], 50, localizacoes[0]),
    (produto_ids[5], 40, localizacoes[2]),
    (produto_ids[5], 30, localizacoes[3]),
    # Headset HyperX - Alto estoque
    (produto_ids[6], 100, localizacoes[0]),
    (produto_ids[6], 80, localizacoes[1]),
    (produto_ids[6], 60, localizacoes[4]),
    # Webcam Logitech - Médio estoque
    (produto_ids[7], 70, localizacoes[0]),
    (produto_ids[7], 50, localizacoes[1]),
    # SSD Samsung - Alto estoque
    (produto_ids[8], 120, localizacoes[0]),
    (produto_ids[8], 100, localizacoes[1]),
    (produto_ids[8], 80, localizacoes[2]),
]

total_estoque = 0
for produto_id, quantidade, localizacao in estoques_data:
    cur.execute(
        'INSERT INTO estoque ("produto_id", quantidade, localizacao) VALUES (%s, %s, %s)',
        (produto_id, quantidade, localizacao),
    )
    total_estoque += quantidade

print(f"  ✅ {len(estoques_data)} registros de estoque inseridos")
print(f"  📊 Total de unidades em estoque: {total_estoque}")

conn.commit()

# Exibir resumo
print("\n" + "=" * 60)
print("📋 RESUMO DO BANCO DE DADOS")
print("=" * 60)

cur.execute(
    """
    SELECT 
        p.nome, 
        p.preco,
        COALESCE(SUM(e.quantidade), 0) as total_estoque,
        COUNT(e.id) as num_locais
    FROM produto p
    LEFT JOIN estoque e ON p.id = e."produto_id"
    GROUP BY p.id, p.nome, p.preco
    ORDER BY p.nome
"""
)

print(f"\n{'Produto':<30} {'Preço':<12} {'Estoque':<10} {'Locais':<8}")
print("-" * 60)
for row in cur.fetchall():
    nome, preco, estoque, locais = row
    print(f"{nome:<30} R$ {preco:>8.2f}  {estoque:>6} un   {locais:>3} CDs")

print("\n" + "=" * 60)
print("✅ Banco de dados populado com sucesso!")
print("=" * 60)

cur.close()
conn.close()
