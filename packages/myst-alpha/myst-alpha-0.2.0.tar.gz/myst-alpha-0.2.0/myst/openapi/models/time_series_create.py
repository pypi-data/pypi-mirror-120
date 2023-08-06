from typing import Any, List, Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model


class TimeSeriesCreate(base_model.BaseModel):
    """Schema for time series create requests."""

    object_: Literal["Node"] = Field(..., alias="object")
    title: str
    project: str
    sample_period: str
    cell_shape: List[Any]
    coordinate_labels: List[Any]
    axis_labels: List[Any]
    type: Optional[Literal["TimeSeries"]] = None
    description: Optional[str] = None
