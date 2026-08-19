from fastapi import FastAPI
from backend.api.interview_routes import router
app = FastAPI(
    title="AI Interview Voice Agent",
    version="1.0.0"
)

app.include_router(router)
@app.get("/")
def home():
    return {"message": "AI Interview Voice Agent API"}

@app.get("/health")
def health():
    return {"status": "healthy"}
