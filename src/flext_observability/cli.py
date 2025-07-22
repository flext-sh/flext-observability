"""CLI interface for flext-infrastructure.monitoring.flext-observability.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import sys

import typer
from flext_core import MetricType
from rich.console import Console
from rich.table import Table

from flext_observability import __version__
from flext_observability.config import get_settings
from flext_observability.simple_api import (
    collect_metric,
    get_system_overview,
    register_observability_services,
)

app = typer.Typer(
    name="flext-infrastructure.monitoring.flext-observability",
    help="FLEXT Observability CLI - Enterprise monitoring and observability",
)
console = Console()


@app.command()
def setup(
    metrics: bool = typer.Option(True, help="Enable metrics collection"),
    alerts: bool = typer.Option(True, help="Enable alerting"),
    health: bool = typer.Option(True, help="Enable health checks"),
    logging: bool = typer.Option(True, help="Enable structured logging"),
    tracing: bool = typer.Option(True, help="Enable distributed tracing"),
) -> None:
    try:
        register_observability_services(
            enable_metrics=metrics,
            enable_alerts=alerts,
            enable_health_checks=health,
            enable_logging=logging,
            enable_tracing=tracing,
        )
        console.print(
            "✅ Observability services initialized successfully",
            style="green",
        )
    except Exception as e:
        console.print(f"❌ Failed to setup observability {e}", style="red")
        sys.exit(1)


@app.command()
def status() -> None:
    try:
        overview = get_system_overview()

        # Create status table
        table = Table(title="System Overview")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Status", overview["status"])
        table.add_row("Components", str(overview["components"]))
        table.add_row("Active Alerts", str(overview["active_alerts"]))
        table.add_row("Recent Errors", str(overview["recent_errors"]))
        table.add_row("Active Traces", str(overview["active_traces"]))

        console.print(table)
    except Exception as e:
        console.print(f"❌ Failed to get system status {e}", style="red")
        sys.exit(1)


@app.command()
def collect(
    name: str = typer.Argument(..., help="Metric name"),
    value: float = typer.Argument(..., help="Metric value"),
    unit: str = typer.Option("count", help="Metric unit"),
    metric_type: str = typer.Option(
        "gauge",
        help="Metric type (counter, gauge, histogram, summary)",
    ),
    component: str = typer.Option("cli", help="Component name"),
    namespace: str = typer.Option("default", help="Component namespace"),
) -> None:
    try:
        try:
            mt = MetricType(metric_type.lower())
        except ValueError:
            console.print(f"❌ Invalid metric type: {metric_type}", style="red")
            console.print(
                "Valid types: counter, gauge, histogram, summary, business",
                style="yellow",
            )
            sys.exit(1)

        success = collect_metric(
            name=name,
            value=value,
            unit=unit,
            metric_type=mt,
            component_name=component,
            component_namespace=namespace,
        )

        if success:
            console.print(f"✅ Metric {name} collected successfully", style="green")
        else:
            console.print(f"❌ Failed to collect metric {name}", style="red")
            sys.exit(1)
    except Exception as e:
        console.print(f"❌ Failed to collect metric: {e}", style="red")
        sys.exit(1)


@app.command()
def config() -> None:
    try:
        settings = get_settings()
        config_dict = settings.model_dump()

        console.print("Current Configuration", style="bold cyan")
        console.print(json.dumps(config_dict, indent=2, default=str))
    except Exception as e:
        console.print(f"❌ Failed to get configuration: {e}", style="red")
        sys.exit(1)


@app.command()
def version() -> None:
    """Show version information."""
    console.print(
        f"flext-infrastructure.monitoring.flext-observability version: {__version__}",
        style="green",
    )

    # Show settings version
    settings = get_settings()
    console.print(f"Project version: {settings.project_version}", style="blue")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
