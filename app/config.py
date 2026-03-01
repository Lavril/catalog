from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = 'postgres'
    postgres_password: str = ""
    postgres_host: str = '127.0.0.1'
    postgres_port: int = 5432
    postgres_db: str = 'catalog'

    API_KEY: str = "supersecret"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )


settings = Settings()
