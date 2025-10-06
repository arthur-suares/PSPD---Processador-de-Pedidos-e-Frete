import grpc
from concurrent import futures
from proto import service_pb2, service_pb2_grpc
import psycopg2


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="pspd-db",
    user="pspd-user",
    password="pspd123"
)


class ServiceAServicer(service_pb2_grpc.ServiceAServicer):

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="pspd-db",
            user="pspd-user",
            password="pspd123"
        )

    def ListarProdutos(self, request, context):
        cur = self.conn.cursor()
        cur.execute("SELECT id, nome, descricao, preco FROM produto")
        produtos = []
        for id, nome, descricao, preco in cur.fetchall():
            produtos.append(service_pb2.ProdutoResponse(
                id=str(id),
                nome=nome,
                descricao=descricao or "",
                preco=preco
            ))
        return service_pb2.ListaProdutosResponse(produtos=produtos)
    

    def ObterProduto(self, request, context):
        cur = self.conn.cursor()
        cur.execute("SELECT id, nome, descricao, preco FROM produto WHERE id = %s", (request.id,))
        row = cur.fetchone()
        if not row:
            context.set_details("Produto não encontrado")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return service_pb2.ProdutoResponse()
        id, nome, descricao, preco = row
        return service_pb2.ProdutoResponse(
            id=str(id),
            nome=nome,
            descricao=descricao or "",
            preco=preco
        )

    def DoSomething(self, request, context):
        input_value = request.input
        output_message = f"gRPC Server (A) processou a requisição. Valor recebido de input: {input_value}"
        return service_pb2.Response(output=output_message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ServiceAServicer_to_server(ServiceAServicer(), server)
    server.add_insecure_port("0.0.0.0:50051")
    print("[Server A - Python] Iniciado com sucesso na porta 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
