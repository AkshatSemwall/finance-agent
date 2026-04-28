from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent import FinanceAgent
from app.config import settings
from app.memory.manager import MemoryManager
from app.memory.json_memory import JsonLongTermMemory
from app.sources.csv_importer import CsvImporter
from app.routers.chat import router as chat_router
from app.routers.memory import router as memory_router
from app.routers.sync import router as sync_router
from app.routers.transactions import router as transactions_router
from app.routers.insights import router as insights_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize components
    long_term_memory = JsonLongTermMemory()
    memory_manager = MemoryManager(long_term_memory)
    csv_importer = CsvImporter()
    agent = FinanceAgent(memory_manager, settings)
    
    app.state.agent = agent
    app.state.csv_importer = csv_importer
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(memory_router)
app.include_router(sync_router)
app.include_router(transactions_router)
app.include_router(insights_router)




