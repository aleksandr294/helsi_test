"""
Module for loading configuration settings from a .env file 
and defining the Config class.
The module uses the pydantic_settings and dotenv 
libraries to load settings from a .env file
and provide access to these settings as a Config object.
"""

import pydantic_settings
import dotenv

dotenv.load_dotenv()


class Config(pydantic_settings.BaseSettings):
    POSTGRES_URL: str
    BANK_URL: str


config = Config()  # type: ignore
