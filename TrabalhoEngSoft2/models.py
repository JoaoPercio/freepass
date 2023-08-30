from sqlalchemy import Column, Integer, String, SmallInteger, Date, ForeignKey, Table, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class Administrador(Base):
    __tablename__ = "administrador"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(300))
    senha = Column(String(150))

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(300))
    telefone = Column(String(11))
    email = Column(String(100))
    senha = Column(String(150))
    cpf = Column(String(11))
    status = Column(SmallInteger)
    quantidade_passe_total = Column(Integer)
    documentos = relationship("Documento", uselist=False, back_populates="usuario", cascade="all, delete-orphan")
    registro2 = relationship("Registro", uselist=False, back_populates="usuario2")
    id_registro= Column(Integer, ForeignKey("registro.id"), nullable=False)

class Endereco(Base):
    __tablename__ = "endereco"

    id = Column(Integer, primary_key=True, index=True)
    cep = Column(String(9))
    estado = Column(String(100))
    cidade = Column(String(150))
    bairro = Column(String(150))
    logradouro = Column(String(150))
    complemento = Column(String(200))
    id_registro = Column(Integer, ForeignKey("registro.id"), nullable=False)

    registro = relationship("Registro", uselist=False, back_populates="endereco")

class Documento(Base):
    __tablename__ = "documento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(300))
    url = Column(String(2000))
    passe = Column(Boolean)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    id_registro = Column(Integer, ForeignKey("registro.id"), nullable=False)

    usuario = relationship("Usuario", uselist=False, back_populates="documentos")
    registro3 = relationship("Registro", uselist=False, back_populates="documentos2")

class Registro(Base):
    __tablename__ = "registro"

    id = Column(Integer, primary_key=True, index=True)
    data_registro = Column(TIMESTAMP)
    local_moradia = Column(String(2000))
    categoria = Column(Boolean)
    motociclista = Column(Boolean)

    endereco = relationship("Endereco", uselist=False, back_populates="registro")

    usuario2 = relationship("Usuario", uselist=False, back_populates="registro2")

    documentos2 = relationship("Documento", uselist=False, back_populates="registro3")
    
