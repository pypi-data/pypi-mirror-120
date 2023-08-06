from pydantic import BaseModel


class Configuration(BaseModel):
    key: str
    language: str = 'en'
    text: str
