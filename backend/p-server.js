import express from "express";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const app = express();
app.use(express.json());

// Carrega proto
const packageDef = protoLoader.loadSync("proto/service.proto");
const grpcObj = grpc.loadPackageDefinition(packageDef).services;

// Cria clientes gRPC para A e B
const clientA = new grpcObj.ServiceA("localhost:50051", grpc.credentials.createInsecure());
const clientB = new grpcObj.ServiceB("localhost:50052", grpc.credentials.createInsecure());

// Exemplo de rota REST chamando ServiceA
app.post("/api/do-something", (req, res) => {
  const { input } = req.body;
  clientA.DoSomething({ input }, (err, response) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(response);
  });
});

// Exemplo de rota REST chamando ServiceB
app.post("/api/calculate", (req, res) => {
  const { input } = req.body;
  clientB.Calculate({ input }, (err, response) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(response);
  });
});

app.listen(3000, () => {
  console.log("Stub/Web server (P) rodando em http://localhost:3000");
});
