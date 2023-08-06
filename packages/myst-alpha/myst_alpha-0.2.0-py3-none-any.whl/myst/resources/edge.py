from uuid import UUID

from myst.resources.resource import Resource


class Edge(Resource):
    """An edge between two nodes in a project graph.

    Attributes:
        upstream_node: the identifier of the node data flows into this edge from
        downstream_node: the identifier of the node data flows out of this edge to
    """

    upstream_node: UUID
    downstream_node: UUID
