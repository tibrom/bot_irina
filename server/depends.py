from fastapi import Depends, HTTPException, status

from .repositories import MainRepository
from db.base import database

def get_main_reposytory() -> MainRepository:
    return MainRepository(database)