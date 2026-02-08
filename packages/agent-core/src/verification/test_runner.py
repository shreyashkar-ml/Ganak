
from typing import Iterable

from tools.tool_sandbox_proxy import SandboxProxy
from verification.checks import CheckResult


def run_checks(sandbox: SandboxProxy, commands: Iterable[str]) -> list[CheckResult]:
    """Run verification commands via the sandbox proxy."""
    results: list[CheckResult] = []
    for command in commands:
        result = sandbox.run(command, timeout_s=120)
        results.append(
            CheckResult(
                name=command,
                passed=result.exit_code == 0,
                output=result.stdout + result.stderr,
            )
        )
    return results

