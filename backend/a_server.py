import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc


class ServiceAServicer(service_pb2_grpc.ServiceAServicer):
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
