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
        musicas = services.listar_musicas(db)
        db.close()
        return streaming_pb2.MusicaList(musicas=[streaming_pb2.Musica(**m.__dict__) for m in musicas])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("gRPC Python rodando na porta 50052")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()