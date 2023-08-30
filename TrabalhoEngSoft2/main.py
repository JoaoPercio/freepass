from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from exceptions import UsuarioException
from database import get_db, engine
import crud, models, schemas
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# usuario
@app.get("/api/usuarios/{usuario_id}", response_model=schemas.Usuario)
def get_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/usuarios", response_model=schemas.PaginatedUsuario)
def get_all_usuarios(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_usuarios = crud.get_all_usuarios(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_usuarios}
    return response

@app.get("/api/usuarios/passe", response_model=schemas.PaginatedUsuario)
def get_all_usuarios_passe(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_usuarios = crud.get_all_usuarios_passe(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_usuarios}
    return response

@app.post("/api/usuarios", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_usuario(db, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/usuarios/{usuario_id}",response_model=schemas.Usuario)
def update_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.update_usuario(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)
    
@app.delete("/api/usuarios/{usuario_id}")
def delete_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/documentos/{usuario_id}", response_model=schemas.PaginatedDocumento)
def get_all_documentos(usuario_id=int, db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_documentos = crud.get_all_documentos(db, usuario_id, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_documentos}
    return response

@app.post("/api/documentos", response_model=schemas.Documento)
def create_documento(documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_documento(db, documento)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)
    
@app.post("/api/registros", response_model=schemas.Registro)
def create_registro(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_registro(db, registro)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)
    
@app.post("/api/enderecos", response_model=schemas.Endereco)
def create_endereco(endereco: schemas.EnderecoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_endereco(db, endereco)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)
    
#login

# signup
@app.post("/api/signup", tags=["usuario"])
async def create_usuario_signup(administrador: schemas.AdministradorCreate = Body(...), db: Session = Depends(get_db)):
    try:
        crud.create_administrador(db, administrador)
        return signJWT(administrador.email)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

# login
@app.post("/api/login", tags=["usuario"])
async def user_login(administrador: schemas.AdministradorLoginSchema = Body(...), db: Session = Depends(get_db)):
    if crud.check_administrador(db, administrador):
        return signJWT(administrador.email)
    raise HTTPException(status_code=400, detail="USUARIO_INCORRETO")