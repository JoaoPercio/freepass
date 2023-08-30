from datetime import date
from typing import List  
from pydantic import BaseModel

class AdministradorBase(BaseModel):
    email: str   
class AdministradorCreate(AdministradorBase):
    senha: str
class Administrador(AdministradorBase):
    id: int
    class Config:
        orm_mode = True
class AdministradorLoginSchema(BaseModel):
    email: str
    senha: str
    class Config:
        schema_extra = {
            "example": {
                "email": "x@x.com",
                "senha": "pass"
            }
        }
class PaginatedAdministrador(BaseModel):
    limit: int
    offset: int
    data: List[Administrador]
class EnderecoBase(BaseModel):
    cep: str
    estado: str
    cidade: str
    bairro: str
    logradouro: str
    complemento: str
    id_registro: int
class EnderecoCreate(EnderecoBase):
    pass
class Endereco(EnderecoBase):
    id: int
    class Config:
        orm_mode = True
class PaginatedEndereco(BaseModel):
    limit: int
    offset: int
    data: List[Endereco]

class RegistroBase(BaseModel):
    data_registro: date
    local_moradia: str
    categoria : bool
    motociclista: bool
class RegistroCreate(RegistroBase):
    pass
class Registro(RegistroBase):
    id: int
    endereco: Endereco = {}
    class Config:
        orm_mode = True

class PaginatedRegistro(BaseModel):
    limit: int
    offset: int
    data: List[Registro]

class UsuarioBase(BaseModel):
    nome_completo: str
    telefone: str
    email: str
    senha: str
    cpf: str
    status: str
    quantidade_passe_total: int
    id_registro: int
class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    registro2: Registro ={}
    class Config:
        orm_mode = True
class PaginatedUsuario(BaseModel):
    limit: int
    offset: int
    data: List[Usuario]

class DocumentoBase(BaseModel):
    id_usuario: int
    id_registro: int
    nome : str
    url : str
    passe : bool
class DocumentoCreate(DocumentoBase):
    pass
class Documento(DocumentoBase):
    id: int
    class Config:
        orm_mode = True
class PaginatedDocumento(BaseModel):
    limit: int
    offset: int
    data: List[Documento]

