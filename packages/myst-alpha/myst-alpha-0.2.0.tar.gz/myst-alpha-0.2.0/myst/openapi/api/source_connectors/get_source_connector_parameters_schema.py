from myst.client import Client

from ...models.source_connector_parameters_schema_get import SourceConnectorParametersSchemaGet


def request_sync(client: Client, uuid: str) -> SourceConnectorParametersSchemaGet:
    """Gets a source connector's parameters schema."""

    return client.request(
        method="get",
        path=f"/source_connectors/{uuid}:get_parameters_schema",
        response_class=SourceConnectorParametersSchemaGet,
    )
