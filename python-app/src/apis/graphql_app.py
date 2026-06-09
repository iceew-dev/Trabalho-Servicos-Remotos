import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session
from .. import services
from ..database import get_db

@strawberry.type
class MusicaType:
    id: int
    nome: str
    artista: str

@strawberry.type
class UsuarioType:
    id: int
    nome: str
    idade: int

@strawberry.type
class PlaylistType:
    id: int
    nome: str
    usuario_id: int
    musicas: List[MusicaType]

@strawberry.type
class Query:
    @strawberry.field
    def usuarios(self) -> List[UsuarioType]:
        db = next(get_db())
        return services.listar_usuarios(db)

    @strawberry.field
    def musicas(self) -> List[MusicaType]:
        db = next(get_db())
        return services.listar_musicas(db)
        
    @strawberry.field
    def playlists_do_usuario(self, usuario_id: int) -> List[PlaylistType]:
        db = next(get_db())
        return services.listar_playlists_do_usuario(db, usuario_id)
        
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")