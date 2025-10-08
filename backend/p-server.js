import express from "express";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const PROTO_PATH = "./proto/service.proto";

const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef).services;

const grpcAHost = process.env.GRPC_A_HOST || "backend:5000";
const grpcBHost = process.env.GRPC_B_HOST || "backend:5001";

const produtoClient = new grpcObject.ServiceA(
  grpcAHost,
  grpc.credentials.createInsecure()
);
const estoqueClient = new grpcObject.ServiceB(
  grpcBHost,
  grpc.credentials.createInsecure()
);

const app = express();
const PORT = 4000;
app.use(express.json());

app.get("/produtos", (req, res) => {
  produtoClient.ListarProdutos({}, (err, response) => {
    if (err) return res.status(500).json({ error: err.details });
    res.json(response.produtos);
  });
});

app.get("/produto/:id", (req, res) => {
  const id = req.params.id;
  produtoClient.ObterProduto({ id }, (err, produto) => {
    if (err) return res.status(404).json({ error: err.details });
    estoqueClient.ObterEstoque({ produto_id: id }, (err2, estoque) => {
      if (err2) return res.json({ ...produto, estoque: null });
      res.json({ ...produto, estoque });
    });
  });
});

app.post("/criarProduto", (req, res) => {
  const { nome, descricao, preco } = req.body;

  produtoClient.CriarProduto({ nome, descricao, preco }, (err, response) => {
    if (err) return res.status(500).json({ error: err.details });
    res.json({
      message: "Produto criado com sucesso!",
      produto: response
    });
  });
});

app.put("/produto/:id", (req, res) => {
  const { id } = req.params;
  const { nome, descricao, preco } = req.body;

  produtoClient.EditarProduto({ id, nome, descricao, preco }, (err, response) => {
    if (err) return res.status(500).json({ error: err.details });
    res.json({
      message: "Produto atualizado com sucesso!",
      produto: response
    });
  });
});

app.delete("/produto/:id", (req, res) => {
  const { id } = req.params;

  produtoClient.DeletarProduto({ id }, (err, response) => {
    if (err) return res.status(500).json({ error: err.details });
    res.json(response);
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Stub rodando em http://localhost:${PORT}`);
});
