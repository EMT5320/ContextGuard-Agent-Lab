"""Simple in-process tool registry.

The registry mirrors an MCP-like boundary: tools receive structured
arguments and return structured payloads plus trace metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from contextguard_agent_lab.benchmark.schema import ToolCallTrace

ToolFn = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(slots=True)
class ToolResult:
    """Structured result returned by a registered tool."""

    tool_name: str
    arguments: dict[str, Any]
    payload: dict[str, Any]
    latency_ms: int = 0

    def trace(self, case_id: str, step_index: int) -> ToolCallTrace:
        """Convert the tool result into a benchmark trace row."""

        return ToolCallTrace(
            case_id=case_id,
            step_index=step_index,
            tool_name=self.tool_name,
            arguments=self.arguments,
            result=self.payload,
            latency_ms=self.latency_ms,
        )


class ToolRegistry:
    """Register and call named tools."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolFn] = {}

    def register(self, name: str, fn: ToolFn) -> None:
        """Register a callable tool."""

        self._tools[name] = fn

    def call(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """Call a registered tool by name."""

        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        payload = self._tools[name](arguments)
        return ToolResult(tool_name=name, arguments=arguments, payload=payload)
