# Processador de Pedidos e Frete

Primeiro laboratório de PSPD a respeito de gRPC

## Passos para rodar o projeto

O frontend está disponível na porta `5173`. Para rodar acesse a pasta frontend e faça os seguintes comandos

```bash
⋊> ~/P/frontend on main ⨯ npm i
⋊> ~/P/frontend on main ⨯ npm run dev
```

Quanto ao backend, de dentro da pasta do back rode:

```bash
⋊> ~/P/backend on main ⨯ npm i
⋊> ~/P/backend on main ⨯ npm run start:all
```

Para rodar apenas um serviço gRPC específico, basta usar algum dos scripts abaixo:

```bash
⋊> ~/P/backend on main ⨯ npm run start:a
## ou
⋊> ~/P/backend on main ⨯ npm run start:b
## ou
⋊> ~/P/backend on main ⨯ npm run start:p
```

As requisições que podem ser feitas por postman nas rotas:

- http://localhost:3000/api/calculate
- http://localhost:3000/api/do-something

devem ser do tipo POST e conter um json como o abaixo:

```json
{
    "input": "teste"
}
```

As respostas esperadas são:

POST em `http://localhost:3000/api/do-something`
```json
{
  "output": "gRPC Server (B) processou a requisição. Valor recebido de input: teste"
}
```

Dizendo que o serviço `B` de gRPC processou a requisição

POST em `http://localhost:3000/api/calculate`
```json
{
  "output": "gRPC Server (A) processou a requisição. Valor recebido de input: teste"
}
```
Dizendo que o serviço `A` de gRPC processou a requisição
