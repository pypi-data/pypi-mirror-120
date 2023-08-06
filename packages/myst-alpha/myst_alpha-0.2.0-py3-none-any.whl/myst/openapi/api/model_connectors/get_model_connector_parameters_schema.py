from myst.client import Client

from ...models.model_connector_parameters_schema_get import ModelConnectorParametersSchemaGet


def request_sync(client: Client, uuid: str) -> ModelConnectorParametersSchemaGet:
    """Gets a model connector's parameters schema."""

    return client.request(
        method="get",
        path=f"/model_connectors/{uuid}:get_parameters_schema",
        response_class=ModelConnectorParametersSchemaGet,
    )
