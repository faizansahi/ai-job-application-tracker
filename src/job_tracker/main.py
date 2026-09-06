import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .db import Base, engine, get_session
from .models import Application, Job
from .schemas import (
    ApplicationCreate,
    ApplicationPatch,
    ApplicationRead,
    JobCreate,
    JobRead,
    ResumeRequest,
)
from .services import analyze_match, stage_statistics

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="AI Job Application Tracker", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/jobs", response_model=JobRead, status_code=201)
def create_job(payload: JobCreate, db: Session = Depends(get_session)):
    row = Job(**payload.model_dump(mode="json"))
    db.add(row)
    db.commit()
    return row


@app.get("/jobs", response_model=list[JobRead])
def list_jobs(q: str | None = Query(None, max_length=100), db: Session = Depends(get_session)):
    stmt = select(Job).order_by(Job.created_at.desc())
    if q:
        stmt = stmt.where(
            or_(
                Job.title.ilike(f"%{q}%"),
                Job.company.ilike(f"%{q}%"),
                Job.description.ilike(f"%{q}%"),
            )
        )
    return db.scalars(stmt).all()


@app.put("/jobs/{job_id}", response_model=JobRead)
def update_job(job_id: int, payload: JobCreate, db: Session = Depends(get_session)):
    row = db.get(Job, job_id)
    if not row:
        raise HTTPException(404, "Job not found")
    for key, value in payload.model_dump(mode="json").items():
        setattr(row, key, value)
    db.commit()
    return row


@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_session)):
    row = db.get(Job, job_id)
    if not row:
        raise HTTPException(404, "Job not found")
    db.delete(row)
    db.commit()


@app.post("/resume/analyze")
def analyze_resume(payload: ResumeRequest, db: Session = Depends(get_session)):
    job = db.get(Job, payload.job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return analyze_match(payload.text, job.description)


@app.post("/applications", response_model=ApplicationRead, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_session)):
    if not db.get(Job, payload.job_id):
        raise HTTPException(404, "Job not found")
    if db.scalar(select(Application).where(Application.job_id == payload.job_id)):
        raise HTTPException(409, "Application already exists")
    row = Application(**payload.model_dump())
    db.add(row)
    db.commit()
    return row


@app.patch("/applications/{application_id}", response_model=ApplicationRead)
def patch_application(
    application_id: int, payload: ApplicationPatch, db: Session = Depends(get_session)
):
    row = db.get(Application, application_id)
    if not row:
        raise HTTPException(404, "Application not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(row, key, value)
    db.commit()
    return row


@app.get("/analytics")
def analytics(db: Session = Depends(get_session)):
    applications = db.scalars(select(Application)).all()
    scores = [a.match_score for a in applications if a.match_score is not None]
    return {
        "total_jobs": db.query(Job).count(),
        "total_applications": len(applications),
        "by_stage": stage_statistics([a.stage.value for a in applications]),
        "average_match_score": round(sum(scores) / len(scores), 1) if scores else None,
    }
