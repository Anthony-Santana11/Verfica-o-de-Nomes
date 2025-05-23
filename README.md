# Validador de Nomes de Pastas

Este projeto é uma aplicação desktop em Python para **análise, sugestão e padronização de nomes de pastas** com base em listas de nomes e sobrenomes padrão, utilizando interface gráfica (PySide6), banco de dados relacional (SQLAlchemy/SQLite) e fuzzy matching (RapidFuzz).

---

## Funcionalidades

- Seleção de uma pasta para análise automática dos nomes das subpastas.
- Sugestão automática de nomes e sobrenomes corrigidos, conforme listas padrão.
- Correção automática de erros comuns de digitação (fuzzy matching).
- Adição automática de nomes/sobrenomes não encontrados à lista padrão.
- Interface visual moderna com tema escuro.
- Visualização e atualização dos registros no banco de dados.
- Adição manual de nomes/sobrenomes padrão pela interface.
- Migrações de banco de dados utilizando **Alembic**.

---

## Tecnologias Utilizadas

- **Python 3.10+**
- **PySide6**  
  Interface gráfica moderna baseada em Qt.
- **SQLAlchemy**  
  ORM para manipulação do banco de dados relacional (SQLite por padrão).
- **Alembic**  
  Ferramenta para controle de versões e migrações do banco de dados.
- **RapidFuzz**  
  Biblioteca para fuzzy matching (correção de nomes/sobrenomes com erros de digitação).
- **qdarkstyle**  
  Tema escuro para aplicações Qt.
- **SQLite**  
  Banco de dados local, leve e fácil de distribuir.
- **PyInstaller**  
  (Opcional) Para empacotar o programa como executável (.exe) para Windows.

---

## Instalação

1. **Clone o repositório:**
   ```
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```

   Exemplo de `requirements.txt`:
   ```
   PySide6
   SQLAlchemy
   alembic
   rapidfuzz
   qdarkstyle
   ```

---

## Migrações de Banco de Dados (Alembic)

O projeto utiliza o **Alembic** para versionamento e migração do banco de dados.  
Para criar ou atualizar o banco:

1. **Inicialize o Alembic (se ainda não existir):**
   ```
   alembic init alembic
   ```

2. **Crie uma nova revisão de migração:**
   ```
   alembic revision --autogenerate -m "Descrição da mudança"
   ```

3. **Aplicar as migrações:**
   ```
   alembic upgrade head
   ```

O arquivo de conexão do banco deve estar configurado em `alembic.ini` (exemplo para SQLite):
```
sqlalchemy.url = sqlite:///./nomes.db
```

---

## Como Usar

1. **Execute o programa:**
   ```
   python main.py
   ```

2. **Na interface:**
   - Clique em **Selecionar Pasta para Análise** para escolher uma pasta e analisar os nomes das subpastas.
   - Veja as sugestões de correção na lista e na tabela.
   - Para adicionar manualmente um nome ou sobrenome padrão, clique em **Adicionar Nome/Sobrenome Padrão**.

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

## Gerando Executável (.exe)

1. Instale o PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Gere o executável:
   ```
   pyinstaller --noconfirm --onefile --windowed --add-data "icons;icons" main.py
   ```
   O executável estará na pasta `dist/`.

---

## Observações

- O banco de dados é criado automaticamente na primeira execução.
- Nomes e sobrenomes não encontrados na lista padrão são adicionados automaticamente para futuras correções.
- Para adicionar mais nomes/sobrenomes padrão, edite a função `inserir_nomes_e_sobrenomes_padrao_na_nomes_pasta()` em `main.py`.
- O Alembic permite evoluir o banco de dados sem perder dados já cadastrados.

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
