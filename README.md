# Validador de Nomes de Pastas

O Validador de Nomes de Pastas é uma aplicação desktop desenvolvida em Python para análise, sugestão e padronização de nomes de pastas, utilizando listas de nomes e sobrenomes padrão. O sistema conta com interface gráfica moderna, integração com banco de dados PostgreSQL e correção automática de erros comuns de digitação.

---

## Funcionalidades

- Análise automática dos nomes das subpastas de um diretório.
- Sugestão inteligente de nomes e sobrenomes corrigidos, com base em listas padrão.
- Correção automática de erros comuns de digitação (fuzzy matching).
- Aprendizado contínuo: nomes e sobrenomes não encontrados são adicionados automaticamente à base padrão.
- Interface gráfica intuitiva e responsiva (PySide6 com tema escuro).
- Visualização e atualização dos registros diretamente na interface.
- Adição manual de nomes/sobrenomes padrão.
- Migrações de banco de dados com Alembic.
- Compatível com Windows e fácil de empacotar como executável.

---

## Tecnologias Utilizadas

- Python 3.10+
- PySide6 — Interface gráfica baseada em Qt.
- SQLAlchemy — ORM para PostgreSQL.
- Alembic — Migrações e versionamento do banco de dados.
- RapidFuzz — Fuzzy matching para sugestões inteligentes.
- qdarkstyle — Tema escuro para aplicações Qt.
- PostgreSQL — Banco de dados relacional.
- psycopg2-binary — Driver de conexão Python/PostgreSQL.
- PyInstaller — (Opcional) Empacotamento para executável Windows.

---

## Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Crie e ative um ambiente virtual (opcional)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Exemplo de `requirements.txt`:
```
PySide6
SQLAlchemy
alembic
rapidfuzz
qdarkstyle
psycopg2-binary
```

### 4. Configure o banco de dados PostgreSQL

- Crie o banco:
  ```bash
  createdb nomes_pasta
  ```
- No arquivo `db/db.py`, ajuste a string de conexão conforme seu ambiente:
  ```python
  DATABASE_URL = "postgresql://usuario:senha@localhost:5432/nomes_pasta?client_encoding=utf8"
  ```
  Substitua `usuario` e `senha` pelos seus dados.

### 5. Migrações com Alembic

- Configure o arquivo `alembic.ini`:
  ```
  sqlalchemy.url = postgresql://usuario:senha@localhost:5432/nomes_pasta?client_encoding=utf8
  ```
- Para criar as tabelas/migrar:
  ```bash
  alembic upgrade head
  ```

---

## Como Usar

1. Execute o programa:
   ```bash
   python main.py
   ```
2. Na interface:
   - Clique em "Selecionar Pasta para Análise" para escolher um diretório e analisar os nomes das subpastas.
   - Veja as sugestões de correção na lista e na tabela.
   - Para adicionar manualmente um nome ou sobrenome padrão, clique em "Adicionar Nome/Sobrenome Padrão".

---

## Estrutura do Projeto

```
projeto-bancodedados/
│
├── db/
│   ├── db.py
│   └── models.py
├── alembic/
│   └── (scripts de migração)
├── icons/
│   ├── folder.png
│   └── add-user.png
├── main.py
├── requirements.txt
└── README.md
```

---

## Observações

- O banco de dados PostgreSQL deve estar rodando e acessível.
- Nomes e sobrenomes não encontrados na lista padrão são adicionados automaticamente para futuras correções.
- Para adicionar mais nomes/sobrenomes padrão, edite a função `inserir_nomes_e_sobrenomes_padrao_na_nomes_pasta()` em `main.py`.
- O Alembic permite evoluir o banco de dados sem perder dados já cadastrados.
- O sistema é facilmente adaptável para outros bancos suportados pelo SQLAlchemy.

---

## Gerando Executável para Windows

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Gere o executável:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --add-data "icons;icons" main.py
   ```
   O executável estará na pasta `dist/`.

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Contribuição

Sugestões, correções e melhorias são bem-vindas.  
Abra uma issue ou envie um pull request para contribuir com o projeto.
