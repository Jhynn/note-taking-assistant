from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Pydantic will automatically cast this string to an integer
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int

    HOST: str

    MODEL_PATH: str
    OLLAMA_BASE_URL: str
    LLM_MODEL: str

    # Configure Pydantic to read from a .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instantiate settings to be imported across your app
settings = Settings() # type: ignore
