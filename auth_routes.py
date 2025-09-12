
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Base, engine, Usuario, get_db_session
from pydantic import BaseModel
import hashlib

# Criação do roteador
router = APIRouter()

# Rota de login por CPF
class LoginRequest(BaseModel):
    cpf: str
    senha: str

@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest, db: Session = Depends(get_db_session)):
    usuario = db.query(Usuario).filter(Usuario.cpf == request.cpf).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="CPF ou senha inválidos")
    # Aqui você pode usar hash de senha real, este é só exemplo
    senha_hash = hashlib.sha256(request.senha.encode()).hexdigest()
    if usuario.senha != senha_hash:
        raise HTTPException(status_code=401, detail="CPF ou senha inválidos")
    return {"message": "Login realizado com sucesso", "usuario_id": usuario.id_usuario}


# --- Seção 1: Eventos de Inicialização ---
# (Esses eventos devem ser definidos no main.py, se necessário)


# --- Seção 2: Rotas (Endpoints) da API ---

@router.get("/usuarios/{user_id}")
def get_usuario(user_id: int, db: Session = Depends(get_db_session)):
    """
    Rota para buscar um usuário por ID.
    O 'Depends(get_db_session)' injeta a sessão do banco de dados na sua função.
    Isso é o que permite que você interaja com o banco.
    """
    # Consulta o banco de dados para encontrar o usuário com o ID fornecido.
    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    
    # Se o usuário não for encontrado, retornamos um erro 404.
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Se encontrado, retornamos os dados do usuário.
    return usuario