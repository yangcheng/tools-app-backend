from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(request: SearchRequest):
    # This is a placeholder for the actual search logic
    return {"result": f"Search results for: {request.query}"}

@app.get("/")
async def root():
    return {"message": "Welcome to the search API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
