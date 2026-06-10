from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Plan:
    explanation: str
    commands: list[str]


def route_request(request: str) -> Plan:
    text = request.lower()
    if any(phrase in text for phrase in ("delete all", "delete everything", "wipe", "remove all files")):
        return Plan("This destructive request is routed to a known forbidden command so the broker can demonstrate blocking.", ["rm -rf /"])
    if "install docker" in text:
        return Plan("Update package metadata, install Docker, then verify the installed version.",
                    ["sudo apt update", "sudo apt install docker.io", "docker --version"])
    if "docker ps" in text and ("permission" in text or "denied" in text):
        return Plan("Inspect the current identity and Docker service status. No permission changes are proposed.",
                    ["whoami", "systemctl status docker"])
    if "verify docker" in text or "docker version" in text:
        return Plan("Check the installed Docker version.", ["docker --version"])
    if "disk" in text:
        return Plan("Inspect filesystem usage without modifying files.", ["df -h"])
    if "memory" in text or "ram" in text:
        return Plan("Inspect memory usage without modifying the system.", ["free -h"])
    if "uptime" in text or "cpu" in text or "system" in text:
        return Plan("Inspect uptime and system information.", ["uptime", "uname -a"])
    if "cleanup" in text:
        return Plan("Inspect disk usage only; no personal files or caches will be deleted.", ["df -h"])
    return Plan("No trusted command template matches this request. The broker will classify the proposal as unknown.", ["echo unsupported request"])
