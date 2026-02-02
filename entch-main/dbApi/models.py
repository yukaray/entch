from sqlalchemy import Integer, String, DateTime, Date, Column, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from dbApi.database import Base

class registros(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String, index=True)
    data_criacao = Column(DateTime,default=lambda:datetime.now(timezone.utc))

    tarefas = relationship(
        "tarefas",
        back_populates="usuario",
        cascade="all, delete"
    )
    
class tarefas(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String, index=True)
    descricao = Column(String, nullable=True,index=True)
    data_vencimento = Column(Date, nullable=True)
    data_criacao = Column(DateTime,default=lambda:datetime.now(timezone.utc))
    data_att = Column(DateTime,default=lambda:datetime.now(timezone.utc))
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship(
        "registros",
        back_populates="tarefas" ,
        cascade="all, delete"
    )
    
