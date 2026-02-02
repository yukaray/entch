from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,ConfigDict
from typing import List,Optional
from datetime import datetime,timedelta,date, timezone
from sqlalchemy.orm import Session
from dbApi.dependencies import get_db
from dbApi.models import tarefas
from .gerenciador_auth_router import obter_usuario_do_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

routerT = APIRouter(prefix="/tarefas",tags=['Tarefas'])

class MostrarTarefas(BaseModel):
    id: int
    id_usuario: int
    titulo: str
    descricao: Optional[str]=None
    data_vencimento: Optional[date]=None
    data_criacao: datetime
    data_att: datetime

    model_config = ConfigDict(from_attributes=True)

class CriarTarefas(BaseModel):
    titulo: str
    descricao: Optional[str]=None
    data_vencimento:  Optional[int]=None

class AtualizarTarefa(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    data_vencimento: Optional[int]

    


@routerT.get("/", response_model=List[MostrarTarefas], status_code=200)
def listar_Tarefas(usuario = Depends(obter_usuario_do_token),db: Session=Depends(get_db)) -> List[MostrarTarefas]:
    return db.query(tarefas).filter(tarefas.id_usuario == usuario.id).all()

@routerT.get("/{id}", response_model=MostrarTarefas, status_code=200)
def tarefa_unica(id:int,  usuario = Depends(obter_usuario_do_token), db: Session=Depends(get_db)) -> MostrarTarefas:
    tarefa = db.query(tarefas).filter(tarefas.id_usuario == usuario.id , tarefas.id == id).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return tarefa




@routerT.post("/", response_model=MostrarTarefas, status_code=201)
def Cadastrar_Tarefas(Tarefa: CriarTarefas,
    usuario = Depends(obter_usuario_do_token),
    db: Session=Depends(get_db)) -> MostrarTarefas:
    
    data_criacao = datetime.now(timezone.utc)

    data_vencimento = (
        data_criacao + timedelta(days=Tarefa.data_vencimento)
        if Tarefa.data_vencimento is not None
        else None
    )
        
    tarefa_dict = Tarefa.model_dump()
    tarefa_dict.update({
        "id_usuario": usuario.id,
        "data_vencimento": data_vencimento
    })

    nova_tarefa =  tarefas(**tarefa_dict)
    

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    
    return nova_tarefa




@routerT.api_route("/{id}", methods=["PUT", "PATCH"], status_code=200)
def atualizar_tarefa( id: int,
    usuario = Depends(obter_usuario_do_token),
    titulo: str | None = None,
    descricao: str | None = None,
    data_vencimento: int| None=None,
    db: Session=Depends(get_db)) -> MostrarTarefas:

    tarefa_db = db.query(tarefas).filter(tarefas.id == id, tarefas.id_usuario == usuario.id).first()
    if not tarefa_db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    if titulo is not None:
        tarefa_db.titulo = titulo
    if descricao is not None:
        tarefa_db.descricao = descricao
    if data_vencimento is not None:
        tarefa_db.data_vencimento = date.today()+timedelta(days=data_vencimento)

    tarefa_db.data_att = datetime.now(timezone.utc)

    db.commit()
    db.refresh(tarefa_db)
    
    return tarefa_db