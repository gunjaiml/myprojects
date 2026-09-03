from fastapi import APIRouter,Request
from app.schemas.trade_schema import TradeRequest
from app.schemas.approval_schema import ApprovalRequest
import uuid
from langgraph.types import Command
router = APIRouter()


@router.post("")
def create_trade(request:TradeRequest,http_request:Request):
    
    trade_id = str(uuid.uuid4())
    initial_state = {
        "user_id":request.user_id,
        "symbol":request.symbol,
        "quantity":request.quantity,
        "action":request.action
    }
    
    config = {
        "configurable":{
            "thread_id":trade_id
        }
    }
    
    result = http_request.app.state.graph.invoke(initial_state,config)
    
    interrupt_data = result.get("__interrupt__")
    return {
        "trade_id":trade_id,
        "status":"WAITING_FOR_APPROVAL",
        "proposal":result.get("trade_proposal"),
        "interrupt":interrupt_data
    }
    
    
@router.post("/{trade_id}/approval")
def approve_trade(trade_id:str,request:ApprovalRequest,http_request:Request):
    
    config={
        "configurable":{
            "thread_id":trade_id
        }
    }
    
    result = http_request.app.state.graph.invoke(Command(resume={"approved":request.approved}),config)
    
    if request.approved:
        return {
            "trade_id":trade_id,
            "status":"APPROVED",
            "execution_result":result.get("execution_result")
        }
    return {
        "trade_id":trade_id,
        "status":"REJECTED",
        "message":"Trade is rejected by the user."
    }