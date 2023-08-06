from timeslime.model import Setting
from timeslime.handler import DatabaseHandler

class SettingsHandler():
    def __init__(self, database_handler: DatabaseHandler):
        self.database_handler = database_handler

    def set(self, key: str, value: str):
        setting = Setting()
        setting.key = key
        setting.value = value
        self.database_handler.save_setting(setting)

    def get(self, key: str) -> Setting:
        return self.database_handler.read_setting(key)

    def delete(self, key: str):
        return self.database_handler.delete_setting(key)

    def contains(self, key: str) -> bool:
        try:
            self.database_handler.read_setting(key)
            return True
        except KeyError:
            return False