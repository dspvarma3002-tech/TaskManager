from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from itertools import count

_id_counter = count(1)

class Task(BaseModel):
    id: int = Field(
        default_factory=lambda: next(_id_counter),
        json_schema_extra={"readOnly": True}
    )
    title: str
    description : str
    completed : bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        json_schema_extra={"readOnly": True}
    )

    @field_validator("title", "description")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty or whitespace")
        return v.strip()

    @field_validator("id", mode="before")
    @classmethod
    def force_server_id(cls, v):
        return next(_id_counter)

    @field_validator("created_at", mode="before")
    @classmethod
    def force_server_created_at(cls, v):
        return datetime.now(timezone.utc)