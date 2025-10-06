import grpc
from concurrent import futures
from proto import service_pb2, service_pb2_grpc
import psycopg2


class ServiceBServicer(service_pb2_grpc.ServiceBServicer):
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="pspd-db",
            user="pspd-user",
            password="pspd123"
        )
        
    def Calculate(self, request, context):
        input_value = request.input
        output_message = f"gRPC Server (B) processou a requisição. Valor recebido de input: {input_value}"
        return service_pb2.Response(output=output_message)


    def ObterEstoque(self, request, context):
        cur = self.conn.cursor()
        cur.execute("SELECT produto_id, quantidade, localizacao FROM estoque WHERE produto_id = %s", (request.produto_id,))
        row = cur.fetchone()
        if not row:
            context.set_details("Estoque não encontrado")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return service_pb2.EstoqueResponse()
        produto_id, quantidade, localizacao = row
        return service_pb2.EstoqueResponse(
            produto_id=str(produto_id),
            quantidade=quantidade,
            localizacao=localizacao or ""
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ServiceBServicer_to_server(ServiceBServicer(), server)
    server.add_insecure_port("0.0.0.0:50052")
    print("[Server B - Python] Iniciado com sucesso na porta 50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
