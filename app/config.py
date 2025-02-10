

from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     database_hostname:str
#     database_port:str
#     database_password:str
#     database_name:str  
#     database_username:str
#     secret_key:str
#     algorithm:str
#     access_token_expire_minutes:int  
    
#     class Config:
#         env_file = ".env"   

#         # Create the settings instance
# settings = Settings()
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str  
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30  # Default value in case the env variable is missing

    class Config:
        env_file = ".env"  # Load variables from .env file if available

settings = Settings()
