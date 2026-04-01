from __future__ import annotations

from pathlib import Path


class MarkdownStore:
    def __init__(self, output_dir: str | Path | None = None) -> None:
        self.output_dir = Path(output_dir) if output_dir else Path("reports/ai-daily")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, content: str, filename: str) -> Path:
        target_path = self.output_dir / filename
        target_path.write_text(content, encoding="utf-8")
        return target_path

