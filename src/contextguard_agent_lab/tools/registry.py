"""In-process tool boundary with MCP-compatible metadata."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable

from contextguard_agent_lab.benchmark.schema import ToolCallTrace

ToolFn = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(slots=True)
class ToolSpec:
    """Structured tool contract exported as the first MCP-compatible artifact."""

    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    risk_level: str = "low"
    side_effect: str = "none"
    cost_estimate: float = 1.0
    mcp_exposure: str = "manifest"

    def manifest_entry(self) -> dict[str, Any]:
        """Return a JSON-serializable manifest row."""

        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "risk_level": self.risk_level,
            "side_effect": self.side_effect,
            "cost_estimate": self.cost_estimate,
            "mcp_exposure": self.mcp_exposure,
        }


@dataclass(slots=True)
class RegisteredTool:
    """Tool function plus contract metadata."""

    fn: ToolFn
    spec: ToolSpec


@dataclass(slots=True)
class ToolResult:
    """Structured result returned by a registered tool."""

    tool_name: str
    arguments: dict[str, Any]
    payload: dict[str, Any]
    latency_ms: int = 0
    cost_proxy: float = 0.0
    context_chars: int = 0
    risk_level: str = "low"

    def trace(self, case_id: str, step_index: int) -> ToolCallTrace:
        """Convert the tool result into a benchmark trace row."""

        return ToolCallTrace(
            case_id=case_id,
            step_index=step_index,
            tool_name=self.tool_name,
            arguments=self.arguments,
            result=self.payload,
            latency_ms=self.latency_ms,
            cost_proxy=self.cost_proxy,
            context_chars=self.context_chars,
            risk_level=self.risk_level,
        )


class ToolRegistry:
    """Register named tools and their structured contracts."""

    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(self, name: str, fn: ToolFn, spec: ToolSpec | None = None) -> None:
        """Register a callable tool."""

        self._tools[name] = RegisteredTool(fn=fn, spec=spec or _default_spec(name))

    def get_spec(self, name: str) -> ToolSpec:
        """Return a tool contract by name."""

        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name].spec

    def export_tool_manifest(self) -> list[dict[str, Any]]:
        """Export all registered tool specs as manifest rows."""

        return [entry.spec.manifest_entry() for entry in self._tools.values()]

    def call(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """Call a registered tool without external accounting."""

        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        entry = self._tools[name]
        payload = entry.fn(arguments)
        context_chars = estimate_context_chars(payload)
        return ToolResult(
            tool_name=name,
            arguments=arguments,
            payload=payload,
            cost_proxy=entry.spec.cost_estimate + context_chars / 1000,
            context_chars=context_chars,
            risk_level=entry.spec.risk_level,
        )


class ToolExecutor:
    """Execute tools through the registry and attach accounting metadata."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def call(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """Call one tool and record latency / cost / context estimates."""

        started = perf_counter()
        result = self.registry.call(name, arguments)
        result.latency_ms = int((perf_counter() - started) * 1000)
        return result

    def export_tool_manifest(self) -> list[dict[str, Any]]:
        """Expose registered tools as an MCP-compatible manifest."""

        return self.registry.export_tool_manifest()


def export_tool_manifest(registry: ToolRegistry | ToolExecutor) -> list[dict[str, Any]]:
    """Export a tool manifest from either registry or executor."""

    return registry.export_tool_manifest()


def estimate_context_chars(value: Any) -> int:
    """Estimate text size contributed by a structured tool result."""

    if value is None:
        return 0
    if isinstance(value, str):
        return len(value)
    if isinstance(value, dict):
        return sum(estimate_context_chars(item) for item in value.values())
    if isinstance(value, list):
        return sum(estimate_context_chars(item) for item in value)
    return len(str(value))


def _default_spec(name: str) -> ToolSpec:
    """Create a conservative contract for legacy registrations."""

    return ToolSpec(
        name=name,
        description=f"In-process tool: {name}",
        input_schema={"type": "object"},
        output_schema={"type": "object"},
    )
