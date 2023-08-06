from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model

from ..models.deploy_status import DeployStatus


class ProjectGet(base_model.BaseModel):
    """Schema for project get responses."""

    object_: Literal["Project"] = Field(..., alias="object")
    uuid: str
    create_time: str
    organization: str
    owner: str
    title: str
    creator: str
    deploy_status: DeployStatus
    update_time: Optional[str] = None
    description: Optional[str] = None
