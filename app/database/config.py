from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv
from pydantic import Field, validator

load_dotenv()

class DatabaseSettings(BaseSettings):
    # Database settings
    DB_HOST: str = Field(alias="DATABASE_HOST")
    DB_USER: str = Field(alias="DATABASE_USER")
    DB_PASSWORD: str = Field(alias="DATABASE_PASSWORD")
    DB_NAME: str = Field(alias="DATABASE_NAME")
    DB_PORT: int = Field(alias="DATABASE_PORT")
    
    @validator('DB_HOST')
    def validate_host(cls, v):
        if '172.31' in v:
            raise ValueError("Using internal AWS IP. Please use the public endpoint.")
        return v
    
    # AWS credentials
    aws_access_key_id: Optional[str] = Field(None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(None, alias="AWS_SECRET_ACCESS_KEY")
    
    # API settings
    upvote_api_key: Optional[str] = Field(None, alias="UPVOTE_API_KEY")
    bill_formatter_api_base_url: Optional[str] = Field(None, alias="BILL_FORMATTER_API_BASE_URL")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = DatabaseSettings()