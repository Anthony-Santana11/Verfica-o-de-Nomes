from sqlalchemy.orm import Session
from db.models import NomeComum
from difflib import get_close_matches

def sugerir_nome_automatico(parte_nome, session: Session):
    nomes_comuns = [n.nome for n in session.query(NomeComum).all()]
    sugestao = get_close_matches(parte_nome.capitalize(), nomes_comuns, n=1)
    return sugestao[0] if sugestao else parte_nome

nomes_comuns = [
    "João", "José", "Antonio", "Francisco", "Carlos", "Paulo", "Pedro", "Lucas", "Luiz", "Marcos"
    # ...adicione mais nomes comuns masculinos
]
sobrenomes_comuns = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Almeida", "Costa", "Gomes", "Martins"
    # ...adicione mais sobrenomes comuns
]

def sugerir_nome_sobrenome(nome_completo):
    partes = nome_completo.split()
    nome = partes[0] if partes else ""
    sobrenome = " ".join(partes[1:]) if len(partes) > 1 else ""
    nome_sug = get_close_matches(nome.capitalize(), nomes_comuns, n=1)
    sobrenome_sug = get_close_matches(sobrenome.capitalize(), sobrenomes_comuns, n=1) if sobrenome else []
    return (
        nome, sobrenome,
        nome_sug[0] if nome_sug else nome,
        sobrenome_sug[0] if sobrenome_sug else sobrenome
    )