import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QListWidget, QMessageBox, QLabel, QHBoxLayout, QHeaderView, QTableWidget, QTableWidgetItem, QInputDialog
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize
from db.db import SessionLocal, engine
from db.models import NomePasta, Base
from sqlalchemy.orm import Session
from difflib import get_close_matches
from rapidfuzz import process
import qdarkstyle

Base.metadata.create_all(bind=engine)

DARK_STYLE = """
QWidget { background-color: #232629; color: #f0f0f0; font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; }
QPushButton { background-color: #3a3f44; color: #fff; border-radius: 8px; padding: 8px 16px; font-weight: bold; }
QPushButton:hover { background-color: #50555a; }
QPushButton:pressed { background-color: #222; }
QListWidget, QTableWidget { background-color: #2c2f33; color: #f0f0f0; border: 1px solid #444; }
QHeaderView::section { background-color: #444; color: #fff; font-weight: bold; border: none; }
QTableWidget QTableCornerButton::section { background-color: #444; }
QLineEdit, QInputDialog { background-color: #232629; color: #f0f0f0; border: 1px solid #444; border-radius: 5px; }
QLabel { color: #f0f0f0; }
"""

def remover_acentos(texto):
    acentos = {
        'a': ['à', 'á', 'â', 'ã', 'ä', 'å'],
        'e': ['è', 'é', 'ê', 'ë'],
        'i': ['ì', 'í', 'î', 'ï'],
        'o': ['ò', 'ó', 'ô', 'õ', 'ö'],
        'u': ['ù', 'ú', 'û', 'ü'],
        'c': ['ç'],
        'n': ['ñ']
    }
    for letra, acentos_variantes in acentos.items():
        for acento in acentos_variantes:
            texto = texto.replace(acento, letra)
    return texto

def sugerir_nome_automatico(parte_nome, session: Session):
    if not parte_nome:
        return ""
    nomes_padrao = [
        n.nome_original for n in session.query(NomePasta).filter(
            NomePasta.pasta_raiz == "PADRAO",
            NomePasta.nome_original != None
        )
    ]
    nomes_normalizados = {remover_acentos(n).lower(): n for n in nomes_padrao if n}
    entrada_normalizada = remover_acentos(parte_nome).lower()
    resultado = process.extractOne(
        entrada_normalizada,
        list(nomes_normalizados.keys()),
        score_cutoff=70
    )
    if resultado:
        return nomes_normalizados[resultado[0]]
    if not session.query(NomePasta).filter_by(nome_original=parte_nome.capitalize(), sobrenome_original=None).first():
        print(f"Adicionando nome padrão automaticamente: {parte_nome.capitalize()}")
        session.add(NomePasta(
            pasta_raiz="PADRAO",
            nome_original=parte_nome.capitalize(),
            sobrenome_original=None,
            nome_sugerido=parte_nome.capitalize(),
            sobrenome_sugerido=None,
            corrigido=True,
            nome_padrao=True,
            sobrenome_padrao=False
        ))
        session.commit()
    return parte_nome.capitalize()

def sugerir_sobrenome_automatico(sobrenome, session: Session):
    preposicoes = {"da", "de", "do", "das", "dos", "e"}
    partes = sobrenome.split()
    if not partes:
        return ""
    preps = []
    i = 0
    while i < len(partes) and partes[i].lower() in preposicoes:
        preps.append(partes[i].lower())
        i += 1
    resto = " ".join(partes[i:])
    if resto:
        sobrenomes_padrao = [
            n.sobrenome_original for n in session.query(NomePasta).filter(
                NomePasta.pasta_raiz == "PADRAO",
                NomePasta.sobrenome_original != None
            )
        ]
        sobrenomes_normalizados = {remover_acentos(n).lower(): n for n in sobrenomes_padrao if n}
        entrada_normalizada = remover_acentos(resto).lower()
        resultado = process.extractOne(
            entrada_normalizada,
            list(sobrenomes_normalizados.keys()),
            score_cutoff=70
        )
        if resultado:
            sugerido = sobrenomes_normalizados[resultado[0]]
        else:
            if not session.query(NomePasta).filter_by(nome_original=None, sobrenome_original=resto.capitalize()).first():
                print(f"Adicionando sobrenome padrão automaticamente: {resto.capitalize()}")
                session.add(NomePasta(
                    pasta_raiz="PADRAO",
                    nome_original=None,
                    sobrenome_original=resto.capitalize(),
                    nome_sugerido=None,
                    sobrenome_sugerido=resto.capitalize(),
                    corrigido=True,
                    nome_padrao=False,
                    sobrenome_padrao=True
                ))
                session.commit()
            sugerido = resto.capitalize()
        return f"{' '.join(preps)} {sugerido}".strip()
    else:
        return " ".join(preps)

def formatar_nome_abnt2(nome):
    preposicoes = {"da", "de", "do", "das", "dos", "e"}
    partes = nome.split()
    partes_formatadas = [
        p.lower() if p.lower() in preposicoes else p.capitalize()
        for p in partes
    ]
    return " ".join(partes_formatadas)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Validador de Nomes de Pastas")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(DARK_STYLE)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Registros atuais no banco de dados:")
        self.label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Pasta Raiz", "Nome Original", "Sobrenome Original", "Nome Sugerido", "Sobrenome Sugerido"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFont(QFont("Segoe UI", 12))
        self.layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.btn_selecionar = QPushButton("Selecionar Pasta para Análise")
        self.btn_selecionar.setIcon(QIcon("icons/folder.png"))
        self.btn_selecionar.setIconSize(QSize(24, 24))
        btn_layout.addWidget(self.btn_selecionar)
        self.btn_selecionar.clicked.connect(self.selecionar_pasta)

        self.btn_adicionar_padrao = QPushButton("Adicionar Nome/Sobrenome Padrão")
        self.btn_adicionar_padrao.setIcon(QIcon("icons/add-user.png"))
        self.btn_adicionar_padrao.setIconSize(QSize(24, 24))
        btn_layout.addWidget(self.btn_adicionar_padrao)
        self.btn_adicionar_padrao.clicked.connect(self.adicionar_padrao)

        self.layout.addLayout(btn_layout)

        self.lista = QListWidget()
        self.layout.addWidget(self.lista)

        self.layout.setSpacing(16)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        session = SessionLocal()
        registros = session.query(NomePasta).all()
        self.table.setRowCount(len(registros))
        for i, reg in enumerate(registros):
            self.table.setItem(i, 0, QTableWidgetItem(str(reg.id)))
            self.table.setItem(i, 1, QTableWidgetItem(reg.pasta_raiz if reg.pasta_raiz else ""))
            self.table.setItem(i, 2, QTableWidgetItem(reg.nome_original if reg.nome_original else ""))
            self.table.setItem(i, 3, QTableWidgetItem(reg.sobrenome_original if reg.sobrenome_original else ""))
            self.table.setItem(i, 4, QTableWidgetItem(reg.nome_sugerido if reg.nome_sugerido else ""))
            self.table.setItem(i, 5, QTableWidgetItem(reg.sobrenome_sugerido if reg.sobrenome_sugerido else ""))
        session.close()

    def selecionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecione a pasta raiz para análise")
        if pasta:
            subpastas = [nome for nome in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, nome))]
            session = SessionLocal()
            for nome_completo in subpastas:
                partes = nome_completo.split()
                nome = partes[0] if partes else ""
                sobrenome = " ".join(partes[1:]) if len(partes) > 1 else ""
                nome_sug = formatar_nome_abnt2(sugerir_nome_automatico(nome, session))
                sobrenome_sug = formatar_nome_abnt2(sugerir_sobrenome_automatico(sobrenome, session)) if sobrenome else ""

                print(f"Analisando: '{nome_completo}' -> Sugerido: '{nome_sug} {sobrenome_sug}'")
                self.lista.addItem(f"{nome_completo} -> {nome_sug} {sobrenome_sug}")

                session.add(NomePasta(
                    pasta_raiz=os.path.basename(pasta),
                    nome_original=nome,
                    sobrenome_original=sobrenome,
                    nome_sugerido=nome_sug,
                    sobrenome_sugerido=sobrenome_sug
                ))
            session.commit()
            session.close()
            self.atualizar_tabela()
            print("Análise de subpastas concluída!")
            QMessageBox.information(self, "Concluído", "Nomes das subpastas processados e salvos no banco.")

    def adicionar_padrao(self):
        session = SessionLocal()
        texto, ok = QInputDialog.getText(self, "Adicionar Nome/Sobrenome Padrão", "Digite o nome ou sobrenome:")
        if ok and texto.strip():
            tipo, ok_tipo = QInputDialog.getItem(
                self, "Tipo", "É um nome ou sobrenome?", ["Nome", "Sobrenome"], 0, False
            )
            if ok_tipo:
                if tipo == "Nome":
                    if not session.query(NomePasta).filter_by(nome_original=texto.strip(), sobrenome_original=None).first():
                        print(f"Usuário adicionou nome padrão: {texto.strip()}")
                        session.add(NomePasta(
                            pasta_raiz="PADRAO",
                            nome_original=texto.strip(),
                            sobrenome_original=None,
                            nome_sugerido=texto.strip(),
                            sobrenome_sugerido=None,
                            corrigido=True,
                            nome_padrao=True,
                            sobrenome_padrao=False
                        ))
                else:
                    if not session.query(NomePasta).filter_by(nome_original=None, sobrenome_original=texto.strip()).first():
                        print(f"Usuário adicionou sobrenome padrão: {texto.strip()}")
                        session.add(NomePasta(
                            pasta_raiz="PADRAO",
                            nome_original=None,
                            sobrenome_original=texto.strip(),
                            nome_sugerido=None,
                            sobrenome_sugerido=texto.strip(),
                            corrigido=True,
                            nome_padrao=False,
                            sobrenome_padrao=True
                        ))
                session.commit()
                QMessageBox.information(self, "Sucesso", f"{tipo} padrão adicionado!")
                self.atualizar_tabela()
        session.close()

def inserir_nomes_e_sobrenomes_padrao_na_nomes_pasta():
    print("Inserindo nomes e sobrenomes padrão...")
    nomes_padrao = [
       "Miguel", "Arthur", "Heitor", "Gael", "Theo", "Davi", "Bernardo", "Gabriel", "Ravi", "Noah",
    "Samuel", "Pedro", "Lorenzo", "Benjamin", "Matheus", "Lucas", "Isaac", "João", "Gustavo", "Henrique",
    "Nicolas", "Daniel", "Rafael", "Enzo", "Emanuel", "Anthony", "Leonardo", "Vicente", "Bryan", "Thiago",
    "Eduardo", "Felipe", "Joaquim", "Vinicius", "Caio", "Guilherme", "Erick", "Ryan", "Otávio", "Breno",
    "Lucca", "Matias", "Tomás", "Ian", "Nathan", "Pietro", "Raul", "Diego", "Igor", "Vitor",
    "Alexandre", "André", "Antônio", "Álvaro", "Bruno", "Carlos", "Cristian", "Cristiano", "Danilo", "Denis",
    "Douglas", "Edgar", "Elias", "Eliseu", "Emiliano", "Emilson", "Everton", "Fabrício", "Fábio", "Flávio",
    "Francisco", "Frederico", "Hélio", "Hugo", "Iago", "Ícaro", "Jadson", "Jair", "Jaime", "Janderson",
    "Janilson", "Jardel", "Jean", "Jefferson", "Jerônimo", "Jonas", "Jonathan", "Jorge", "José", "Josias",
    "Josué", "Juan", "Júlio", "Leandro", "Levi", "Luciano", "Luís", "Luiz", "Márcio", "Marcos",
    "Maurício", "Moisés", "Murilo", "Natanael", "Nelson", "Octávio", "Olavo", "Orlando", "Osvaldo", "Pablo",
    "Patrick", "Paulo", "Raimundo", "Renato", "Ricardo", "Robson", "Rodrigo", "Ruan", "Rubens", "Sandro",
    "Saulo", "Sérgio", "Sidney", "Silas", "Silvano", "Silvio", "Tales", "Tiago", "Ubirajara", "Valdir",
    "Valter", "Vagner", "Victor", "Vicente", "Vinicius", "Wagner", "Wallace", "Washington", "Wellington", "Wesley",
    "Willian", "Yuri", "Zacarias", "Zaqueu", "Adriel", "Agnaldo", "Alan", "Alberto", "Aldo", "Alejandro",
    "Aloísio", "Amadeu", "Amaro", "Amílcar", "Ananias", "Anselmo", "Antenor", "Aristeu", "Arlindo", "Armando",
    "Arnaldo", "Arnon", "Arsenio", "Assis", "Aureliano", "Aurelio", "Baltasar", "Belmiro", "Benedito", "Benício",
    "Bonifácio", "Cássio", "Celso", "César", "Cláudio", "Clemente", "Clever", "Clodomir", "Clodovaldo", "Conrado",
    "Crispim", "Damião", "Dário", "Décio", "Demétrio", "Dener", "Dirceu", "Domingos", "Dorival", "Durval",
    "Edgard", "Edílson", "Edivaldo", "Egidio", "Elói", "Emanuel", "Eron", "Estêvão", "Evaristo", "Ezequiel","Adriano", "Afonso", "Alan", "Alberto", "Aldair", "Aleandro", "Alejandro", "Alesandro", "Alessandro", "Alex",
    "Alexandre", "Alexsandro", "Almir", "Alonso", "Altemar", "Altino", "Amadeu", "Amauri", "Américo", "Amílcar",
    "Ananias", "Anderson", "Ângelo", "Anselmo", "Antônio", "Antenor", "Aristeu", "Arlindo", "Armando", "Arnaldo",
    "Aron", "Artur", "Atílio", "Augusto", "Aureliano", "Aurelio", "Baltazar", "Belmiro", "Benedito", "Benício",
    "Benjamim", "Bonifácio", "Breno", "Caetano", "Calebe", "Cássio", "Célio", "César", "Cirilo", "Cláudio",
    "Clemente", "Clever", "Cristiano", "Damião", "Dário", "Décio", "Demétrio", "Dener", "Dirceu", "Domingos",
    "Dorival", "Durval", "Edgard", "Edílson", "Edivaldo", "Egídio", "Elcio", "Eliseu", "Eloy", "Elpídio",
    "Enéas", "Epaminondas", "Erasmo", "Eron", "Estêvão", "Eurico", "Evaldo", "Evaristo", "Ezequiel", "Fábio",
    "Fabrício", "Fausto", "Felício", "Felisberto", "Ferdinando", "Fernando", "Firmino", "Flávio", "Floriano", "Fortunato",
    "Francisco", "Frederico", "Geraldo", "Germano", "Gervásio", "Getúlio", "Gonçalo", "Gregório", "Guido", "Heráclito"
    ]

    sobrenomes_padrao = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes",
    "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa",
    "Rocha", "Dias", "Nunes", "Moreira", "Cavalcante", "Teixeira", "Correia", "Moura", "Araújo", "Cardoso",
    "Monteiro", "Pinto", "Batista", "Freitas", "Ramos", "Jesus", "Campos", "Medeiros", "Bezerra", "Antunes",
    "Macedo", "Sales", "Braga", "Farias", "Pires", "Rezende", "Andrade", "Assis", "Camargo", "Coelho",
    "Azevedo", "Magalhães", "Barros", "Tavares", "Queiroz", "Borges", "Abreu", "Brandão", "Viana", "Neves",
    "Castro", "Pinheiro", "Mello", "Brito", "Aguiar", "Figueiredo", "Serra", "Cunha", "Moraes", "Leite",
    "Machado", "Mendes", "Garcia", "Peixoto", "Siqueira", "Simões", "Fontes", "Prado", "Motta", "Bittencourt",
    "Coutinho", "Chaves", "Cordeiro", "Xavier", "Amaral", "Seabra", "Lacerda", "Pacheco", "Beltrão", "Porto",
    "Rangel", "Souto", "Valente", "Franco", "Lourenço", "Duarte", "Lacerda", "Meireles", "Saldanha", "Sarmento",
    "Fagundes", "Pimentel", "Montalvão", "Rezende", "Quevedo", "Vieira", "Vasconcelos", "Torres", "Veloso", "Vargas",
    "Goulart", "Guimarães", "Gomes", "Castanho", "Benevides", "Pontes", "Carneiro", "Mansur", "Frota", "Novaes",
    "Trindade", "Espindola", "Severino", "Nóbrega", "Parente", "Paiva", "Drummond", "Pimentel", "Lustosa", "Marques",
    "Valle", "Barcellos", "Roriz", "Paredes", "Sabino", "Saraiva", "Ferraz", "Maranhão", "Milani", "Menezes",
    "Pedrosa", "Rezende", "Roldão", "Sampaio", "Teles", "Toledo", "Tomaz", "Trigueiros", "Valladares", "Vasques",
    "Veras", "Vidal", "Vilela", "Villela", "Zanetti", "Zanini", "Zanotto", "Zapata", "Zappa", "Zaranza",
    "Zardo", "Zavan", "Zerbini", "Zerbinatti", "Ziegler", "Zimmermann", "Zini", "Zorzi", "Zottis", "Zuin",
    "Assunção", "Bacelar", "Baldin", "Baldini", "Balestra", "Balestrin", "Ballesteros", "Baltar", "Bandeira", "Banhos",
    "Barboza", "Bardini", "Barradas", "Basilio", "Bastiani", "Bastos", "Bataglia", "Batista", "Baumgartner", "Becker",
    "Belini", "Belotto", "Benedetti", "Benetti", "Benvenutti", "Beraldo", "Bergamini", "Bergamo", "Bernardi", "Bianchi",
    "Bianchini", "Bianco", "Bilac", "Bizzarri", "Boccato", "Bocchi", "Boff", "Boffi", "Boffo", "Bolzan","Amado", "Amorim", "Anjos", "Aparício", "Aragão", "Arruda", "Avila", "Bacelar", "Bandeira", "Barcellos",
    "Barreto", "Barros", "Bastos", "Bastos", "Beltrão", "Benevides", "Bittencourt", "Borges", "Branco", "Brandão",
    "Buarque", "Cabral", "Calixto", "Câmara", "Campos", "Canedo", "Capistrano", "Caputo", "Carneiro", "Carrara",
    "Castilho", "Castro", "Cavalcanti", "Cavalcante", "Cerdeira", "Cerqueira", "Cesar", "Chaves", "Cintra", "Coelho",
    "Colares", "Conceição", "Cordeiro", "Corrêa", "Cortez", "Coutinho", "Crispim", "Cunha", "Curvelo", "Custódio",
    "Damasceno", "Dantas", "Delgado", "Dorneles", "Drumond", "Duarte", "Dutra", "Escobar", "Espínola", "Esteves",
    "Fagundes", "Falcão", "Farias", "Faro", "Faustino", "Feliciano", "Fialho", "Figueira", "Fioravante", "Florêncio",
    "Floriano", "Fogaça", "Fornari", "Fortes", "Fraga", "França", "Franco", "Frota", "Furtado", "Galvão",
    "Gandra", "Garcia", "Gaspar", "Gentil", "Geraldes", "Germano", "Gervásio", "Godinho", "Goes", "Gonçalves",
    "Gouveia", "Graciano", "Gregório", "Guerra", "Gusmão", "Haddad", "Henrique", "Hermes", "Hilário", "Holanda"
    ]

    session = SessionLocal()
    for nome in nomes_padrao:
        if not session.query(NomePasta).filter_by(nome_original=nome, sobrenome_original=None).first():
            print(f"Inserindo nome padrão: {nome}")
            session.add(NomePasta(
                pasta_raiz="PADRAO",
                nome_original=nome,
                sobrenome_original=None,
                nome_sugerido=nome,
                sobrenome_sugerido=None,
                corrigido=True,
                nome_padrao=True,
                sobrenome_padrao=False
            ))
    for sobrenome in sobrenomes_padrao:
        if not session.query(NomePasta).filter_by(nome_original=None, sobrenome_original=sobrenome).first():
            print(f"Inserindo sobrenome padrão: {sobrenome}")
            session.add(NomePasta(
                pasta_raiz="PADRAO",
                nome_original=None,
                sobrenome_original=sobrenome,
                nome_sugerido=None,
                sobrenome_sugerido=sobrenome,
                corrigido=True,
                nome_padrao=False,
                sobrenome_padrao=True
            ))
    session.commit()
    session.close()
    print("Finalizado inserção de nomes e sobrenomes padrão!")

if __name__ == "__main__":
    inserir_nomes_e_sobrenomes_padrao_na_nomes_pasta()
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())