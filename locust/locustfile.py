from locust import HttpUser, task, between
import random
import json

# Colocar os IDs de produtos reais do banco de dados
PRODUCT_IDS = [
    "ID1", 
    "ID2",
    "ID3",
    "ID4",
    "ID5",
]

# Dados de frete para simular diferentes requisições POST
FRETE_DATA = [
    {"cep_destino": "01310100", "produto_id": PRODUCT_IDS[0], "quantidade": 1},
    {"cep_destino": "20040020", "produto_id": PRODUCT_IDS[1], "quantidade": 2},
    {"cep_destino": "30130100", "produto_id": PRODUCT_IDS[2], "quantidade": 1},
    {"cep_destino": "40110160", "produto_id": PRODUCT_IDS[3], "quantidade": 3},
    {"cep_destino": "80010000", "produto_id": PRODUCT_IDS[4], "quantidade": 1},
]

# Dados para criar produtos de teste
PRODUTOS_CRIAR = [
    {
        "nome": "Produto Teste Locust 1",
        "descricao": "Produto criado automaticamente pelo teste de carga",
        "preco": 99.90,
    },
    {
        "nome": "Produto Teste Locust 2",
        "descricao": "Outro produto de teste",
        "preco": 199.90,
    },
]


class MicroserviceUser(HttpUser):
    """
    Define o comportamento de um usuário que interage com o API Gateway (Serviço P).
    O wait_time define o tempo de espera (em segundos) entre cada tarefa.
    """

    wait_time = between(1, 3)

    @task(5)  # Peso 5: Acessa a listagem de produtos com mais frequência
    def list_produtos(self):
        """Simula a listagem de todos os produtos (Gateway -> A)."""
        with self.client.get(
            "/produtos", name="/produtos [LISTAGEM]", catch_response=True
        ) as response:
            try:
                if response.status_code == 200:
                    produtos = response.json()
                    if isinstance(produtos, list) and len(produtos) > 0:
                        response.success()
                    else:
                        response.failure("Lista de produtos vazia")
                else:
                    response.failure(f"Status code: {response.status_code}")
            except Exception as e:
                response.failure(f"Erro ao parsear resposta: {str(e)}")

    @task(3)  # Peso 3: Acessa o detalhe do produto (Gateway -> A -> B)
    def get_produto_detail(self):
        """Simula a obtenção de detalhes com estoque (Teste da latência combinada A+B)."""
        if not PRODUCT_IDS:
            return

        product_id = random.choice(PRODUCT_IDS)
        with self.client.get(
            f"/produto/{product_id}",
            name="/produto/[id] [DETALHE A+B]",
            catch_response=True,
        ) as response:
            try:
                if response.status_code == 200:
                    produto = response.json()
                    # Valida se tem os campos esperados
                    if "id" in produto and "nome" in produto and "preco" in produto:
                        # Valida se o estoque está presente (pode ser null)
                        if "estoque" in produto:
                            response.success()
                        else:
                            response.failure(
                                "Campo 'estoque' não encontrado na resposta"
                            )
                    else:
                        response.failure("Campos obrigatórios faltando na resposta")
                elif response.status_code == 404:
                    response.failure(f"Produto {product_id} não encontrado")
                else:
                    response.failure(f"Status code: {response.status_code}")
            except Exception as e:
                response.failure(f"Erro ao parsear resposta: {str(e)}")

    @task(2)  # Peso 2: Simula o cálculo de frete (Gateway -> B)
    def calculate_frete(self):
        """Simula a chamada POST para cálculo de frete (Teste da latência B)."""
        data = random.choice(FRETE_DATA)
        with self.client.post(
            "/frete", json=data, name="/frete [CÁLCULO B]", catch_response=True
        ) as response:
            try:
                if response.status_code == 200:
                    frete = response.json()
                    if "valor_frete" in frete and "prazo_entrega" in frete:
                        response.success()
                    else:
                        response.failure(
                            f"Campos obrigatórios faltando na resposta de frete. Recebido: {frete}"
                        )
                else:
                    response.failure(f"Status code: {response.status_code}")
            except Exception as e:
                response.failure(f"Erro ao parsear resposta: {str(e)}")

    @task(1)  # Peso 1: Cria um novo produto (Gateway -> A)
    def create_produto(self):
        """Simula a criação de um novo produto (Teste de escrita no Service A)."""
        data = random.choice(PRODUTOS_CRIAR)
        with self.client.post(
            "/criarProduto",
            json=data,
            name="/criarProduto [CREATE A]",
            catch_response=True,
        ) as response:
            try:
                if response.status_code == 200:
                    result = response.json()
                    if "produto" in result and "id" in result["produto"]:
                        response.success()
                    else:
                        response.failure("Produto criado mas resposta inválida")
                else:
                    response.failure(f"Status code: {response.status_code}")
            except Exception as e:
                response.failure(f"Erro ao parsear resposta: {str(e)}")
