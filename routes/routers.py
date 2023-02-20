from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import UsuarioUpdate, Usuario

router = APIRouter()


@router.post("/", response_description="Usuario criado", status_code=status.HTTP_201_CREATED, response_model=Usuario)
def cria_usuario(request: Request, usuario: Usuario = Body(...)): 
    usuario = jsonable_encoder(usuario)

    if (Usuario := request.app.database["usuario"].find_one({"cpf": usuario["cpf"]})):
           
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cpf cadastrado")
        
    novo_usuario = request.app.database["usuario"].insert_one(usuario)
    cria_usuario = request.app.database["usuario"].find_one(
        {"_id": novo_usuario.inserted_id}
    )
    
    return cria_usuario
    

@router.get("/", response_description="Lista todos os usuários", response_model=List[Usuario])
def listar_usuarios(request: Request):
    usuarios = list(request.app.database["usuario"].find(limit=10))
    return usuarios

@router.get("/{id}", response_description="Busca usuário por ID", response_model=Usuario)
def usuario_id(id: str, request: Request):
    if (Usuario := request.app.database["usuario"].find_one({"_id": id})) is not None:
        return Usuario
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario com ID {id} não localizado")


@router.put("/{id}", response_description="Atualiza o Usuário", response_model=Usuario)
def atualiza_usuario(id: str, request: Request, usuario: UsuarioUpdate = Body(...)):
    usuario = {k: v for k, v in usuario.dict().items() if v is not None}
    if len(usuario) >= 1:
        resultado = request.app.database["usuario"].update_one(
            {"_id": id}, {"$set": usuario}
        )
    if resultado.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"usuario com  {id} não localizado")
    if (
        usuario_existente := request.app.database["usuario"].find_one({"_id": id})
    ) is not None:
        return usuario_existente
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"usuario com {id} não localizado")


@router.delete("/{id}", response_description="Usuario Deletado")
def delete_usuario(id: str, request: Request, response: Response):
    delete_result = request.app.database["usuario"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"usuario com {id} não localizado")

