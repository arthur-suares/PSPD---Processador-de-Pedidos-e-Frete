import express from "express";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const PROTO_PATH = "./proto/service.proto";

const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef).services;

const produtoClient = new grpcObject.ServiceA(
  "localhost:50051",
  grpc.credentials.createInsecure()
);
const estoqueClient = new grpcObject.ServiceB(
  "localhost:50052",
  grpc.credentials.createInsecure()
);

const app = express();
const PORT = 3000;

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

app.listen(PORT, () => {
  console.log(`🚀 Stub rodando em http://localhost:${PORT}`);
});
