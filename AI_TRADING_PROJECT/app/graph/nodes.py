from app.graph.state import TradingState
from app.services.market_data import get_market_data
from app.services.llm import llm
from langgraph.types import interrupt
from app.services.broker import execute_trade

def market_data_node(state:TradingState):
    symbol = state["symbol"]
    market_data = get_market_data(symbol)
    
    return {
        "market_data":market_data
    }
    
    
def analyze_market_node(state:TradingState):
    prompt = f"""
    You are analyzing a simulated trading request.
    
    User wants to:
    {state["action"]} {state['quantity']} shares of {state["symbol"]}
    
    Market data:
    {state["market_data"]}
    
    Analyze the supplied market data.
    
    
    Return:
    1. A concise analysis.
    2. Whether the proposed trade looks reasonable based only on the supplied data.
 
    Do not claim certainty and do not execute any trade.
    """
    
    response = llm.invoke(prompt)
    
    return {
        "analysis":response.content,
        "trade_proposal":{
            "symbol":state["symbol"],
            "action":state["action"],
            "quantity":state["quantity"],
            "analysis":response.content
        }
    }
    
    
def human_approval_node(state:TradingState):
    proposal = state["trade_proposal"]
    
    decision = interrupt({
        "type":"trade_proposal",
        "message":"Please review the trade proposal.",
        "proposal":proposal
    })
    
    return {
        "approved":decision["approved"]
    }


def approval_router(state:TradingState):
    
    print("STATE:", state)
    if state["approved"]:
        return "execute_trade"
    return "end"

def execute_trade_node(state:TradingState):
    market_data = state["market_data"]
    order ={
        "user_id":state["user_id"],
        "symbol":state["symbol"],
        "action":state["action"],
        "quantity":state["quantity"],
        "price":market_data["price"]
    }
    
    print(order)
    
    result = execute_trade(order)
    
    return {
        "execution_result":result
    }
    