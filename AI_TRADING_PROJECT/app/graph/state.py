from typing import TypedDict

class TradingState(TypedDict,total=False):
    user_id:str
    symbol:str
    quantity:int
    action:str
    
    market_data:dict
    analysis:str
    trade_proposal:dict
    
    approved:bool
    
    execution_result:dict