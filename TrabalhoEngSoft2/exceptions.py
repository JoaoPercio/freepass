class UsuarioException(Exception):
    ...

class UsuarioNotFoundError(UsuarioException):
    def __init__(self):
        self.status_code = 404
        self.detail = "PESSOA_NAO_ENCONTRADO"

class UsuarioAlreadyExistError(UsuarioException):
    def __init__(self):
        self.status_code = 409
        self.detail = "EMAIL_DUPLICADO"

class EnderecoException(Exception):
    ...

class EnderecoNotFoundError(EnderecoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "ENDERECO_NAO_ENCONTRADO"
