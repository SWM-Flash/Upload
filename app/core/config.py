from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_base_url: str
    token_validation_url: str
    s3_presigned_url: str
    transcode_url: str
    environment: str = "dev"
    aws_api_base_url: str

    class Config:
        env_file = "env.list"

settings = Settings()
