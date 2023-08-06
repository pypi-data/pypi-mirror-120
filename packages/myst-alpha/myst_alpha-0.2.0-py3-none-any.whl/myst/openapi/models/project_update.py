from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model

from ..models.deploy_status import DeployStatus


class ProjectUpdate(base_model.BaseModel):
    """Schema for project update requests."""

    object_: Optional[Literal["Project"]] = Field(..., alias="object")
    uuid: Optional[str] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None
    organization: Optional[str] = None
    owner: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[str] = None
    deploy_status: Optional[DeployStatus] = None
