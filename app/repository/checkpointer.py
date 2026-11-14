"""Memória de CURTO prazo: o checkpointer do LangGraph."""
from langgraph.checkpoint.mongodb import MongoDBSaver

from app.config.settings import settings
from app.repository import mongo


def criar_checkpointer() -> MongoDBSaver:
    return MongoDBSaver(mongo.cliente(), db_name=settings.mongo_banco)