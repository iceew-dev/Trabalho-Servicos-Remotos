from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .. import services
from ..database import get_db

app = FastAPI()

@app.get("/usuarios")
def ler_usuarios(db: Session = Depends(get_db)):
    return services.listar_usuarios(db)

@app.get("/musicas")
def ler_musicas(db: Session = Depends(get_db)):
    return services.listar_musicas(db)

@app.get("/usuarios/{usuario_id}/playlists")
def ler_playlists_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return services.listar_playlists_do_usuario(db, usuario_id)

@app.get("/playlists/{playlist_id}/musicas")
def ler_musicas_playlist(playlist_id: int, db: Session = Depends(get_db)):
    return services.listar_musicas_da_playlist(db, playlist_id)

@app.get("/musicas/{musica_id}/playlists")
def ler_playlists_musica(musica_id: int, db: Session = Depends(get_db)):
    return services.listar_playlists_com_musica(db, musica_id)