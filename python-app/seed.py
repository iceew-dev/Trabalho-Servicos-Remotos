import os
import psycopg2
from psycopg2.extras import execute_values

DB_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@db:5432/streaming_db")

def seed_db():
    try:
        print("Conectando ao banco de dados...")
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()

        print("Criando tabelas...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS musicas (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                artista VARCHAR(255) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                idade INTEGER NOT NULL
            );
        """)

        print("Limpando dados antigos...")
        cursor.execute("TRUNCATE TABLE musicas, usuarios RESTART IDENTITY CASCADE;")

        print("Preparando registros...")
        musicas = [(f"Música {i}", f"Artista {i % 100}") for i in range(1, 10001)]
        usuarios = [(f"Usuário {i}", 20 + (i % 30)) for i in range(1, 101)]
        
        print("Inserindo dados...")
        execute_values(cursor, "INSERT INTO musicas (nome, artista) VALUES %s", musicas)
        execute_values(cursor, "INSERT INTO usuarios (nome, idade) VALUES %s", usuarios)

        conn.commit()
        cursor.close()
        conn.close()
        print("Sucesso! Banco populado com músicas e usuários.")

    except Exception as e:
        print(f"Erro ao popular o banco: {e}")

if __name__ == "__main__":
    seed_db()