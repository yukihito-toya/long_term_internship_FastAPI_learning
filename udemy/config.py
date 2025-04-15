from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  SECRET_KEY: str
  SQLALCHEMY_DATABASE_URI: str

  model_config = SettingsConfigDict(
    env_file = ".env",
    env_file_encoding = "utf-8",
  )

def get_settings() -> Settings:
  return Settings()