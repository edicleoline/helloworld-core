from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    __log__: bool = True