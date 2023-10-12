from pydantic_settings import BaseSettings, SettingsConfigDict, DotEnvSettingsSource
from pydantic import Field
from dotenv import dotenv_values

config = dotenv_values(".env")

class MongoSetting():
    mongo_uri = config.get("MONGO_URI")
    mongo_db = config.get("MONGO_DB")


mongo_setting = MongoSetting()