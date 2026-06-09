const express = require('express');
const services = require('../services');

const app = express();
app.use(express.json());

app.get('/usuarios', async (req, res) => {
    try {
        res.json(await services.listarUsuarios());
    } catch (error) {
        res.status(500).json({ erro: 'Falha ao buscar usuários' });
    }
});

app.get('/musicas', async (req, res) => {
    try {
        res.json(await services.listarMusicas());
    } catch (error) {
        res.status(500).json({ erro: 'Falha ao buscar músicas' });
    }
});

app.get('/usuarios/:id/playlists', async (req, res) => {
    try {
        res.json(await services.listarPlaylistsDoUsuario(req.params.id));
    } catch (error) {
        res.status(500).json({ erro: 'Falha ao buscar playlists do usuário' });
    }
});

app.get('/playlists/:id/musicas', async (req, res) => {
    try {
        res.json(await services.listarMusicasDaPlaylist(req.params.id));
    } catch (error) {
        res.status(500).json({ erro: 'Falha ao buscar músicas da playlist' });
    }
});

app.get('/musicas/:id/playlists', async (req, res) => {
    try {
        res.json(await services.listarPlaylistsComMusica(req.params.id));
    } catch (error) {
        res.status(500).json({ erro: 'Falha ao buscar playlists com a música' });
    }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`REST Node.js rodando na porta ${PORT}`));