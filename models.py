"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Model for creating a new task."""
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"  # BUG: No validation for allowed values


class TaskUpdate(BaseModel):
    """Model for updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None  # BUG: No validation for allowed statuses


class TaskResponse(BaseModel):
    """Model for task response."""
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    slug: str
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
