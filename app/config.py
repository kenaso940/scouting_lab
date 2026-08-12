from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: int = 5432
    database_password: str = ""
    database_name: str = "scouting_lab"
    database_username: str = "postgres"

    class Config:
        env_file = ".env"

settings = Settings()