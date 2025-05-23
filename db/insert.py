from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração do banco de dados
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/nomes_pasta?client_encoding=utf8"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo da tabela de nomes das pastas
class NomePasta(Base):
    __tablename__ = 'nomes_pasta'
    id = Column(Integer, primary_key=True)
    nome_original = Column(String, nullable=False)
    nome_sugerido = Column(String)
    corrigido = Column(Boolean, default=False)

# Modelo da tabela de nomes comuns
class NomeComum(Base):
    __tablename__ = 'nomes_comuns'
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)

# Criação das tabelas
def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

# Inserção de nomes comuns brasileiros
def inserir_nomes_comuns():
    nomes_brasil = [
        "João", "Maria", "José", "Ana", "Francisco", "Antônio", "Carlos", "Paulo", "Pedro", "Lucas",
        "Marcos", "Luiz", "Gabriel", "Rafael", "Mateus", "Bruno", "Felipe", "Gustavo", "Daniel", "Vinícius",
        "Rodrigo", "Eduardo", "Fernando", "Ricardo", "Roberto", "Sandra", "Patrícia", "Aline", "Camila", "Juliana",
        "Letícia", "Larissa", "Beatriz", "Amanda", "Bruna", "Carolina", "Fernanda", "Gabriela", "Isabela", "Jéssica",
        "Luana", "Manuela", "Natália", "Priscila", "Renata", "Sabrina", "Tatiane", "Vanessa", "Yasmin", "Sofia"
    ]
    session = SessionLocal()
    for nome in nomes_brasil:
        if not session.query(NomeComum).filter_by(nome=nome).first():
            session.add(NomeComum(nome=nome))
    session.commit()
    session.close()
    print("Nomes comuns inseridos com sucesso!")

# Exemplo de inserção na tabela de nomes das pastas
def inserir_nome_pasta(nome_original, nome_sugerido=None, corrigido=False):
    session = SessionLocal()
    try:
        novo_nome = NomePasta(
            nome_original=nome_original,
            nome_sugerido=nome_sugerido,
            corrigido=corrigido
        )
        session.add(novo_nome)
        session.commit()
        print(f"Inserido: {nome_original} (sugerido: {nome_sugerido})")
    except Exception as e:
        print("Erro ao inserir nome da pasta:", e)
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    criar_tabelas()
    inserir_nomes_comuns()
    # Exemplos de inserção de nomes de pastas
    inserir_nome_pasta("Joao", "João")
    inserir_nome_pasta("Maria", None)
    inserir_nome_pasta("Pedrro", "Pedro")
    inserir_nome_pasta("An", "Ana")