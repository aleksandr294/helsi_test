
import pydantic_settings
import dotenv

dotenv.load_dotenv()


class Config(pydantic_settings.BaseSettings):
    postgres_url: str



def get_config() -> Config:
    return Config()
