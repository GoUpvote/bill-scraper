from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import billbook

app = FastAPI(title="Bill Scraper API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(billbook.router, prefix="/api/v1", tags=["billbook"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)