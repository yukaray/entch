from sqlalchemy import Integer, String, Datetime, Date, Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class registro(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String, unique=True, index=True)
    created_at = Column(Datetime)

    tarefas = relationship(
        "tarefas",
        back_populates="usuario",
        cascade="all, delete"
    )
    
class tarefas(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, index=True)
    data_vencimento = Column(Date)
    data_criacao = Column(Datetime)
    data_conclusao = Column(Datetime)
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship(
        "registro",
        back_populates="tarefas" 
    )
    
