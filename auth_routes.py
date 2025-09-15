from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from models import Usuario, get_db_session

# Criamos um roteador para organizar as rotas de autenticação.
router = APIRouter(prefix="/auth", tags=["Autenticação"])

# --- Seção 1: Schemas do Pydantic ---
# Usamos Pydantic para validar os dados que chegam na API.
# Ele garante que as informações de registro do usuário estão corretas.

class UsuarioCreate(BaseModel):
    """
    Schema para criar um novo usuário.
    Define os campos obrigatórios e seus tipos.
    """
    cpf: str
    email: EmailStr
    senha: str
    nome: str
    cargo: str
    descricao_pessoal: str
    tipo_usuario: str
    foto_perfil_url: str = None
    empresa: str = None
    localizacao: str = None
    telefone: str = None
    data_nascimento: str = None # Usamos string para facilitar e convertemos depois se necessário

# --- Seção 2: Rotas (Endpoints) da API ---

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db_session)):
    """
    Rota para registrar um novo usuário no banco de dados.

    - Recebe os dados de registro.
    - Verifica se o CPF ou e-mail já existem para evitar duplicidade.
    - Se tudo estiver OK, cria o novo usuário e o salva no banco.
    """
    # 1. Verificamos se o usuário já existe
    usuario_existente = db.query(Usuario).filter(
        (Usuario.cpf == usuario_data.cpf) | (Usuario.email == usuario_data.email)
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="CPF ou e-mail já cadastrados."
        )

    # 2. Criamos uma nova instância do modelo de usuário
    novo_usuario = Usuario(
        cpf=usuario_data.cpf,
        email=usuario_data.email,
        senha=usuario_data.senha, # Em uma aplicação real, a senha deveria ser hasheada aqui!
        nome=usuario_data.nome,
        cargo=usuario_data.cargo,
        descricao_pessoal=usuario_data.descricao_pessoal,
        tipo_usuario=usuario_data.tipo_usuario,
        foto_perfil_url=usuario_data.foto_perfil_url,
        empresa=usuario_data.empresa,
        localizacao=usuario_data.localizacao,
        telefone=usuario_data.telefone,
        data_nascimento=usuario_data.data_nascimento
    )

    # 3. Adicionamos o novo usuário à sessão do banco de dados e salvamos
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario) # Atualiza a instância com o ID gerado pelo banco

    return {"message": "Usuário registrado com sucesso!", "id_usuario": novo_usuario.id_usuario}
