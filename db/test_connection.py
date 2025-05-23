from db import engine
from sqlalchemy import text

def testar_conexao():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';"))
            tabelas = [row[0] for row in result]
            print("Conexão bem-sucedida!")
            print("Tabelas existentes:", tabelas)
    except Exception as e:
        print("Erro ao conectar:", e)

if __name__ == "__main__":
    testar_conexao()