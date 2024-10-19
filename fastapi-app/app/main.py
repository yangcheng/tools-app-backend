from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth
from .core.config import Settings

settings = Settings()


app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Frontend URL from environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Other app configurations and routes

@app.get("/")
async def root():
    return {"message": "Welcome to the moon API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)