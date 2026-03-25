from fastapi import FastAPI

from api import api_router


app = FastAPI(title="GC-Proctor API", version="1.0.0")
app.include_router(api_router, prefix="/api")


@app.get("/")
def health_check() -> dict[str, str]:
	return {"message": "GC-Proctor API is running"}
