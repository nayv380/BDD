from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, engine, Usuario, get_db_session
from auth_routes import router as auth_router

# Criamos a nossa aplicação FastAPI.
app = FastAPI()

# Incluímos o roteador de autenticação
app.include_router(auth_router)

# --- Seção 1: Eventos de Inicialização ---

@app.on_event("startup")
def startup_event():
    """
    Esta função é executada uma única vez quando a sua API começa a rodar.
    Ela garante que todas as tabelas, que definimos no 'models.py', sejam criadas
    no banco de dados se elas ainda não existirem.
    """
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

# --- Seção 2: Rotas (Endpoints) da API ---

@app.get("/")
def read_root():
    """
    Rota de boas-vindas. Serve para testar se o servidor está funcionando.
    Você pode acessá-la em http://127.0.0.1:8000/
    """
    return {"message": "Bem-vindo à API Infinity School!"}

@app.get("/usuarios/")
def get_all_usuarios(db: Session = Depends(get_db_session)):
    """
    Nova rota para buscar todos os usuários cadastrados.
    """
    # Consulta o banco de dados para encontrar todos os usuários.
    usuarios = db.query(Usuario).all()
    
    # Retorna a lista de usuários encontrada.
    return usuarios

@app.get("/usuarios/{user_id}")
def get_usuario(user_id: int, db: Session = Depends(get_db_session)):
    """
    Rota para buscar um usuário por ID.
    """
    # Consulta o banco de dados para encontrar o usuário com o ID fornecido.
    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    
    # Se o usuário não for encontrado, retornamos um erro 404.
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Se encontrado, retornamos os dados do usuário.
    return usuario