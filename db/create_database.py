import psycopg2
from psycopg2 import sql

def criar_banco(nome_banco, usuario, senha, host='localhost', porta=5432):
    try:
        # Conecta ao banco padrão 'postgres'
        conn = psycopg2.connect(dbname='postgres', user='postgres', password=1234, host='localhost', port=5432)
        conn.autocommit = True
        cur = conn.cursor()
        # Cria o banco de dados
        cur.execute(sql.SQL("CREATE DATABASE {} ENCODING 'UTF8'").format(sql.Identifier(nome_banco)))
        print(f"Banco de dados '{nome_banco}' criado com sucesso!")
        cur.close()
        conn.close()
    except Exception as e:
        print("Erro ao criar banco de dados:", e)

if __name__ == "__main__":
    criar_banco('nomes_pasta', 'postgres', '1234')