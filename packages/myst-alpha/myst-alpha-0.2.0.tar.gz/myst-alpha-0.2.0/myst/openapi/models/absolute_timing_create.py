from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model


class AbsoluteTimingCreate(base_model.BaseModel):
    """Absolute timing schema for create requests."""

    object_: Literal["Timing"] = Field(..., alias="object")
    type: Literal["AbsoluteTiming"]
    time: str
