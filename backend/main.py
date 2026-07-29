from fastapi import FastAPI

from app.routes.subjects import router as subjects_router


app = FastAPI()
app.include_router(subjects_router, prefix="/subjects", tags=["subjects"])

@app.get("/")
def root():
    return "Tutaj pojawi sie menu glowne"
