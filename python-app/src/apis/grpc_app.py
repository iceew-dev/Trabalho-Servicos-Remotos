import grpc
from concurrent import futures
import sys
import os

# Adiciona o diretório atual ao path para importar os arquivos gerados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streaming_pb2
import streaming_pb2_grpc

from .. import services
from ..database import SessionLocal

class StreamingServiceServicer(streaming_pb2_grpc.StreamingServiceServicer):
    def ListarUsuarios(self, request, context):
        db = SessionLocal()
        usuarios = services.listar_usuarios(db)
        db.close()
        return streaming_pb2.UsuarioList(usuarios=[streaming_pb2.Usuario(**u.__dict__) for u in usuarios])

    def ListarMusicas(self, request, context):
        db = SessionLocal()
        try:
            # 1. Busca os objetos crus do banco de dados (SQLAlchemy)
            musicas_db = services.listar_musicas(db)
            
            # 2. Cria uma lista vazia para colocar as músicas formatadas para o gRPC
            musicas_grpc = []
            
            # 3. Faz a tradução manual: campo por campo
            for m in musicas_db:
                musica_formatada = streaming_pb2.Musica(
                    id=m.id,
                    nome=m.nome,
                    artista=m.artista
                    # Coloque aqui os outros campos que estiverem no seu arquivo .proto
                )
                musicas_grpc.append(musica_formatada)
            
            # 4. Devolve a resposta oficial do gRPC
            return streaming_pb2.MusicaList(musicas=musicas_grpc)
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return streaming_pb2.MusicaList() # <-- Aqui também precisava mudar!
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("gRPC Python rodando na porta 50052")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()