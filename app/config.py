print(f"app/config.py package: {__package__}")

from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    secret_key: str #JWT
    algorithm: str
    access_token_expire_minutes: int


    class Config:
        env_file = ".env"


app_settings = Settings()

