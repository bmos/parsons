"""
Pytest configuration and shared fixtures for dbt integration.

These fixtures utilize real dbt-core dataclasses (NodeResult, ExecutionResult)
to ensure the Parsons utility remains compatible with dbt's internal API and Enum structures.
"""

from datetime import datetime
from unittest.mock import MagicMock

import pytest
from dbt.artifacts.resources.types import NodeType
from dbt.contracts.graph.manifest import ManifestMetadata
from dbt.contracts.results import ExecutionResult, NodeResult, RunStatus


@pytest.fixture
def dbt_node_factory():
    """
    Return a factory function to create dbt NodeResult objects.

    Uses dbt.contracts.results.NodeResult and dbt.artifacts.resources.types.NodeType.
    The inner 'node' is mocked to simplify setup, but the result container remains a concrete dbt object.
    """

    def _create_node(
        status=RunStatus.Success, name="my_model", resource_type=NodeType.Model, bytes_processed=0
    ):
        mock_node = MagicMock()
        mock_node.name = name
        mock_node.resource_type = resource_type

        return NodeResult(
            status=status,
            timing=[],
            thread_id="thread-1",
            execution_time=1.0,
            adapter_response={"bytes_processed": bytes_processed, "slot_ms": 3600000},
            message="Success",
            failures=None,
            node=mock_node,
        )

    return _create_node


@pytest.fixture
def mock_manifest_data():
    """
    Return a factory to create a dbt ExecutionResult with attached metadata.

    Since ExecutionResult does not natively store metadata in its constructor,
    this fixture manually attaches ManifestMetadata to the object. This
    simulates the structure expected by the Manifest proxy wrapper.
    """

    def _create(results=None):
        res = ExecutionResult(
            results=results or [],
            elapsed_time=10.0,
        )

        res.metadata = ManifestMetadata(
            generated_at=datetime.strptime("2026-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            project_id="parsons_project",
            adapter_type="bigquery",
        )

        return res

    return _create
