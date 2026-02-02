import uvicorn
from fastapi import FastAPI
from gerenciador.routers.gerenciador_tarefas_router import routerT
from gerenciador.routers.gerenciador_auth_router import router_Auth
from dbApi.database import engine,Base
from dbApi.models import tarefas,registros

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home() ->str:
    return "api pancada"

app.include_router(router_Auth)
app.include_router(routerT)

