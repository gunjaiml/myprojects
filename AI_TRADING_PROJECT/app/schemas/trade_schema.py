from pydantic import BaseModel
from typing import Literal

class TradeRequest(BaseModel):
    user_id:str
    symbol:str
    quantity:int
    action:Literal["BUY","SELL"]