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

    @pytest.mark.parametrize(
        ("statuses", "expected_overall_icon", "expected_overall_text"),
        [
            ([NodeStatus.Success, NodeStatus.Success], "\U0001f7e2", "succeeded"),
            ([NodeStatus.Success, NodeStatus.Fail], "\U0001f534", "failed"),
            ([NodeStatus.Error, NodeStatus.Warn], "\U0001f534", "failed"),
            ([NodeStatus.Warn, NodeStatus.Success], "\U0001f7e0", "succeeded with warnings"),
            ([NodeStatus.Skipped, NodeStatus.Success], "\U0001f535", "skipped"),
            ([NodeStatus.Fail, NodeStatus.Skipped], "\U0001f534", "failed"),
        ],
    )
    def test_format_result_prioritization(
        self,
        statuses,
        expected_overall_icon,
        expected_overall_text,
        dbt_node_factory,
        mock_manifest_data,
    ):
        """
        Verify that format_result aggregates multiple commands and chooses
        the correct overall 'worst-case' status for the header.
        """
        manifests = []
        for i, status in enumerate(statuses):
            node = dbt_node_factory(status=status)
            data = mock_manifest_data(results=[node])
            data.metadata.elapsed_time = 10.0
            manifests.append(Manifest(command=f"cmd_{i}", dbt_manifest=data))

        logger = ConcreteMarkdownLogger()
        logger.commands = manifests

        output = logger.format_result()

        # Check the header (the first line of the output)
        header = output.split("\n")[0]
        assert expected_overall_icon in header
        assert expected_overall_text in header

        # Verify duration summed correctly (10s * number of statuses)
        expected_duration = f"{int(10 * len(statuses))} seconds"
        assert expected_duration in output
