from fastapi import FastAPI
from app.api import app_router
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os
from app.graph.workflow import build_graph

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not in .env")


@asynccontextmanager
async def lifespan(app:FastAPI):
    
    with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
        checkpointer.setup()
        
        app.state.graph = build_graph(checkpointer)
        
        yield
        
        


app=FastAPI(
    title="AI Trading",
    lifespan=lifespan
)

app.include_router(app_router)

@app.get("/")
def root():
    return {
        "message":"AI Trading Project Setup"
    }