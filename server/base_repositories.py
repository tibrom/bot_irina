from db.base import Database

class BaseRepository:
    def __init__(self, database: Database) -> None:
        self.database = database