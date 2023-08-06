from typing import Optional, Union

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model

from ..models.absolute_timing_create import AbsoluteTimingCreate
from ..models.relative_timing_create import RelativeTimingCreate


class TimeSeriesRunPolicyCreate(base_model.BaseModel):
    """Schema for time series run policy create requests."""

    object_: Literal["Policy"] = Field(..., alias="object")
    type: Literal["TimeSeriesRunPolicy"]
    schedule_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    start_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    end_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    active: Optional[bool] = True
