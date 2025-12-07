import grpc
from concurrent import futures
from proto import service_pb2, service_pb2_grpc
import psycopg2
import os
from prometheus_client import start_http_server, Counter, Summary, Histogram

# --- Definição das Métricas ---
SERVICE_NAME = "service_a"

# Contador de requisições gRPC totais (por método e status)
REQUEST_COUNT = Counter(
    f"{SERVICE_NAME}_requests_total",
    "Contagem total de requisições gRPC",
    ["method", "status_code"],
)

# Histograma para medir a latência (tempo de resposta) das requisições
REQUEST_LATENCY = Histogram(
    f"{SERVICE_NAME}_request_latency_seconds",
    "Latência de requisições gRPC em segundos",
    ["method"],
)


# --- Wrapper para simplificar a instrumentação ---
def instrumented(method_handler):
    """Decorator para instrumentar métodos gRPC com métricas de tempo e contagem."""
    method_name = method_handler.__name__

    def wrapper(self, request, context):
        status = "UNKNOWN"

        with REQUEST_LATENCY.labels(method=method_name).time():
            try:
                response = method_handler(self, request, context)
                status = "OK"
                return response

            except Exception as e:
                code = context.code() if context.code() else grpc.StatusCode.INTERNAL

                # Obtém o nome do status (corrigido para o problema de enum)
                status_code_name = code.name

                REQUEST_COUNT.labels(
                    method=method_name, status_code=status_code_name
                ).inc()

                raise e

            finally:
                if status == "OK":
                    REQUEST_COUNT.labels(method=method_name, status_code="OK").inc()

    return wrapper


class ServiceAServicer(service_pb2_grpc.ServiceAServicer):
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 5432)),
            database=os.getenv("DB_NAME", "pspd-db"),
            user=os.getenv("DB_USER", "pspd-user"),
            password=os.getenv("DB_PASSWORD", "pspd123"),
        )
        self.conn.autocommit = True

    @instrumented
    def ListarProdutos(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id, nome, descricao, preco FROM produto")
            produtos = [
                service_pb2.ProdutoResponse(
                    id=str(id), nome=nome, descricao=descricao or "", preco=preco
                )
                for id, nome, descricao, preco in cur.fetchall()
            ]
            return service_pb2.ListaProdutosResponse(produtos=produtos)
        except Exception as e:
            self.conn.rollback()
            context.set_details(f"Erro ao listar produtos: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            raise grpc.RpcError(e)
        finally:
            cur.close()

    @instrumented
    def ObterProduto(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute(
                "SELECT id, nome, descricao, preco FROM produto WHERE id = %s",
                (request.id,),
            )
            row = cur.fetchone()
            if not row:
                context.set_details("Produto não encontrado")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                raise grpc.RpcError("Produto não encontrado")
            id, nome, descricao, preco = row
            return service_pb2.ProdutoResponse(
                id=str(id), nome=nome, descricao=descricao or "", preco=preco
            )
        except Exception as e:
            self.conn.rollback()
            context.set_details(f"Erro ao obter produto: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            raise grpc.RpcError(e)
        finally:
            cur.close()

    @instrumented
    def CriarProduto(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute(
                "INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s) RETURNING id, nome, descricao, preco",
                (request.nome, request.descricao, request.preco),
            )
            row = cur.fetchone()
            if not row:
                raise Exception("Falha ao inserir produto (nenhuma linha retornada)")

            produto_id, nome, descricao, preco = row

            cur.execute(
                "INSERT INTO estoque (\"produtoId\", quantidade, localizacao) VALUES (%s, %s, %s)",
                (produto_id, 0, "Depósito Padrão"),
            )

            print(
                f"[Server A] Produto criado: {nome} (id={produto_id}) com estoque inicial."
            )
            return service_pb2.ProdutoResponse(
                id=str(produto_id), nome=nome, descricao=descricao or "", preco=preco
            )

        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass

            context.set_details(f"Erro ao criar produto: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            raise grpc.RpcError(e)

        finally:
            cur.close()

    @instrumented
    def EditarProduto(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute(
                "UPDATE produto SET nome=%s, descricao=%s, preco=%s WHERE id=%s RETURNING id, nome, descricao, preco",
                (request.nome, request.descricao, request.preco, request.id),
            )
            if cur.rowcount == 0:
                context.set_details("Produto não encontrado para atualização")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                raise grpc.RpcError("Produto não encontrado")
            row = cur.fetchone()
            id, nome, descricao, preco = row
            print(f"[Server A] Produto editado: {nome}")
            return service_pb2.ProdutoResponse(
                id=str(id), nome=nome, descricao=descricao or "", preco=preco
            )
        except Exception as e:
            context.set_details(f"Erro ao editar produto: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            raise grpc.RpcError(e)
        finally:
            cur.close()

    @instrumented
    def DeletarProduto(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute("DELETE FROM estoque WHERE \"produtoId\" = %s", (request.id,))
            cur.execute("DELETE FROM produto WHERE id = %s RETURNING id", (request.id,))

            if cur.rowcount == 0:
                context.set_details("Produto não encontrado")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                raise grpc.RpcError("Produto não encontrado")

            print(
                f"[Server A] Produto {request.id} deletado (estoque associado removido)."
            )
            return service_pb2.DeleteResponse(
                sucesso=True, mensagem=f"Produto {request.id} removido com sucesso"
            )

        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass

            context.set_details(f"Erro ao deletar produto: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            raise grpc.RpcError(e)

        finally:
            cur.close()

    @instrumented
    def DoSomething(self, request, context):
        try:
            input_value = request.input
            output_message = f"gRPC Server (A) processou a requisição. Valor recebido de input: {input_value}"
            return service_pb2.Response(output=output_message)
        except Exception as e:
            context.set_details(f"Erro interno: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            raise grpc.RpcError(e)


def serve():
    start_http_server(8000)
    print(f"Servidor de Métricas do Prometheus ({SERVICE_NAME}) iniciado na porta 8000")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    try:
        ServiceAServicer()
    except Exception as e:
        print(
            f"Erro fatal na conexão inicial do DB: {e}. O initContainer pode ter avançado muito rápido."
        )

    service_pb2_grpc.add_ServiceAServicer_to_server(ServiceAServicer(), server)
    server.add_insecure_port("0.0.0.0:5000")
    print("[Server A - Python] Iniciado com sucesso na porta 5000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
