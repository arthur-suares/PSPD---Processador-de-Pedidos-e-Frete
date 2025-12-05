import grpc
from concurrent import futures
from proto import service_pb2, service_pb2_grpc
import psycopg2
import os
from prometheus_client import start_http_server, Counter, Summary, Histogram

# --- Definição das Métricas ---
SERVICE_NAME = 'service_b'
REQUEST_COUNT = Counter(f'{SERVICE_NAME}_requests_total', 'Contagem total de requisições gRPC', ['method', 'status_code'])
REQUEST_LATENCY = Histogram(f'{SERVICE_NAME}_request_latency_seconds', 'Latência de requisições gRPC em segundos', ['method'])

# --- Wrapper para instrumentação ---
def instrumented(method_handler):
    """Decorator para instrumentar métodos gRPC com métricas de tempo e contagem."""
    method_name = method_handler.__name__

    def wrapper(self, request, context):
        status = 'UNKNOWN'
        
        with REQUEST_LATENCY.labels(method=method_name).time():
            try:
                response = method_handler(self, request, context)
                status = 'OK'
                return response
            
            except Exception as e:
                code = context.code() if context.code() else grpc.StatusCode.INTERNAL
                
                status_code_name = code.name
                
                REQUEST_COUNT.labels(method=method_name, status_code=status_code_name).inc()
                
                raise e
            
            finally:
                if status == 'OK':
                    REQUEST_COUNT.labels(method=method_name, status_code='OK').inc()
    
    return wrapper

class ServiceBServicer(service_pb2_grpc.ServiceBServicer):
    def __init__(self):
        pass 
    
    def _get_db_connection(self):
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            database=os.getenv('DB_NAME', 'pspd-db'),
            user=os.getenv('DB_USER', 'pspd-user'),
            password=os.getenv('DB_PASSWORD', 'pspd123')
        )
        conn.autocommit = True
        return conn

    @instrumented
    def ObterEstoque(self, request, context):
        conn = None
        cur = None
        try:
            # ABRIMOS A CONEXÃO DENTRO DO MÉTODO
            conn = self._get_db_connection()
            cur = conn.cursor()
            
            # Consulta SQL: Aspas duplas para forçar o case-sensitivity (produtoId)
            cur.execute('SELECT "produtoId", quantidade, localizacao FROM estoque WHERE "produtoId" = %s', (request.produto_id,))
            row = cur.fetchone()
            
            if not row:
                context.set_details("Estoque não encontrado")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                raise Exception("Estoque não encontrado") 
            
            produto_id, quantidade, localizacao = row
            return service_pb2.EstoqueResponse(
                produto_id=str(produto_id),
                quantidade=quantidade,
                localizacao=localizacao or ""
            )
        
        except psycopg2.Error as e:
            # Se houver erro, tenta fechar e re-lançar
            if conn: conn.rollback()
            context.set_details(f"Erro de DB: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            raise Exception(e) 
            
        finally:
            # FECHAMOS O CURSOR E A CONEXÃO
            if cur: cur.close()
            if conn: conn.close()

    @instrumented
    def CalcularFrete(self, request, context):
        cep_destino = request.cep_destino
        if cep_destino.startswith("123"):
            valor_frete = 45.50
            prazo_entrega = "5 dias úteis"
        else:
            valor_frete = 22.90
            prazo_entrega = "10 dias úteis"
            
        return service_pb2.FreteResponse(
            valor_frete=valor_frete,
            prazo_entrega=prazo_entrega
        )
    
    @instrumented
    def Calculate(self, request, context):
        input_value = request.input
        output_message = f"gRPC Server (B) processou a requisição. Valor recebido de input: {input_value}"
        return service_pb2.Response(output=output_message)


def serve():
    start_http_server(8000)
    print(f"Servidor de Métricas do Prometheus ({SERVICE_NAME}) iniciado na porta 8000")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ServiceBServicer_to_server(ServiceBServicer(), server)
    server.add_insecure_port("0.0.0.0:50052")
    print("[Server B - Python] Iniciado com sucesso na porta 50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()