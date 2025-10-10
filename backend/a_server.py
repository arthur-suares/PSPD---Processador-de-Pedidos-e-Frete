import grpc
from concurrent import futures
from proto import service_pb2, service_pb2_grpc
import psycopg2
import os


class ServiceAServicer(service_pb2_grpc.ServiceAServicer):
    def __init__(self):
        # Conexão única com o banco
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            database=os.getenv('DB_NAME', 'pspd-db'),
            user=os.getenv('DB_USER', 'pspd-user'),
            password=os.getenv('DB_PASSWORD', 'pspd123')
        )

    def ListarProdutos(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id, nome, descricao, preco FROM produto")
            produtos = [
                service_pb2.ProdutoResponse(
                    id=str(id),
                    nome=nome,
                    descricao=descricao or "",
                    preco=preco
                )
                for id, nome, descricao, preco in cur.fetchall()
            ]
            return service_pb2.ListaProdutosResponse(produtos=produtos)
        except Exception as e:
            self.conn.rollback()
            context.set_details(f"Erro ao listar produtos: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.ListaProdutosResponse()
        finally:
            cur.close()

    def ObterProduto(self, request, context):
        cur = self.conn.cursor()
        try:
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
        except Exception as e:
            self.conn.rollback()
            context.set_details(f"Erro ao obter produto: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.ProdutoResponse()
        finally:
            cur.close()

    def CriarProduto(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute(
                "INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s) RETURNING id, nome, descricao, preco",
                (request.nome, request.descricao, request.preco)
            )
            row = cur.fetchone()
            self.conn.commit()
            id, nome, descricao, preco = row
            print(f"[Server A] Produto criado: {nome}")
            return service_pb2.ProdutoResponse(
                id=str(id),
                nome=nome,
                descricao=descricao or "",
                preco=preco
            )
        except Exception as e:
            self.conn.rollback()
            context.set_details(f"Erro ao criar produto: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.ProdutoResponse()
        finally:
            cur.close()

    def EditarProduto(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute(
                "UPDATE produto SET nome=%s, descricao=%s, preco=%s WHERE id=%s RETURNING id, nome, descricao, preco",
                (request.nome, request.descricao, request.preco, request.id)
            )
            if cur.rowcount == 0:
                context.set_details("Produto não encontrado para atualização")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                self.conn.rollback()
                return service_pb2.ProdutoResponse()
            row = cur.fetchone()
            self.conn.commit()
            id, nome, descricao, preco = row
            print(f"[Server A] Produto editado: {nome}")
            return service_pb2.ProdutoResponse(
                id=str(id),
                nome=nome,
                descricao=descricao or "",
                preco=preco
            )
        except Exception as e:
            self.conn.rollback()
            context.set_details(f"Erro ao editar produto: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.ProdutoResponse()
        finally:
            cur.close()

    def DeletarProduto(self, request, context):
        cur = self.conn.cursor()
        try:
            cur.execute("DELETE FROM produto WHERE id = %s", (request.id,))
            if cur.rowcount == 0:
                self.conn.rollback()
                return service_pb2.DeleteResponse(
                    sucesso=False,
                    mensagem="Produto não encontrado"
                )
            self.conn.commit()
            print(f"[Server A] Produto {request.id} deletado.")
            return service_pb2.DeleteResponse(
                sucesso=True,
                mensagem=f"Produto {request.id} removido com sucesso"
            )
        except Exception as e:
            self.conn.rollback()
            context.set_details(f"Erro ao deletar produto: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.DeleteResponse(
                sucesso=False,
                mensagem=f"Erro ao deletar produto: {e}"
            )
        finally:
            cur.close()

    def DoSomething(self, request, context):
        try:
            input_value = request.input
            output_message = f"gRPC Server (A) processou a requisição. Valor recebido de input: {input_value}"
            return service_pb2.Response(output=output_message)
        except Exception as e:
            context.set_details(f"Erro interno: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.Response(output="Erro interno no servidor.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ServiceAServicer_to_server(ServiceAServicer(), server)
    server.add_insecure_port("0.0.0.0:5000")
    print("[Server A - Python] Iniciado com sucesso na porta 5000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    print("Módulo gRPC (A) rodando em http://localhost:5000")