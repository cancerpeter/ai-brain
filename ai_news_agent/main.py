from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai_news_agent.workflow.scheduler import run_daily_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI 前沿资讯抓取与日报生成系统")
    parser.add_argument(
        "--max-items-per-source",
        type=int,
        default=8,
        help="每个站点最多抓取的文章数",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="将最终结果直接打印到标准输出",
    )
    return parser


async def _run(args: argparse.Namespace) -> int:
    result = await run_daily_pipeline(max_items_per_source=args.max_items_per_source)
    payload = result["payload"]
    output_path = result["output_path"]
    report_path = result["report_path"]

    print(f"Pipeline finished. total_unique={payload['total_unique']}, output={output_path}")
    print(f"Markdown report: {report_path}")
    for article in payload["articles"][:5]:
        print(f"- [{article['source']}] {article['title']}")

    if args.print_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return asyncio.run(_run(args))


if __name__ == "__main__":
    raise SystemExit(main())
