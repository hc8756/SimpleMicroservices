from __future__ import annotations

from typing import Optional, Annotated
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

EINType = Annotated[str, StringConstraints(pattern=r"^\d{2}-\d{7}$")]
class BusinessBase(BaseModel):
    ein: EINType = Field(
        ...,
        description="Tax identifier number unique to employers.",
        json_schema_extra={"example": "12-3456789"},
    )
    name: str = Field(
        ...,
        description="Name of business.",
        json_schema_extra={"example": "Ashley's Cupcakes"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "ashleyscupcakes@example.com"},
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example": "+1-212-555-0199"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ein": "12-3456789",
                    "name": "Ashley's Cupcakes",
                    "email": "ashleyscupcakes@example.com",
                    "phone": "+1-212-555-0199",
                }
            ]
        }
    }


class BusinessCreate(BusinessBase):
    """Creation payload for a Business."""
    pass


class BusinessUpdate(BaseModel):
    """Partial update for a Business; supply only fields to change."""
    ein: Optional[EINType] = Field(
        None, description="Business EIN.", json_schema_extra={"example": "12-3456789"}
    )
    name: Optional[str] = Field(None, json_schema_extra={"example": "Ashley's Cupcakes"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "ashleyscupcakes@example.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+1-212-555-0199"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Ashley's Bakery"},
                {"phone": "+1-415-555-0199"},
            ]
        }
    }


class BusinessRead(BusinessBase):
    """Server representation returned to clients."""
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ein": "12-3456789",
                    "name": "Ashley's Cupcakes",
                    "email": "ashleyscupcakes@example.com",
                    "phone": "+1-212-555-0199",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
