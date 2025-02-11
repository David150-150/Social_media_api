
# Import BaseSettings from pydantic_settings to handle environment variables
from pydantic_settings import BaseSettings

# Define a Settings class that extends BaseSettings to load configuration from environment variables
class Settings(BaseSettings):
    database_hostname: str  # Database server hostname (e.g., localhost or IP address)
    database_port: str  # Port number for database connection (e.g., 5432 for PostgreSQL)
    database_password: str  # Password for the database user
    database_name: str  # Name of the database to connect to
    database_username: str  # Username for database authentication
    secret_key: str  # Secret key used for signing JWT tokens
    algorithm: str  # Algorithm used for token encryption (e.g., "HS256")
    access_token_expire_minutes: int = 30  # Token expiration time in minutes (default: 30)

    # Configuration class to specify that environment variables should be loaded from a .env file
    class Config:
        env_file = ".env"  # Specifies that the values should be loaded from a .env file

# Create an instance of the Settings class, which automatically loads values from the .env file
settings = Settings()


