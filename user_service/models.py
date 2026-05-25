from pydantic import BaseModel, Field, field_validator, EmailStr
from itertools import count
from datetime import datetime, timezone

_user_id_counter = count(1)

class User(BaseModel):
    id: int = Field(
        default_factory=lambda: next(_user_id_counter),
        json_schema_extra={"readOnly": True},
    )
    name: str = Field(min_length=1)
    email: EmailStr
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        json_schema_extra={"readOnly": True},
    )

    @field_validator("name")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty or whitespace")
        return v.strip()