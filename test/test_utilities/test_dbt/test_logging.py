"""
Tests for dbt report formatting and logging.

This module ensures that the dbtLoggerMarkdown accurately translates dbt execution
results into user-friendly Markdown. It specifically validates the mapping
between dbt Status Enums (Success, Fail, Error, Warn, Skip) and their
corresponding visual indicators (emojis).
"""

import pytest
from dbt.contracts.results import NodeStatus

from parsons.utilities.dbt.logging import dbtLoggerMarkdown
from parsons.utilities.dbt.models import Manifest


class ConcreteMarkdownLogger(dbtLoggerMarkdown):
    def send(self, manifests):
        pass


class TestLoggers:
    """Tests for dbtLoggerMarkdown and its subclasses."""

    @pytest.mark.parametrize(
        ("dbt_status", "icon"),
        [
            (NodeStatus.Success, "\U0001f7e2"),  # Green: Model/Seed/Snapshot worked
            (NodeStatus.Error, "\U0001f534"),  # Red: Model/Seed/Snapshot crashed
            (NodeStatus.Fail, "\U0001f534"),  # Red: A dbt test failed
            (NodeStatus.Skipped, "\U0001f535"),  # Blue: Node was skipped
            (NodeStatus.Warn, "\U0001f7e0"),  # Orange: Test passed with warning
        ],
    )
    def test_markdown_formatting(self, dbt_status, icon, dbt_node_factory, mock_manifest_data):
        """
        Verify that each possible dbt outcome produces the correct visual icon
        and status text in the Markdown header.
        """
        node = dbt_node_factory(status=dbt_status)
        dbt_m = mock_manifest_data(results=[node])

        manifest = Manifest(command="run", dbt_manifest=dbt_m)

        logger = ConcreteMarkdownLogger()
        output = logger.format_command_result(manifest)

        assert icon in output

    def test_format_result_aggregation(self, dbt_node_factory, mock_manifest_data):
        """
        Verify that format_result aggregates multiple commands and chooses
        the correct overall status.
        """
        success_node = dbt_node_factory(status=NodeStatus.Success)
        fail_node = dbt_node_factory(status=NodeStatus.Fail)

        m1_data = mock_manifest_data(results=[success_node])
        m1_data.metadata.elapsed_time = 10.5

        m2_data = mock_manifest_data(results=[fail_node])
        m2_data.metadata.elapsed_time = 20.0

        manifest_success = Manifest(command="run", dbt_manifest=m1_data)
        manifest_fail = Manifest(command="test", dbt_manifest=m2_data)

        logger = ConcreteMarkdownLogger()
        logger.commands = [manifest_success, manifest_fail]

        output = logger.format_result()

        assert "\U0001f534" in output
        assert "dbt run failed" in output

        assert "30 seconds" in output

        assert "Invoke dbt with `dbt run`" in output
        assert "Invoke dbt with `dbt test`" in output
