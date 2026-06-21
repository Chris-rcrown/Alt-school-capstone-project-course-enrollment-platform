from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CourseBase(BaseModel):
    title: str
    code: str
    capacity: int = Field(..., gt=0)

    @field_validator("title", "code")
    def must_not_be_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator("title", "code", mode="before")
    def blank_to_none(cls, value):
        if value is None:
            return value
        value = value.strip()
        return value or None

    @field_validator("capacity")
    def capacity_must_be_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError("capacity must be greater than zero")
        return value


class CourseRead(CourseBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
