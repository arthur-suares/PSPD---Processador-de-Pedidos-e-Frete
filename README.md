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
⋊> ~/P/frontend on main ⨯ npm i
⋊> ~/P/frontend on main ⨯ npm run start:all
```

Para rodar apenas um serviço gRPC específico, basta usar algum dos scripts abaixo:

```bash
⋊> ~/P/frontend on main ⨯ npm run start:a
## ou
⋊> ~/P/frontend on main ⨯ npm run start:b
## ou
⋊> ~/P/frontend on main ⨯ npm run start:p
```

