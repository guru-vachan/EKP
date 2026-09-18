from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, EmailStr

class EmailRequest(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    recipient: EmailStr

    subject: str = Field(
        min_length=1,
        max_length=255
    )

    body: str = Field(
        min_length=1
    )


class EmailResult(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    recipient: EmailStr

    message_id: str | None = None