import config
import sqlite3

class DAO:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(config.DB_NAME)
        self.cursor = self.conn.cursor()

    def _get_table_name(self):
        raise NotImplementedError()

    def _store_sql(self):
        raise NotImplementedError()
    
    def _update_sql(self):
        raise NotImplementedError()

    def _data(self, obj):
        raise NotImplementedError()

    def create_table(self):
        raise NotImplementedError()

    def store(self, obj):
        self.cursor.execute(self._store_sql(), self._data(obj))
        self.conn.commit()
    
    def update(self, obj):
        self.cursor.execute(self._update_sql(), self._data(obj))
        self.conn.commit()

    def fetch_all(self):
        tname = self._get_table_name()
        entries = []
        for entry in self.cursor.execute(f"SELECT rowid, * FROM {tname}"):
            entries.append(entry)
        return entries

    def __del__(self) -> None:
        self.cursor.close()
        self.conn.close()