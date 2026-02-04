"""
Tests for dbt report formatting and logging.

This module ensures that the dbtLoggerMarkdown accurately translates dbt execution
results into user-friendly Markdown. It specifically validates the mapping
between dbt Status Enums (Success, Fail, Error, Warn, Skip) and their
corresponding visual indicators (emojis).
"""

import pytest
from dbt.contracts.results import RunStatus, TestStatus

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
            (RunStatus.Success, "\U0001f7e2"),  # Green: Model/Seed/Snapshot worked
            (RunStatus.Error, "\U0001f534"),  # Red: Model/Seed/Snapshot crashed
            (TestStatus.Fail, "\U0001f534"),  # Red: A dbt test failed
            (RunStatus.Skipped, "\U0001f535"),  # Blue: Node was skipped
            (TestStatus.Warn, "\U0001f7e0"),  # Orange: Test passed with warning
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
