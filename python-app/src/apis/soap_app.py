from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.serving import run_simple
from .. import services
from ..database import SessionLocal

class UsuarioModel(ComplexModel):
    id = Integer
    nome = Unicode
    idade = Integer

class MusicaModel(ComplexModel):
    id = Integer
    nome = Unicode
    artista = Unicode

class StreamingService(ServiceBase):
    @rpc(_returns=Iterable(UsuarioModel))
    def ListarUsuarios(ctx):
        db = SessionLocal()
        try:
            usuarios = services.listar_usuarios(db)
            # Retorna uma lista diretamente. Se estiver vazia, retorna [], evitando o StopIteration
            return [UsuarioModel(id=u.id, nome=u.nome, idade=u.idade) for u in usuarios]
        finally:
            db.close() # Garante que a conexão sempre feche, blindando contra o Locust!

    @rpc(_returns=Iterable(MusicaModel))
    def ListarMusicas(ctx):
        db = SessionLocal()
        try:
            musicas = services.listar_musicas(db)
            return [MusicaModel(id=m.id, nome=m.nome, artista=m.artista) for m in musicas]
        finally:
            db.close()

application = Application([StreamingService],
    tns='streaming.soap.example',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    print("SOAP Python rodando na porta 8002")
    run_simple('0.0.0.0', 8002, wsgi_app)