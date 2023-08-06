from typing import Any, Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model


class SourceCreate(base_model.BaseModel):
    """Schema for source create requests."""

    object_: Literal["Node"] = Field(..., alias="object")
    type: Literal["Source"]
    title: str
    project: str
    connector_uuid: str
    description: Optional[str] = None
    parameters: Optional[Any] = None
