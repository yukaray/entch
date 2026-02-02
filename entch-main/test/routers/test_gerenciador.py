from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timedelta

client = TestClient(app)

# --- USUÁRIO --- #
"""def test_get_usuario():
    response = client.get("/auth/eu")
    assert response.status_code == 200

    # Apenas verifica se há usuários e campos essenciais
    usuarios = response.json()
    assert isinstance(usuarios, list)
    for u in usuarios:
        assert "id" in u and isinstance(u["id"], int)
        assert "nome" in u
        assert "email" in u
        assert "data_criacao" in u """

def test_post_usuario():
    novo_usuario = {
        "nome": "yuka",
        "email": f"yuka{datetime.now().timestamp()}@gmail.com",
        "senha": "cavalo"
    }
    response = client.post("/auth/cadastrar", json=novo_usuario)
    print(response.json())  # Mostra detalhes do erro
    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["nome"] == "yuka"
    assert data["email"].startswith("yuka")
    assert "senha" not in data
    assert "data_criacao" in data

# --- TAREFAS --- #
def test_get_tarefas():
    response = client.get("/tarefas/",params={"id_user":1})
    assert response.status_code == 200

    tarefas = response.json()
    assert isinstance(tarefas, list)
    for t in tarefas:
        assert "id" in t and isinstance(t["id"], int)
        assert "titulo" in t
        assert "id_usuario" in t
        assert "data_criacao" in t
        assert "data_att" in t

def test_post_tarefas():
    # Primeiro cria um usuário para associar a tarefa
    usuario = {
        "nome": f"teste_usuario_{datetime.now().timestamp()}",
        "email": f"teste{datetime.now().timestamp()}@gmail.com",
        "senha": "123456"
    }
    res_user = client.post("/auth/cadastrar", json=usuario)
    assert res_user.status_code == 201
    user_data = res_user.json()

    # Cria a tarefa
    nova_tarefa =   {
            "titulo": "estudar",
            "descricao": "estudar fastapi",
            "data_vencimento": 2
        }

    nova_tarefa2 = {
            "titulo": "correr",
            "descricao": "correr da policia",
            "data_vencimento": 4
        }
    
    response = client.post(f"/tarefas/?id_user={user_data['id']}", json=nova_tarefa)
    response = client.post(f"/tarefas/?id_user={user_data['id']}", json=nova_tarefa2)
    assert response.status_code == 201

    res1 = client.post(f"/tarefas/?id_user={user_data['id']}", json=nova_tarefa)
    assert res1.status_code == 201
    tarefa1 = res1.json()
    assert tarefa1["titulo"] == "estudar"

    res2 = client.post(f"/tarefas/?id_user={user_data['id']}", json=nova_tarefa2)
    assert res2.status_code == 201
    tarefa2 = res2.json()
    assert tarefa2["titulo"] == "correr"
