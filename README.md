# API FastAPI - Hackathon

Este projeto é uma API desenvolvida em Python utilizando FastAPI e SQLAlchemy, conectada a um banco de dados MySQL. O objetivo é fornecer uma base para cadastro, autenticação e gerenciamento de usuários e projetos para um hackathon.

## Pré-requisitos

- Python 3.10+
- MySQL Server
- Git

## Passo a passo para rodar o projeto

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd banco_de_dados
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
# Ative no Windows:
.venv\Scripts\activate
# Ou no Linux/Mac:
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados MySQL

- Crie o banco de dados e as tabelas (exemplo):

```sql
CREATE DATABASE hackathon;
USE hackathon;

CREATE TABLE usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  cpf VARCHAR(11) NOT NULL UNIQUE,
  email VARCHAR(150) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

- Ajuste a string de conexão em `models.py` se necessário:

```
DATABASE_URL = "mysql+mysqlconnector://usuario:senha@127.0.0.1:3306/hackathon"
```


### 5. Rode a aplicação

```bash
uvicorn main:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Como fazer login por CPF

Para autenticar um usuário, utilize a rota POST `/login` enviando um JSON com o CPF e a senha:

Exemplo de requisição:

```
POST /login
Content-Type: application/json

{
  "cpf": "12345678900",
  "senha": "sua_senha"
}
```

Se o CPF e a senha estiverem corretos, a resposta será:

```
{
  "message": "Login realizado com sucesso",
  "usuario_id": 1
}
```

Se estiverem incorretos, será retornado erro 401.

## Estrutura dos arquivos principais

- `main.py`: inicialização da API e inclusão das rotas
- `models.py`: modelos do banco de dados e funções auxiliares
- `auth_routes.py`: rotas de autenticação e manipulação de usuários
- `requirements.txt`: dependências do projeto
- `.gitignore`: arquivos e pastas ignorados pelo Git

## Observações importantes

- **Nunca suba arquivos sensíveis** (como .env, senhas, etc) para o repositório. O arquivo `.gitignore` já está configurado para evitar isso.
- Para produção, utilize variáveis de ambiente para credenciais.
- Contribuições são bem-vindas!

---

Desenvolvido para fins educacionais e de colaboração em hackathons.
