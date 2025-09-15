# API FastAPI - Hackathon

Este projeto é uma API desenvolvida em Python utilizando FastAPI e SQLAlchemy, conectada a um banco de dados MySQL. O objetivo é fornecer uma base para cadastro, autenticação e gerenciamento de usuários e projetos para um hackathon.


## Pré-requisitos

- Python 3.10 ou superior
- MySQL Server instalado e rodando
- Git instalado

## Passo a passo para rodar o projeto

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd banco_de_dados
```


### 2. Crie e ative o ambiente virtual Python

No terminal, dentro da pasta do projeto, execute:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

- **No Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **No Linux/Mac:**
  ```bash
  source .venv/bin/activate
  ```


### 3. Instale as dependências do projeto

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

Se aparecer erro relacionado ao email-validator, instale manualmente:
```bash
pip install email-validator
```



### 4. Configure o banco de dados MySQL

Abra o MySQL e execute:

```sql
CREATE DATABASE hackathon;
USE hackathon;
```

As tabelas serão criadas automaticamente ao rodar a aplicação pela primeira vez, conforme os modelos definidos em `models.py`.

#### Atenção: configure corretamente o usuário e a senha do seu banco de dados

No início do arquivo `models.py`, existe uma linha semelhante a:

```
DATABASE_URL = "mysql+mysqlconnector://usuario:senha@127.0.0.1:3306/hackathon"
```

Substitua `usuario` e `senha` pelos dados do seu MySQL local. Por exemplo, se seu usuário for `root` e sua senha for `minhasenha123`, a linha ficará assim:

```
DATABASE_URL = "mysql+mysqlconnector://root:minhasenha123@127.0.0.1:3306/hackathon"
```

Se você não souber sua senha, verifique na instalação do MySQL ou peça ao administrador do banco. Cada ambiente pode ter um usuário e senha diferentes!



### 5. Rode a aplicação

Com o ambiente virtual ativado, execute:

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

- `main.py`: inicialização da API, eventos e inclusão das rotas
- `models.py`: modelos do banco de dados e funções auxiliares
- `auth_routes.py`: rotas de autenticação e manipulação de usuários
- `requirements.txt`: dependências do projeto
- `.gitignore`: arquivos e pastas ignorados pelo Git


## Observações importantes

- **Nunca suba arquivos sensíveis** (como .env, senhas, etc) para o repositório. O arquivo `.gitignore` já está configurado para evitar isso.
- Para produção, utilize variáveis de ambiente para credenciais.
- Sempre ative o ambiente virtual antes de rodar qualquer comando Python.
- Contribuições são bem-vindas!

---

Desenvolvido para fins educacionais e de colaboração em hackathons.
