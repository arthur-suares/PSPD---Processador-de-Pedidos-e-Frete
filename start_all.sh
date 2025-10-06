#!/bin/bash
# Script para iniciar todos os servidores em background

# Para servidores existentes
pkill -f "python.*a_server.py" 2>/dev/null || true
pkill -f "python.*b_server.py" 2>/dev/null || true
pkill -f "node.*p-server.js" 2>/dev/null || true

# Inicia Server A
echo "Iniciando Server A (Python gRPC - porta 50051)..."
cd backend
../backend/venv/bin/python a_server.py > /dev/null 2>&1 &
cd ..
sleep 0.5

# Inicia Server B
echo "Iniciando Server B (Python gRPC - porta 50052)..."
cd backend
../backend/venv/bin/python b_server.py > /dev/null 2>&1 &
cd ..
sleep 0.5

# Inicia Server P
echo "Iniciando Server P (Node.js REST - porta 3000)..."
cd backend
npm start > /dev/null 2>&1 &
cd ..
sleep 0.5

echo ""
echo "✅ Todos os serviços iniciados!"
echo ""
echo "Serviços rodando:"
echo "  • Server A (Python gRPC): localhost:50051"
echo "  • Server B (Python gRPC): localhost:50052"
echo "  • Server P (Node.js REST): http://localhost:3000"
echo ""
echo "Para verificar status: make status"
echo "Para parar: make stop"
