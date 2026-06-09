const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const services = require('../services');

// Definição do Schema GraphQL
const schema = buildSchema(`
  type Usuario { id: Int, nome: String, idade: Int }
  type Musica { id: Int, nome: String, artista: String }
  type Playlist { id: Int, nome: String, usuarioId: Int, musicas: [Musica] }

  type Query {
    usuarios: [Usuario]
    musicas: [Musica]
    playlistsDoUsuario(usuarioId: Int!): [Playlist]
    musicasDaPlaylist(playlistId: Int!): [Musica]
    playlistsComMusica(musicaId: Int!): [Playlist]
  }
`);

// Mapeamento dos resolvers para os nossos services
const root = {
  usuarios: async () => await services.listarUsuarios(),
  musicas: async () => await services.listarMusicas(),
  playlistsDoUsuario: async ({ usuarioId }) => await services.listarPlaylistsDoUsuario(usuarioId),
  musicasDaPlaylist: async ({ playlistId }) => await services.listarMusicasDaPlaylist(playlistId),
  playlistsComMusica: async ({ musicaId }) => await services.listarPlaylistsComMusica(musicaId)
};

const app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true // Interface visual para testar as queries
}));

const PORT = 3001;
app.listen(PORT, () => console.log(`GraphQL Node.js rodando na porta ${PORT}`));