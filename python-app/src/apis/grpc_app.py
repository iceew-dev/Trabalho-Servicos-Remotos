import grpc
from concurrent import futures
import os
import sys
import psycopg2
from src.database import SessionLocal # Importando do seu arquivo de configuração

# Adiciona o diretório ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streaming_pb2
import streaming_pb2_grpc

class StreamingServiceServicer(streaming_pb2_grpc.StreamingServiceServicer):
    
    def ListarUsuarios(self, request, context):
        print("DEBUG: Iniciando ListarUsuarios...")
        conn = None
        try:
            # Conexão direta com o banco via psycopg2 para garantir
            db_url = os.getenv("DATABASE_URL", "postgresql://admin:password@db:5432/streaming_db")
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()
            cur.execute("SELECT id, nome, idade FROM usuarios")
            rows = cur.fetchall()
            
            print(f"DEBUG: Usuários encontrados no banco: {len(rows)}")
            
            response = streaming_pb2.UsuarioList()
            for row in rows:
                # O ID, NOME, IDADE devem bater com seu .proto
                usuario = response.usuarios.add()
                usuario.id = int(row[0])
                usuario.nome = str(row[1])
                usuario.idade = int(row[2])
            
            cur.close()
            return response
            
        except Exception as e:
            print(f"ERRO CRÍTICO: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return streaming_pb2.UsuarioList()
        finally:
            if conn:
                conn.close()

    def ListarMusicas(self, request, context):
        conn = None
        try:
            db_url = os.getenv("DATABASE_URL", "postgresql://admin:password@db:5432/streaming_db")
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()
            cur.execute("SELECT id, nome, artista FROM musicas") # Certifique-se que a tabela é 'musicas'
            rows = cur.fetchall()
            
            print(f"DEBUG: Músicas encontradas no banco: {len(rows)}")
            
            response = streaming_pb2.MusicaList()
            for row in rows:
                musica = response.musicas.add()
                musica.id = int(row[0])
                musica.nome = str(row[1])
                musica.artista = str(row[2])
            
            cur.close()
            return response
        except Exception as e:
            print(f"ERRO MÚSICAS: {e}")
            return streaming_pb2.MusicaList()
        finally:
            if conn: conn.close()
            
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("gRPC Python rodando na porta 50052")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()