from fastapi import FastAPI
from .api import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Other app configurations and routes

@app.get("/")
async def root():
    return {"message": "Welcome to the moon API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)