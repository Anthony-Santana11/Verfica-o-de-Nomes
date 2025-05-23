from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NomePasta(Base):
    __tablename__ = 'nomes_pasta'
    id = Column(Integer, primary_key=True)
    pasta_raiz = Column(String)
    nome_original = Column(String, nullable=True)  # Altere para nullable=True
    sobrenome_original = Column(String)
    nome_sugerido = Column(String)
    sobrenome_sugerido = Column(String)
    corrigido = Column(Boolean, default=False)
    nome_padrao = Column(Boolean, default=False)
    sobrenome_padrao = Column(Boolean, default=False)
