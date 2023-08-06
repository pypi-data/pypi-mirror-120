from typing import Any, List, Optional, Union

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model


class InputCreate(base_model.BaseModel):
    """Schema for input create requests."""

    object_: Literal["Edge"] = Field(..., alias="object")
    type: Literal["Input"]
    upstream_node: str
    group_name: str
    output_index: Optional[int] = 0
    label_indexer: Optional[Union[List[Union[int, str, List[Any]]], List[Any], int, str]] = None
