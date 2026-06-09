const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const services = require('../services');

const PROTO_PATH = path.resolve(__dirname, '../protos/streaming.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true, longs: String, enums: String, defaults: true, oneofs: true
});
const streamingProto = grpc.loadPackageDefinition(packageDefinition).streaming;

const server = new grpc.Server();

server.addService(streamingProto.StreamingService.service, {
  ListarUsuarios: async (_, callback) => {
    const usuarios = await services.listarUsuarios();
    callback(null, { usuarios });
  },
  ListarMusicas: async (_, callback) => {
    const musicas = await services.listarMusicas();
    callback(null, { musicas });
  },
  ListarPlaylistsDoUsuario: async (call, callback) => {
    const playlists = await services.listarPlaylistsDoUsuario(call.request.id);
    callback(null, { playlists });
  },
  ListarMusicasDaPlaylist: async (call, callback) => {
    const musicas = await services.listarMusicasDaPlaylist(call.request.id);
    callback(null, { musicas });
  },
  ListarPlaylistsComMusica: async (call, callback) => {
    const playlists = await services.listarPlaylistsComMusica(call.request.id);
    callback(null, { playlists });
  }
});

const PORT = '0.0.0.0:50051';
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
  console.log(`gRPC Node.js rodando na porta ${PORT}`);
});