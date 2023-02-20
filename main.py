from fastapi import FastAPI
from routes import routers
from pymongo import MongoClient
from dotenv import dotenv_values


config = dotenv_values(".env")

app = FastAPI(
    title="Api de Usuarios", description=" Esta Api Serve para: Cadastrar, Listar, Editar e Exclir usuários"
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(routers.router,  tags=["Usuarios"], prefix="/usuario")

