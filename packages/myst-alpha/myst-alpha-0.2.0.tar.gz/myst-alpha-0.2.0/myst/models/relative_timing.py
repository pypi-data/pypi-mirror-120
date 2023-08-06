from typing import Optional

from myst.core.time.time_delta import TimeDelta
from myst.models.timing import Timing


class RelativeTiming(Timing):
    frequency: Optional[TimeDelta] = None
    offset: Optional[TimeDelta] = None
    time_zone: str = "UTC"
