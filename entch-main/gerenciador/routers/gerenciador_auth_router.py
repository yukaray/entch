from fastapi import APIRouter,Depends,HTTPException,Header
from pydantic import BaseModel,constr,ConfigDict
from typing import List
from datetime import datetime,timedelta,timezone
from env import CHAVE_SECRETA,ALGORITMO,TEMPO_EXP
from sqlalchemy.orm import Session
from dbApi.models import registros
from dbApi.dependencies import get_db
from jose import jwt,JWTError
from passlib.hash import pbkdf2_sha256
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


router_Auth = APIRouter(prefix="/auth",tags=['Auth'])

def criar_token(id_usuario):
    tempo_expirar = datetime.now(timezone.utc)+timedelta(TEMPO_EXP)
    dic_info = {"sub": str(id_usuario), "exp": tempo_expirar}
    token = jwt.encode(dic_info,CHAVE_SECRETA,ALGORITMO)
    return token

def autenticar(email,senha,sessao):
    usuario = sessao.query(registros).filter(
        registros.email == email
    ).first()
   
    if usuario and pbkdf2_sha256.verify(senha, usuario.senha_hash):
        return usuario
        
    return False

def obter_usuario_do_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        usuario_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(registros).filter(registros.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


class MostrarUsuarios(BaseModel):
    id: int
    nome: str
    email: str
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)

class CriarUsuarios(BaseModel):
    nome: str
    email: str
    senha: constr(min_length=6, max_length=72)


class TokenUsuario(BaseModel):
    access_token: str
    token_type: str

class LoginUsuario(BaseModel):
    email: str
    senha: str




@router_Auth.get("/me", response_model=MostrarUsuarios)
def me(usuario = Depends(obter_usuario_do_token)):
    return usuario




@router_Auth.post("/login", response_model=TokenUsuario)
def entrar(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario_autenticado = autenticar(
        form_data.username,
        form_data.password,
        db
    )

    if not usuario_autenticado:
        raise HTTPException(status_code=401, detail="Credenciais Inválidas")

    token_acesso = criar_token(usuario_autenticado.id)

    return {
        "access_token": token_acesso,
        "token_type": "bearer"
    }





@router_Auth.post("/cadastrar", response_model=MostrarUsuarios, status_code=201)
def Cadastrar_Usuario(usuario: CriarUsuarios, db: Session=Depends(get_db)) -> MostrarUsuarios:
    
    existing_user = db.query(registros).filter(registros.email == usuario.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    usuario_dict = usuario.model_dump()
    senha = usuario_dict.pop("senha")  
    usuario_dict.update({
        "senha_hash": pbkdf2_sha256.hash(senha),
        "data_criacao": datetime.now(timezone.utc)  
    })

    novo_usuario = registros(
        **usuario_dict
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return MostrarUsuarios(
        id=novo_usuario.id,
        nome=novo_usuario.nome,
        email=novo_usuario.email,
        data_criacao=novo_usuario.data_criacao
    )