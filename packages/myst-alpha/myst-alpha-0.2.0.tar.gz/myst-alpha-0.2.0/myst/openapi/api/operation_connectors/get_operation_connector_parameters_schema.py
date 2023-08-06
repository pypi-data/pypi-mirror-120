from myst.client import Client

from ...models.operation_connector_parameters_schema_get import OperationConnectorParametersSchemaGet


def request_sync(client: Client, uuid: str) -> OperationConnectorParametersSchemaGet:
    """Gets an operation connector's parameters schema."""

    return client.request(
        method="get",
        path=f"/operation_connectors/{uuid}:get_parameters_schema",
        response_class=OperationConnectorParametersSchemaGet,
    )
