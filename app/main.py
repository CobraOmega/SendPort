from fastapi import FastAPI
from .routes import router
from .config import settings

app = FastAPI(title="Email Microservice")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=int(settings.APP_PORT), reload=True)