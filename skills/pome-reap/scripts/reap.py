#!/usr/bin/env python3

import argparse
import re
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    root = parser.parse_args().root.resolve()

    nursery = root / ".pome" / "nursery"
    if not nursery.is_dir() or next(nursery.iterdir(), None) is None:
        print("nursery 下没有文件，无需归档。")
        return 0

    blueprint = nursery / "blueprint.md"
    if not blueprint.is_file():
        print("找不到 .pome/nursery/blueprint.md，无法提取项目名称。")
        return 1

    content = blueprint.read_text(encoding="utf-8")
    match = re.search(r"^#\s*设计方案\s*[：:]\s*(.+?)\s*$", content, re.MULTILINE)
    if not match:
        print("blueprint.md 中没有项目名称。")
        return 1

    project_name = match.group(1).strip()
    if project_name in {".", ".."} or Path(project_name).name != project_name:
        print("项目名称不能包含路径分隔符。")
        return 1

    destination = root / ".pome" / "archive" / date.today().isoformat() / project_name
    if destination.exists():
        print(f"归档目录已存在：{destination.relative_to(root)}")
        return 1

    destination.mkdir(parents=True)
    for item in nursery.iterdir():
        item.rename(destination / item.name)
    print(f"已归档到 {destination.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
