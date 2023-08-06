from typing import TYPE_CHECKING, Optional

from myst.adapters.timing import to_timing_create
from myst.client import get_client
from myst.models.timing import Timing
from myst.models.types import ItemOrSlice
from myst.openapi.api.time_series import create_time_series_layer
from myst.openapi.models.layer_create import LayerCreate
from myst.resources.edge import Edge
from myst.resources.node import Node

if TYPE_CHECKING:  # Avoid circular imports.
    from myst.resources.time_series import TimeSeries


class Layer(Edge):
    """An edge into a time series.

    Layers are a way of stitching together data from multiple upstream nodes into a single, cohesive time series. Data
    can be combined across different time ranges, and a time series can use data from a lower-precedence layer when
    data is missing from a higher-precedence layer.

    Attributes:
        order: integer specifying priority of this layer when combining multiple layers; lower order implies higher
            precedence
    """

    order: int

    @classmethod
    def create(
        cls,
        downstream_node: "TimeSeries",
        upstream_node: Node,
        order: int,
        output_index: int = 0,
        label_indexer: Optional[ItemOrSlice] = None,
        start_timing: Optional[Timing] = None,
        end_timing: Optional[Timing] = None,
    ) -> "Layer":
        layer = create_time_series_layer.request_sync(
            client=get_client(),
            time_series_uuid=str(downstream_node.uuid),
            json_body=LayerCreate(
                object="Edge",
                type="Layer",
                upstream_node=str(upstream_node.uuid),
                order=order,
                output_index=output_index,
                label_indexer=label_indexer,
                start_timing=to_timing_create(start_timing),
                end_timing=to_timing_create(end_timing),
            ),
        )

        return Layer.parse_obj(layer.dict())
