from __future__ import annotations

from typing import Optional, List
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr

from .business import BusinessBase

class ProductBase(BaseModel):
    product_id: int = Field(
        ...,
        description="Unique integer identifying product",
        json_schema_extra={"example": 0},
    )
    name: str = Field(
        ...,
        description="Name of product.",
        json_schema_extra={"example": "Vanilla Cupcake"},
    )

    # Embed business with ein
    business: BusinessBase = Field(
        ...,
        description="Business that produces this product.",
        json_schema_extra={
            "example":{
                "ein": "12-3456789",
                "name": "Ashley's Cupcakes",
                "email": "ashleyscupcakes@example.com",
                "phone": "+1-212-555-0199",
            }
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_id": 0,
                    "name": "Vanilla Cupcake",
                    "business": {
                        "ein": "12-3456789",
                        "name": "Ashley's Cupcakes",
                        "email": "ashleyscupcakes@example.com",
                        "phone": "+1-212-555-0199",
                    },
                }
            ]
        }
    }


class ProductCreate(ProductBase):
    """Creation payload for a Product."""
    pass

class ProductUpdate(BaseModel):
    """Update for a Product."""
    product_id: Optional[int] = Field(
        None, description="Unique integer identifying product.", json_schema_extra={"example": 0}
    )
    name: Optional[str] = Field(None, description="Name of product.", json_schema_extra={"example": "Chocolate Cupcake"})
    business: Optional[BusinessBase] = Field(
        None,
        description="Replace the business creating product.",
        json_schema_extra={
            "example": {
                "ein": "12-3456789",
                "name": "Ashley's Cupcakes",
                "email": "ashleyscupcakes@example.com",
                "phone": "+1-212-555-0199",
            }
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_id": 0,
                    "name": "Chocolate Cupcake",
                    "business": {
                        "ein": "12-3456789",
                        "name": "Ashley's Cupcakes",
                        "email": "ashleyscupcakes@example.com",
                        "phone": "+1-212-555-0199",
                    },
                },
            ]
        }
    }


class ProductRead(ProductBase):
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
                    "product_id": 0,
                    "name": "Vanilla Cupcake",
                    "business": {
                        "ein": "12-3456789",
                        "name": "Ashley's Cupcakes",
                        "email": "ashleyscupcakes@example.com",
                        "phone": "+1-212-555-0199",
                    },
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
