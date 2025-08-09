from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data_loader import load_holdings, load_allocation

app = FastAPI(title="WealthManager Portfolio API")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; in production use your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/portfolio/holdings")
def get_holdings():
    return load_holdings()


@app.get("/api/portfolio/allocation")
def get_allocation():
    return load_allocation()