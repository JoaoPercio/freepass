from sqlalchemy.orm import Session
from exceptions import UsuarioNotFoundError,UsuarioAlreadyExistError
import bcrypt, models, schemas

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações do servidor SMTP do Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'jp.percito@gmail.com'
sender_password = 'slkbtiuhroxfsowy'

#usuario

def check_administrador(db: Session, administrador: schemas.AdministradorLoginSchema):
    db_administrador = db.query(models.Administrador).filter(models.Administrador.email == administrador.email).first()
    if db_administrador is None:
        return False
    return bcrypt.checkpw(administrador.senha.encode('utf8'), db_administrador.senha.encode('utf8'))

def get_administrador_by_email(db: Session, administrador_email: str):
    return db.query(models.Administrador).filter(models.Administrador.email == administrador_email).first()

def create_administrador(db: Session, administrador: schemas.AdministradorCreate):
    db_administrador = get_administrador_by_email(db, administrador.email)
    # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
    administrador.senha = bcrypt.hashpw(administrador.senha.encode('utf8'), bcrypt.gensalt())
    if db_administrador is not None:
        raise UsuarioAlreadyExistError
    db_administrador = models.Administrador(**administrador.dict())
    db.add(db_administrador)
    db.commit()
    db.refresh(db_administrador)
    return db_administrador


def get_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).get(usuario_id)
    if db_usuario is None:
        raise UsuarioNotFoundError
    return db_usuario

def get_all_usuarios(db: Session, offset: int, limit: int):
    return db.query(models.Usuario).filter(models.Usuario.status == 1).offset(offset).limit(limit).all()

def get_all_usuarios_passe(db: Session, offset: int, limit: int):
    return db.query(models.Usuario).filter(models.Usuario.status == 3).offset(offset).limit(limit).all()

def delete_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db.delete(db_usuario)
    db.commit()
    # Crie uma mensagem MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = db_usuario.email
    msg['Subject'] = 'Cadastro Reprovado'
    
    # Corpo do email
    body = "a algum erro no seu cadastro para o passe livre, faça o cadastro novamente assim que possivel."
    msg.attach(MIMEText(body, 'plain'))

    # Inicie uma conexão com o servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Inicie a criptografia TLS

    # Faça login na conta
    server.login(sender_email, sender_password)

    # Envie o email
    text = msg.as_string()
    server.sendmail(sender_email, db_usuario.email, text)

    # Encerre a conexão
    server.quit()
    return

def update_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db_usuario.status = 2
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_all_documentos(db: Session,usuario_id:int, offset: int, limit: int):
    db_usuario =get_usuario_by_id(db, usuario_id) 
    if(db_usuario.status==1):
        print("passo aqui")
        return db.query(models.Documento).filter(models.Documento.id_usuario == usuario_id).filter(models.Documento.passe == False).offset(offset).limit(limit).all()
    else:
        print("passo aqui 2")
        return db.query(models.Documento).filter(models.Documento.id_usuario == usuario_id).filter(models.Documento.passe == True).offset(offset).limit(limit).all()

def create_documento(db: Session, usuario: schemas.DocumentoCreate):
    db_documento = models.Documento(**usuario.dict())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

def create_registro(db: Session, registro: schemas.RegistroCreate):
    db_registro = models.Registro(**registro.dict())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro

def create_endereco(db: Session, registro: schemas.EnderecoCreate):
    db_endereco = models.Endereco(**registro.dict())
    db.add(db_endereco)
    db.commit()
    db.refresh(db_endereco)
    return db_endereco