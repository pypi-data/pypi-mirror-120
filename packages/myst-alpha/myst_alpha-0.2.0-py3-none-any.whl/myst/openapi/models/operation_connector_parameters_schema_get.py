from typing import Any, Dict

from myst.models import base_model


class OperationConnectorParametersSchemaGet(base_model.BaseModel):
    """Schema for operation connector parameters get responses."""

    __root__: Dict[str, Any]

    def __getitem__(self, item: str) -> Any:
        return self.__root__[item]
