from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, mapped_column

# --- Seção 1: Configuração da Conexão com o Banco de Dados ---
# Esta é a string de conexão para o seu banco de dados MySQL.
# Por favor, substitua 'user', 'password' e 'localhost:3306' pelos seus dados reais.
DATABASE_URL = "mysql+mysqlconnector://root:125213@127.0.0.1:3306/hackathon"

# O 'engine' é o ponto de partida do SQLAlchemy, ele gerencia a conexão com o banco de dados.
engine = create_engine(DATABASE_URL)

# `Base` é a classe base para todos os nossos modelos.
Base = declarative_base()

# --- Seção 2: Modelos (Classes que viram Tabelas) ---
# Cada classe abaixo se tornará uma tabela no seu banco de dados.

class Usuario(Base):
    """
    Modelo para a tabela 'usuarios'.
    Armazena dados de perfis de usuário.
    """
    __tablename__ = "usuarios"
    id_usuario = mapped_column(Integer, primary_key=True)
    cpf = mapped_column(String(11), nullable=False, unique=True)
    email = mapped_column(String(150), nullable=False, unique=True)
    senha = mapped_column(String(255), nullable=False)
    # Note que no SQLAlchemy não precisamos de uma coluna para data_criacao se usarmos o default no SQL
    nome = mapped_column(String(255))
    cargo = mapped_column(String(255))
    descricao_pessoal = mapped_column(Text)
    tipo_usuario = mapped_column(String(50))
    foto_perfil_url = mapped_column(String(255))
    google_id = mapped_column(String(255))
    apple_id = mapped_column(String(255))

    # Relacionamentos com outras tabelas
    habilidades = relationship("UsuarioHabilidade", back_populates="usuario")
    projetos_participados = relationship("ParticipanteProjeto", back_populates="usuario")
    links_externos = relationship("LinkExterno", back_populates="usuario")

class Habilidade(Base):
    """
    Modelo para a tabela 'habilidades'.
    Armazena uma lista de habilidades técnicas.
    """
    __tablename__ = "habilidades"
    id_habilidade = mapped_column(Integer, primary_key=True)
    nome_habilidade = mapped_column(String(255), nullable=False, unique=True)
    
    usuarios = relationship("UsuarioHabilidade", back_populates="habilidade")

class UsuarioHabilidade(Base):
    """
    Tabela de junção para conectar 'usuarios' e 'habilidades'.
    """
    __tablename__ = "usuario_habilidades"
    id = mapped_column(Integer, primary_key=True)
    id_usuario = mapped_column(ForeignKey("usuarios.id_usuario"))
    id_habilidade = mapped_column(ForeignKey("habilidades.id_habilidade"))
    
    usuario = relationship("Usuario", back_populates="habilidades")
    habilidade = relationship("Habilidade", back_populates="usuarios")

class CategoriaPortfolio(Base):
    """
    Modelo para a tabela 'categorias_portfolio'.
    Categoriza os projetos (ex: 'Designer', 'Dev').
    """
    __tablename__ = "categorias_portfolio"
    id_categoria = mapped_column(Integer, primary_key=True)
    nome_categoria = mapped_column(String(255), nullable=False, unique=True)
    
    projetos = relationship("Projeto", back_populates="categoria")

class Projeto(Base):
    """
    Modelo para a tabela 'projetos'.
    Armazena os detalhes de cada projeto.
    """
    __tablename__ = "projetos"
    id_projeto = mapped_column(Integer, primary_key=True)
    nome_projeto = mapped_column(String(255), nullable=False)
    descricao_projeto = mapped_column(Text)
    nicho = mapped_column(String(255))
    imagem_projeto_url = mapped_column(String(255))
    id_categoria = mapped_column(ForeignKey("categorias_portfolio.id_categoria"))
    
    categoria = relationship("CategoriaPortfolio", back_populates="projetos")
    participantes = relationship("ParticipanteProjeto", back_populates="projeto")

class ParticipanteProjeto(Base):
    """
    Tabela de junção para conectar 'usuarios' e 'projetos'.
    """
    __tablename__ = "participantes_projeto"
    id = mapped_column(Integer, primary_key=True)
    id_usuario = mapped_column(ForeignKey("usuarios.id_usuario"))
    id_projeto = mapped_column(ForeignKey("projetos.id_projeto"))
    
    usuario = relationship("Usuario", back_populates="projetos_participados")
    projeto = relationship("Projeto", back_populates="participantes")

class LinkExterno(Base):
    """
    Modelo para a tabela 'links_externos'.
    Links para GitHub, Behance, LinkedIn, etc.
    """
    __tablename__ = "links_externos"
    id_link = mapped_column(Integer, primary_key=True)
    id_usuario = mapped_column(ForeignKey("usuarios.id_usuario"))
    plataforma = mapped_column(String(255))
    url = mapped_column(String(255))
    
    usuario = relationship("Usuario", back_populates="links_externos")

class Feedback(Base):
    """
    Modelo para a tabela 'feedbacks'.
    Depoimentos de usuários.
    """
    __tablename__ = "feedbacks"
    id_feedback = mapped_column(Integer, primary_key=True)
    nome_autor = mapped_column(String(255), nullable=False)
    cargo_autor = mapped_column(String(255))
    depoimento = mapped_column(Text)
    estrelas = mapped_column(Integer)

# --- Seção 3: Funções Auxiliares ---
def get_db_session():
    """
    Esta função cria uma sessão de banco de dados para cada requisição.
    É uma boa prática para garantir que a conexão seja gerenciada corretamente.
    O 'yield' faz com que a sessão seja fechada automaticamente após o uso.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()