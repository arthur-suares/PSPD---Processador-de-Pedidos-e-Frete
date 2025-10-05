# Makefile para gerenciar o projeto
# Uso: make <comando>

# Cores para output
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m # No Color
VENV=backend/venv

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instala TODAS as dependências (Python + Node.js)
	@echo "$(YELLOW)📦 Instalando dependências...$(NC)"
	@echo "$(BLUE)→ Instalando dependências Python...$(NC)"
	# Cria virtualenv em backend/venv se não existir e instala dependências dentro dele
	@if [ ! -d $(VENV) ]; then \
		python3 -m venv $(VENV); \
		echo "$(BLUE)→ Virtualenv criado em $(VENV)$(NC)"; \
	fi
	@echo "$(BLUE)→ Atualizando pip/setuptools/wheel no venv...$(NC)"
	@$(VENV)/bin/pip install --upgrade pip setuptools wheel >/dev/null 2>&1 || true
	@cd backend && ../$(VENV)/bin/pip install -q -r requirements.txt 2>&1 | grep -v "WARNING: Running pip as the 'root'" || true
	@echo "$(BLUE)→ Instalando dependências Node.js...$(NC)"
	cd backend && npm install --silent
	@echo "$(GREEN)✅ Todas as dependências instaladas!$(NC)"

setup: install ## Setup completo (instala dependências + gera proto)
	@echo "$(YELLOW)🔧 Gerando arquivos proto Python...$(NC)"
	cd backend && ../$(VENV)/bin/python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/service.proto 2>&1 | grep -v "DeprecationWarning" || true
	@echo "$(GREEN)✅ Setup concluído!$(NC)"

start-a: ## Inicia server Python A
	@echo "$(YELLOW)🚀 Iniciando server Python A...$(NC)"
	@echo "$(BLUE)→ Iniciando Server A (porta 50051)...$(NC)"
	@cd backend && ../$(VENV)/bin/python a_server.py &
	@echo "$(GREEN)✅ Server A iniciado!$(NC)"

start-b: ## Inicia server Python B
	@echo "$(YELLOW)🚀 Iniciando server Python B...$(NC)"
	@echo "$(BLUE)→ Iniciando Server B (porta 50052)...$(NC)"
	@cd backend && ../$(VENV)/bin/python b_server.py &
	@echo "$(GREEN)✅ Server B iniciado!$(NC)"

start-p: ## Inicia server Node.js P
	@echo "$(YELLOW)🚀 Iniciando server Node.js P...$(NC)"
	@echo "$(BLUE)→ Iniciando Server P (porta 3000)...$(NC)"
	@cd backend && npm start &
	@echo "$(GREEN)✅ Server P iniciado!$(NC)"

start-all: ## Inicia todos os serviços (A, B e P)
	@chmod +x start_all.sh
	@./start_all.sh

stop: ## Para todos os serviços
	@echo "$(YELLOW)🛑 Parando serviços...$(NC)"
	-@pkill -9 -f "a_server.py" 2>/dev/null
	-@pkill -9 -f "b_server.py" 2>/dev/null
	-@pkill -9 -f "p-server.js" 2>/dev/null
	@sleep 0.5
	@echo "$(GREEN)✅ Serviços parados!$(NC)"

status: ## Verifica status dos serviços
	@echo "$(BLUE)Status dos serviços:$(NC)"
	@echo ""
	@if ss -tuln | grep -q ':50051 '; then \
		echo "$(GREEN)✓$(NC) Server A (Python) - RODANDO (porta 50051)"; \
	else \
		echo "$(YELLOW)✗$(NC) Server A (Python) - PARADO"; \
	fi
	@if ss -tuln | grep -q ':50052 '; then \
		echo "$(GREEN)✓$(NC) Server B (Python) - RODANDO (porta 50052)"; \
	else \
		echo "$(YELLOW)✗$(NC) Server B (Python) - PARADO"; \
	fi
	@if ss -tuln | grep -q ':3000 '; then \
		echo "$(GREEN)✓$(NC) Server P (Node.js) - RODANDO (porta 3000)"; \
	else \
		echo "$(YELLOW)✗$(NC) Server P (Node.js) - PARADO"; \
	fi
	@echo ""
