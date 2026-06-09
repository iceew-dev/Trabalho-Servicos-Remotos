from sqlalchemy.orm import Session
from .models import Usuario, Musica, Playlist

# • Listar os dados de todos os usuários do serviço
def listar_usuarios(db: Session):
    return db.query(Usuario).all()

# • Listar os dados de todas as músicas mantidas pelo serviço
def listar_musicas(db: Session):
    return db.query(Musica).all()

# • Listar os dados de todas as playlists de um determinado usuário
def listar_playlists_do_usuario(db: Session, usuario_id: int):
    return db.query(Playlist).filter(Playlist.usuario_id == usuario_id).all()

# • Listar os dados de todas as músicas de uma determinada playlist
def listar_musicas_da_playlist(db: Session, playlist_id: int):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    return playlist.musicas if playlist else []

# • Listar os dados de todas as playlists que contêm uma determinada música
def listar_playlists_com_musica(db: Session, musica_id: int):
    return db.query(Playlist).filter(Playlist.musicas.any(id=musica_id)).all()