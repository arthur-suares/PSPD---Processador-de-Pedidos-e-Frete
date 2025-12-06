import express from "express";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";
import cors from "cors";
import client from "prom-client";

const PROTO_PATH = "./proto/service.proto";

const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef).services;

// Variáveis de ambiente
const grpcAHost = process.env.GRPC_A_HOST || "backend:5000";
const grpcBHost = process.env.GRPC_B_HOST || "backend:50052";

// Inicialização dos clientes gRPC
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

app.use(cors());
app.use(express.json());

// ===================================
// CONFIGURAÇÃO DO PROMETHEUS
// ===================================

const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics({ prefix: 'node_app_', timeout: 10000 });

const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total de requisições HTTP para o API Gateway (P)',
  labelNames: ['method', 'route', 'status_code'],
});

const httpRequestDurationMicroseconds = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Latência das requisições HTTP em segundos',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5], 
});

app.use((req, res, next) => {
  const end = httpRequestDurationMicroseconds.startTimer();
  
  res.on('finish', () => {
    const route = req.route ? req.route.path : 'unknown_route';
    const status_code = res.statusCode;

    httpRequestsTotal.labels(req.method, route, status_code).inc();
    
    end({ method: req.method, route: route, status_code: status_code });
  });

  next();
});

// ===================================
// ROTAS DE SERVIÇO
// ===================================

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

app.post("/frete", (req, res) => {
  const { cep_destino, produto_id, quantidade } = req.body;
  
  if (!cep_destino || !produto_id) {
    return res.status(400).json({ error: "CEP de destino e ID do produto são obrigatórios." });
  }

  estoqueClient.CalcularFrete({ cep_destino, produto_id, quantidade: quantidade || 1 }, (err, response) => {
    if (err) return res.status(500).json({ error: err.details });
    res.json(response);
  });
});


// ===================================
// ROTA DE EXPOSIÇÃO DE MÉTRICAS (PROMETHEUS)
// ===================================

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

// ===================================
// INICIALIZAÇÃO DO SERVIDOR
// ===================================

app.listen(PORT, () => {
  console.log(`🚀 Stub rodando em http://localhost:${PORT}`);
  console.log(`📊 Métricas disponíveis em http://localhost:${PORT}/metrics`);
});