import os
import psycopg2
from psycopg2.extras import execute_values

DB_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@db:5432/streaming_db")

def seed_db():
    try:
        print("Conectando ao banco de dados...")
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()

        print("Criando tabela 'musicas'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS musicas (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                artista VARCHAR(255) NOT NULL
            )
        """)

        print("Limpando dados antigos...")
        cursor.execute("TRUNCATE TABLE musicas RESTART IDENTITY CASCADE;")

        print("Preparando 10.000 registros...")
        registros = [(f"Música {i}", f"Artista {i % 100}") for i in range(1, 10001)]
        
        print("Inserindo no PostgreSQL...")
        execute_values(cursor, "INSERT INTO musicas (nome, artista) VALUES %s", registros)

        conn.commit()
        cursor.close()
        conn.close()
        print("Sucesso! Banco de dados populado com 10.000 músicas.")

    except Exception as e:
        print(f"Erro ao popular o banco: {e}")

if __name__ == "__main__":
    seed_db()