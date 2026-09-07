from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .models import Stage


class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    company: str = Field(min_length=1, max_length=200)
    location: str = Field(default="", max_length=200)
    description: str = Field(min_length=20)
    source_url: HttpUrl | None = None


class JobRead(JobCreate):
    id: int
    created_at: datetime
    source_url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class ApplicationCreate(BaseModel):
    job_id: int
    stage: Stage = Stage.SAVED
    notes: str = Field(default="", max_length=5000)


class ApplicationPatch(BaseModel):
    match_score: float | None = Field(default=None, ge=0, le=100)
    stage: Stage | None = None
    notes: str | None = Field(default=None, max_length=5000)


class ApplicationRead(BaseModel):
    id: int
    job_id: int
    stage: Stage
    notes: str
    match_score: float | None
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResumeRequest(BaseModel):
    text: str = Field(min_length=20, max_length=200_000)
    job_id: int
