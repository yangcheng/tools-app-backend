from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    BASE_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5173"
    RESET_PASSWORD_URL: str = "{base_url}/auth/reset-password"

    @property
    def formatted_reset_password_url(self):
        return self.RESET_PASSWORD_URL.format(base_url=self.BASE_URL)

    class Config:
        env_file = ".env"

settings = Settings()
