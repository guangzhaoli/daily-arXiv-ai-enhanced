#!/usr/bin/env python3
"""
检查 Scrapy 爬取结果的脚本 / Script to validate Scrapy crawling output.
保留与 arXiv 列表页一致的全部条目，不做任何内容过滤。
"""

import json
import os
import sys
from datetime import datetime


def load_papers_data(file_path):
    """
    从 jsonl 文件中加载完整的论文数据。

    Returns:
        tuple[list, set]: 论文列表和唯一 ID 集合
    """
    if not os.path.exists(file_path):
        return [], set()

    papers = []
    ids = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                papers.append(data)
                ids.add(data.get("id", ""))
        return papers, ids
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return [], set()


def perform_deduplication():
    """
    为了兼容现有工作流保留这个函数名，但不再执行任何去重。
    """
    today = datetime.now().strftime("%Y-%m-%d")
    today_file = f"../data/{today}.jsonl"

    if not os.path.exists(today_file):
        print("今日数据文件不存在 / Today's data file does not exist", file=sys.stderr)
        return "no_data"

    try:
        today_papers, today_ids = load_papers_data(today_file)
        print(
            f"今日论文总数: {len(today_papers)} / Today's total papers: {len(today_papers)}",
            file=sys.stderr,
        )

        if not today_papers:
            return "no_data"

        duplicate_entries = len(today_papers) - len(today_ids)
        if duplicate_entries > 0:
            print(
                f"今日包含 {duplicate_entries} 个重复 ID 条目（例如 cross-list 或多分类页面重复），按原样保留 "
                f"/ Today's file contains {duplicate_entries} repeated ID entries and they are kept as-is",
                file=sys.stderr,
            )
        else:
            print(
                "未发现重复 ID 条目，按原样保留全部内容 / No repeated ID entries detected; keeping all content",
                file=sys.stderr,
            )

        return "has_new_content"
    except Exception as e:
        print(f"结果检查失败: {e} / Output validation failed: {e}", file=sys.stderr)
        return "error"


def main():
    """
    检查抓取结果并返回相应的退出码。

    Exit code meanings:
    0: 有内容，继续处理
    1: 无数据，停止工作流
    2: 处理错误
    """

    print("正在检查抓取结果... / Validating crawl output...", file=sys.stderr)
    dedup_status = perform_deduplication()

    if dedup_status == "has_new_content":
        print(
            "✅ 检查完成，保留全部内容并继续工作流 / Validation completed, keeping all content and continuing workflow",
            file=sys.stderr,
        )
        sys.exit(0)
    if dedup_status == "no_data":
        print("⏹️ 今日无数据，停止工作流 / No data today, stop workflow", file=sys.stderr)
        sys.exit(1)
    if dedup_status == "error":
        print("❌ 结果检查出错，停止工作流 / Output validation error, stop workflow", file=sys.stderr)
        sys.exit(2)

    print("❌ 未知检查状态，停止工作流 / Unknown validation status, stop workflow", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
