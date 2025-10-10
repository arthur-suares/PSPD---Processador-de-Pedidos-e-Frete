# Processador de Pedidos e Frete

Primeiro laboratório da disciplina **Programação para Sistemas Paralelos e Distribuídos (PSPD)** sobre **gRPC**.

---

## Passos para rodar o projeto

### Frontend
O frontend está disponível na porta `5173`.  
Para rodar, acesse a pasta `frontend` e execute:

```bash
npm install
npm run dev
```

---

### Backend
Antes de iniciar o backend, é necessário criar arquivos `.env` tanto na **raiz do projeto** quanto dentro da **pasta backend**, contendo o seguinte conteúdo:

```bash
# Configurações do banco de dados
DB_PORT = 5432
DB_NAME = pspd-db
DB_USER = pspd-user
DB_PASSWORD = pspd123

# URL de conexão com o banco de dados
DATABASE_URL = postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}
```

Depois, acesse a pasta `backend` e rode os comandos:

```bash
docker compose up --build
```

Em seguida, ainda dentro da pasta `backend`, rode:

```bash
npx prisma generate dev
npx prisma migrate dev
```

O servidor backend estará disponível para testes na **porta 4000**.

---

### Scripts úteis

```bash
# Setup completo (instala dependências e gera proto)
make setup

# Iniciar todos os servidores (A, B e P)
make start-all

# Parar todos os servidores
make stop

# Ver todos os comandos disponíveis
make help
```

Para rodar apenas um serviço gRPC específico:

```bash
make start-a   # Server A
make start-b   # Server B
make start-p   # Server P
```

---

### Testando as requisições

Use o Postman ou outro cliente HTTP para testar as rotas:

- `POST http://localhost:4000/api/calculate`
- `POST http://localhost:4000/api/do-something`

Com o seguinte corpo JSON:

```json
{
  "input": "teste"
}
```

Respostas esperadas:

`POST /api/do-something`
```json
{
  "output": "gRPC Server (B) processou a requisição. Valor recebido de input: teste"
}
```

`POST /api/calculate`
```json
{
  "output": "gRPC Server (A) processou a requisição. Valor recebido de input: teste"
}
```

---

**Banco de dados:** PostgreSQL com gerenciamento via **Prisma ORM**.

## Vídeo da apresentação 
[![Grafos2](https://img.youtube.com/vi/dBiLgd35qYI/0.jpg)](https://www.youtube.com/watch?v=dBiLgd35qYI)

