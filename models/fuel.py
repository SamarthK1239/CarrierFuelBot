from pydantic import BaseModel
from faunadb.objects import Ref
from fauna_easy.base_model import FaunaEasyBaseModel

# name, fuel_level, reserves, buy order

class FuelIn(BaseModel):
    name: str
    fuel_level: int
    reserves: float
    buy_order: int

class FuelDocument(BaseModel):
    ref: Ref
    data: FuelIn

    class Config:
        arbitrary_types_allowed = True

Fuel = FaunaEasyBaseModel('fuels', FuelIn)
