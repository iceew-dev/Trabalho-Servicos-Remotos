const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// • Listar os dados de todos os usuários do serviço
async function listarUsuarios() {
  return await prisma.usuario.findMany();
}

// • Listar os dados de todas as músicas mantidas pelo serviço
async function listarMusicas() {
  return await prisma.musica.findMany();
}

// • Listar os dados de todas as playlists de um determinado usuário
async function listarPlaylistsDoUsuario(usuarioId) {
  return await prisma.playlist.findMany({
    where: { usuarioId: parseInt(usuarioId) },
    include: { musicas: true } // Traz as músicas junto com a playlist
  });
}

// • Listar os dados de todas as músicas de uma determinada playlist
async function listarMusicasDaPlaylist(playlistId) {
  const playlist = await prisma.playlist.findUnique({
    where: { id: parseInt(playlistId) },
    include: { musicas: true }
  });
  return playlist ? playlist.musicas : [];
}

// • Listar os dados de todas as playlists que contêm uma determinada música
async function listarPlaylistsComMusica(musicaId) {
  return await prisma.playlist.findMany({
    where: {
      musicas: {
        some: { id: parseInt(musicaId) }
      }
    }
  });
}

module.exports = {
  listarUsuarios,
  listarMusicas,
  listarPlaylistsDoUsuario,
  listarMusicasDaPlaylist,
  listarPlaylistsComMusica
};