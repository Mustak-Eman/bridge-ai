from fastapi import FastAPI

app = FastAPI(
    title="Bridge AI",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Bridge AI",
        "health": "/health",
        "docs": "/docs",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}