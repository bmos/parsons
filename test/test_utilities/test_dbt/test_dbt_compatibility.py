"""
End-to-end compatibility tests between Parsons and dbt-core.

These tests use concrete dbt-core dataclasses (ExecutionResult, NodeResult)
to ensure that the Parsons Manifest wrapper remains compatible with dbt's
internal API. If dbt-core renames attributes or changes Enum behaviors,
these tests serve as an early warning system.
"""

from dbt.artifacts.resources.types import NodeType
from dbt.contracts.results import NodeStatus

from parsons.utilities.dbt.models import Manifest


def test_dbt_core_attribute_consistency(dbt_node_factory, mock_manifest_data):
    """
    Verify that the Manifest wrapper correctly calculates GB processed
    and summarizes run statuses from concrete dbt objects.
    """
    node = dbt_node_factory(status=NodeStatus.Success, bytes_processed=2 * 10**9)
    dbt_obj = mock_manifest_data(results=[node])
    manifest = Manifest(command="run", dbt_manifest=dbt_obj)

    assert manifest.total_gb_processed == 2.0
    assert manifest.summary["success"] == 1


def test_skips_filter_logic(dbt_node_factory, mock_manifest_data):
    """
    Ensure the 'skips' property accurately distinguishes between
    skipped models and skipped tests using dbt's native NodeType.
    """
    model_node = dbt_node_factory(
        status=NodeStatus.Skipped, name="my_model", resource_type=NodeType.Model
    )

    test_node = dbt_node_factory(
        status=NodeStatus.Skipped,
        name="some_test",
        resource_type=NodeType.Test,  # Manifest should filter this out
    )

    dbt_obj = mock_manifest_data(results=[model_node, test_node])
    manifest = Manifest(command="run", dbt_manifest=dbt_obj)

    assert len(manifest.skips) == 1
    assert manifest.skips[0].node.name == "my_model"
