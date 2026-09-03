from langgraph.graph import StateGraph,START,END
from app.graph.state import TradingState
from app.graph.nodes import (market_data_node,analyze_market_node,human_approval_node,approval_router,execute_trade_node)



def build_graph(checkpointer):
    builder = StateGraph(TradingState)

    builder.add_node("market_data",market_data_node)
    builder.add_node("analyze_market",analyze_market_node)
    builder.add_node("human_approval",human_approval_node)
    builder.add_node("execute_trade",execute_trade_node)

    builder.add_edge(START,"market_data")
    builder.add_edge("market_data","analyze_market")
    builder.add_edge("analyze_market","human_approval")
    builder.add_conditional_edges("human_approval",approval_router,{"execute_trade":"execute_trade","end":END})
    builder.add_edge("execute_trade",END)

    return builder.compile(
        checkpointer=checkpointer
    )

