import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc


class ServiceBServicer(service_pb2_grpc.ServiceBServicer):
    def Calculate(self, request, context):
        input_value = request.input
        output_message = f"gRPC Server (B) processou a requisição. Valor recebido de input: {input_value}"
        return service_pb2.Response(output=output_message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ServiceBServicer_to_server(ServiceBServicer(), server)
    server.add_insecure_port("0.0.0.0:50052")
    print("[Server B - Python] Iniciado com sucesso na porta 50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
