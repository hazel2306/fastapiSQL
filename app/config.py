from pydantic_settings import BaseSettings, SettingsConfigDict
 
class Settings(BaseSettings):
    DTB_HOSTNAME: str
    DTB_PORT: str 
    DTB_PWD: str
    DTB_NAME: str
    DTB_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# print("ENV: DATABASE_URL =", os.getenv("DATABASE_URL"))  # will print None if not found
# print("SETTINGS:", Settings().model_dump())  # shows everything or throws

