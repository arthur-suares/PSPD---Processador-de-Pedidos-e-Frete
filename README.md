# Processador de Pedidos e Frete

Projeto final da disciplina **Programação para Sistemas Paralelos e Distribuídos (PSPD)**.

---

# Passos para rodar o projeto

## 🚀 Frontend
Porta padrão: **5173**

```bash
cd frontend
npm install
npm run dev
````

---

## 🛠 Backend

### 1. Criar arquivos `.env`

Criar **um .env na raiz** e **um .env dentro de `backend/`** contendo:

```env
DB_PORT=5432
DB_NAME=pspd-db
DB_USER=pspd-user
DB_PASSWORD=pspd123

DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}
```

---

## ☸️ Kubernetes (K3D)

### 📌 Pré-requisitos

* Docker + Docker Compose
* Kubectl
* K3d
* Docker Hub logado (`docker login`)
* Acesso Grafana: [http://localhost:8080](http://localhost:8080) (admin/prom_admin)

---

## ▶️ Execução (Passo a Passo)

### 1. Login no Docker Hub

```bash
docker login
```

### 2. Build da imagem do backend

```bash
docker build -t docker.io/pspdtf/pspd-backend:v1.0 ./backend
docker push docker.io/pspdtf/pspd-backend:v1.0
```

### 3. Remover cluster antigo

```bash
k3d cluster delete pspd-cluster
```

### 4. Criar cluster Kubernetes (1 master + 2 workers)

```bash
k3d cluster create pspd-cluster \
  --servers 1 \
  --agents 2 \
  --port 4000:4000@server:0 \
  --port 8089:8089@server:0
```

### 5. Aplicar deployments

```bash
kubectl apply -f k8s/k8s-deploy.yaml
kubectl apply -f k8s/k8s-monitoring.yaml
```

### 6. Verificar status dos pods

```bash
kubectl get pods
kubectl get pods -n monitoring
```

### 7. Encaminhar portas (Grafana + Prometheus)

```bash
kubectl port-forward -n monitoring svc/grafana-service 3001:3000 > /dev/null 2>&1 & \
echo "Grafana: http://localhost:3001 (PID: $!)"

kubectl port-forward -n monitoring svc/prometheus-service 9090:9090 > /dev/null 2>&1 & \
echo "Prometheus: http://localhost:9090 (PID: $!)"
```

### 8. Popular banco

```bash
kubectl exec -i $(kubectl get pod -l app=service-a -o jsonpath='{.items[0].metadata.name}') \
  -c service-a -- python3 seed.py
```

### 9. Obter IDs dos produtos (para configurar o Locust)

```bash
kubectl exec -i $(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}') \
  -- psql -U pspd-user -d pspd-db \
  -c "SELECT id, nome, preco FROM produto ORDER BY nome;"
```

### 10. Build e push do Locust

```bash
docker build -t docker.io/pspdtf/locust-tester:v1.0 -f locust/Dockerfile.locust ./locust
docker push docker.io/pspdtf/locust-tester:v1.0
```

### 11. Validar Prometheus

Acesse:

```
http://localhost:9090/targets
```

### 12. Configurar Prometheus no Grafana

No Grafana:
**Configuration → Data Sources → Add Data Source → Prometheus**

Configuração:

* **Name:** Prometheus
* **URL:** `http://prometheus-service.monitoring:9090`
* Salvar com **Save & Test**

---


## Vídeo da apresentação 
[![Grafos2](https://img.youtube.com/vi/HUdvEvxAvGI/0.jpg)](https://www.youtube.com/watch?v=HUdvEvxAvGI)

