"""Ensure the `dbtRunnerParsons` wrapper correctly interfaces with the `dbt-core` Python API."""

from unittest.mock import Mock, patch

from parsons.utilities.dbt.dbt import dbtRunnerParsons


@patch("parsons.utilities.dbt.dbt.dbtRunner")
def test_execute_strips_prefix_and_adds_dir(mock_runner_class, tmp_path):
    """Test that execute_dbt_command properly cleans CLI strings and injects the project directory."""
    mock_runner_inst = mock_runner_class.return_value
    mock_runner_inst.invoke.return_value = Mock(result=Mock(), exception=None)

    runner = dbtRunnerParsons(commands="dbt run", dbt_project_directory=tmp_path)
    runner.execute_dbt_command("dbt run")

    args = mock_runner_inst.invoke.call_args[0][0]
    assert "dbt" not in args
    assert "run" in args
    assert "--project-dir" in args
    assert str(tmp_path) in args
