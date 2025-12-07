from locust import HttpUser, task, between
import random

# IDs de produtos para simular a consulta de detalhes (Substitua por IDs reais)
PRODUCT_IDS = [
    "4a56924e-b765-4a7a-b9e4-6107f0833502", 
    "ID_DE_UM_SEGUNDO_PRODUTO", 
]


# Dados de frete para simular diferentes requisições POST
FRETE_DATA = [
    {"cep_destino": "12345000", "produto_id": PRODUCT_IDS[0], "quantidade": 1},
    {"cep_destino": "99999000", "produto_id": PRODUCT_IDS[1], "quantidade": 2},
    {"cep_destino": "54321000", "produto_id": PRODUCT_IDS[2], "quantidade": 1},
    {"cep_destino": "88888000", "produto_id": PRODUCT_IDS[3], "quantidade": 3},
]


class MicroserviceUser(HttpUser):
    """
    Define o comportamento de um usuário que interage com o API Gateway (Serviço P).
    O wait_time define o tempo de espera (em segundos) entre cada tarefa.
    """

    wait_time = between(1, 2)

    @task(3)  # Peso 3: Acessa a listagem de produtos com mais frequência
    def list_produtos(self):
        """Simula a listagem de todos os produtos (Gateway -> A)."""
        self.client.get("/produtos", name="/produtos [LISTAGEM]")

    @task(2)  # Peso 2: Acessa o detalhe do produto (Gateway -> A -> B)
    def get_produto_detail(self):
        """Simula a obtenção de detalhes (Teste da latência combinada A+B)."""
        if not PRODUCT_IDS:
            return

        product_id = random.choice(PRODUCT_IDS)
        self.client.get(f"/produto/{product_id}", name="/produto/[id] [DETALHE A+B]")

    @task(1)  # Peso 1: Simula o cálculo de frete (Gateway -> B)
    def calculate_frete(self):
        """Simula a chamada POST para cálculo de frete (Teste da latência B)."""
        data = random.choice(FRETE_DATA)
        self.client.post("/frete", json=data, name="/frete [CÁLCULO B]")
