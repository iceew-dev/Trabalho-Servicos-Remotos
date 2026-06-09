from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Tabela associativa invisível para gerenciar a relação N:M entre Músicas e Playlists
playlist_musica_association = Table(
    'playlist_musica', Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id'), primary_key=True),
    Column('musica_id', Integer, ForeignKey('musicas.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    
    playlists = relationship("Playlist", back_populates="usuario")

class Musica(Base):
    __tablename__ = 'musicas'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    artista = Column(String, nullable=False)
    
    playlists = relationship("Playlist", secondary=playlist_musica_association, back_populates="musicas")

class Playlist(Base):
    __tablename__ = 'playlists'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    usuario = relationship("Usuario", back_populates="playlists")
    musicas = relationship("Musica", secondary=playlist_musica_association, back_populates="playlists")