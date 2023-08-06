from typing import Any, Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model


class OperationCreate(base_model.BaseModel):
    """Schema for operation create requests."""

    object_: Literal["Node"] = Field(..., alias="object")
    type: Literal["Operation"]
    title: str
    project: str
    connector_uuid: str
    description: Optional[str] = None
    parameters: Optional[Any] = None
