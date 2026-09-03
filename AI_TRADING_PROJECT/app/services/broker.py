import uuid
from app.schemas.order_schema import OrderRequest
def execute_trade(order:OrderRequest):
    order_id = str(uuid.uuid4())
    print("EXECUTE :" , order)
    return {
        "message":(f"OrderID: #{order_id}: Trade executed: {order['action']} {order['quantity']} shares of {order['symbol']}")
    }