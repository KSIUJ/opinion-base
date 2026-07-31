from fastapi import FastAPI

from app.routes.subjects import router as subjects_router
from app.routes.lecturers import router as lecturers_router


app = FastAPI()
app.include_router(subjects_router, prefix="/subjects", tags=["subjects"])
app.include_router(lecturers_router, prefix="/lecturers", tags=["lecturers"])

@app.get("/")
def root():
    return "Tutaj pojawi sie menu glowne"
