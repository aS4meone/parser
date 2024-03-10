from pydantic import BaseModel


class OrderSchema(BaseModel):
    name: str
    phone: str
    product: str
