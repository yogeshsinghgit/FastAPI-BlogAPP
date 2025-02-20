# Description: This file contains the configuration settings for the FastAPI application. 
# It uses the pydantic_settings library to load the settings from environment variables or a .env file.

import os
from pydantic_settings import BaseSettings  
from pydantic import Field

class Settings(BaseSettings):
    # General settings
    APP_NAME: str = Field("My FastAPI Application", env="APP_NAME")
    APP_VERSION: str = Field("1.0.0", env="APP_VERSION")
    DEBUG: bool = Field(False, env="DEBUG")
    APP_DESCRIPTION: str = Field("A FastAPI application", env="APP_DESCRIPTION")

    # Database settings
    DATABASE_URL: str = Field(..., env="DATABASE_URL")  # MongoDB connection string
    DATABASE_NAME: str = Field("mydatabase", env="DATABASE_NAME")

    # Google OAuth2 settings
    GOOGLE_CLIENT_ID: str = Field(..., env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(..., env="GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = Field(..., env="GOOGLE_REDIRECT_URI")
    GOOGLE_AUTH_URL : str = Field(..., env="GOOGLE_AUTH_URL")
    GOOGLE_TOKEN_URL:str = Field(..., env="GOOGLE_TOKEN_URL")
    GOOGLE_USER_INFO_URL:str = Field(..., env="GOOGLE_USER_INFO_URL")


    # Security settings
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")

    # Auth settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

# Instantiate the settings object
def get_settings():
    return Settings()
