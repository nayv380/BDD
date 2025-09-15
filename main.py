from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from models import Base, engine, Usuario, get_db_session
from auth_routes import router as auth_router

# Criamos a nossa aplicação FastAPI.
app = FastAPI()

# Incluímos o roteador de autenticação
app.include_router(auth_router)

# --- Seção 1: Schemas do Pydantic para Atualização ---
# Este schema define quais campos podem ser atualizados.
# Usamos 'Optional' para indicar que nenhum campo é obrigatório na requisição de atualização.

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None
    descricao_pessoal: Optional[str] = None
    tipo_usuario: Optional[str] = None
    foto_perfil_url: Optional[str] = None
    empresa: Optional[str] = None
    localizacao: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[str] = None

# --- Seção 2: Eventos de Inicialização ---

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

# --- Seção 3: Rotas (Endpoints) da API ---

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

@app.put("/usuarios/{user_id}")
def update_usuario(user_id: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_db_session)):
    """
    Rota para atualizar os dados de um usuário existente.
    
    - Recebe o ID do usuário na URL e os dados a serem atualizados no corpo da requisição.
    - Se o usuário não for encontrado, retorna um erro 404.
    - Se o usuário for encontrado, atualiza apenas os campos fornecidos.
    """
    # 1. Busca o usuário no banco de dados
    usuario_existente = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    
    if usuario_existente is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 2. Itera sobre os dados recebidos e atualiza o usuário no banco
    for campo, valor in usuario_data.dict(exclude_unset=True).items():
        setattr(usuario_existente, campo, valor)
    
    # 3. Salva as mudanças no banco de dados
    db.commit()
    db.refresh(usuario_existente)
    
    return {"message": "Usuário atualizado com sucesso!", "usuario_atualizado": usuario_existente}

@app.delete("/usuarios/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(user_id: int, db: Session = Depends(get_db_session)):
    """
    Rota para excluir um usuário por ID.
    
    - Recebe o ID do usuário na URL.
    - Se o usuário não for encontrado, retorna um erro 404.
    - Se for encontrado, o exclui do banco de dados.
    """
    # 1. Busca o usuário para deletar
    usuario_a_deletar = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    
    if usuario_a_deletar is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # 2. Deleta o usuário do banco
    db.delete(usuario_a_deletar)
    db.commit()
    
    # Retorna uma resposta de sucesso sem conteúdo
    return {"message": "Usuário deletado com sucesso!"}