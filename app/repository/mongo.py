"""Conexão com o MongoDB (uma só para o projeto inteiro)."""
from functools import lru_cache

from pymongo import MongoClient
from pymongo.database import Database

from app.config.settings import settings


@lru_cache
def cliente() -> MongoClient:
    return MongoClient(settings.mongo_url, serverSelectionTimeoutMS=5000)


def banco() -> Database:
    return cliente()[settings.mongo_banco]