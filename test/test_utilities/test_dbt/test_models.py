"""
Validates the internal logic of the Manifest class.
"""

from dbt.artifacts.resources.types import NodeType
from dbt.contracts.results import RunStatus

from parsons.utilities.dbt.models import Manifest


def test_skips_filter_uses_resource_type(dbt_node_factory, mock_manifest_data):
    """
    Validate that the Manifest class uses dbt's 'resource_type' attribute to filter
    results, providing a more robust alternative to string-parsing node names.
    """
    model_node = dbt_node_factory(status=RunStatus.Skipped, name="my_model")
    model_node.node.resource_type = NodeType.Model

    test_node = dbt_node_factory(status=RunStatus.Skipped, name="my_test")
    test_node.node.resource_type = NodeType.Test

    dbt_obj = mock_manifest_data(results=[model_node, test_node])
    manifest = Manifest(command="run", dbt_manifest=dbt_obj)

    assert len(manifest.skips) == 1
    assert manifest.skips[0].node.resource_type == NodeType.Model
