from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class JsonStore:
    def __init__(self, output_dir: str | Path | None = None) -> None:
        base_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parents[1] / "data"
        self.output_dir = base_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, payload: dict[str, Any], filename: str | None = None) -> Path:
        target_name = filename or f"ai_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        target_path = self.output_dir / target_name
        target_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return target_path

