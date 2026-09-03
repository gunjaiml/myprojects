from pydantic import BaseModel

class OrderRequest(BaseModel):
    user_id:str
    symbol:str
    action:str
    quantity:int
    price:float