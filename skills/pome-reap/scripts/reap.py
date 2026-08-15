#!/usr/bin/env python3
"""reap.py —— 把 .pome/nursery/ 的产物归档到 .pome/archive/<任务简称>/。

用法:
    python reap.py <任务简称> [--nursery PATH] [--archive-root PATH] [--dry-run]

默认:
    nursery       .pome/nursery
    archive-root  .pome/archive

行为:
    1. 清洗任务简称为安全的目录名（去掉路径分隔符与非法字符，折叠空白为 '-'）。
    2. 校验 nursery 存在且非空，目标归档目录不存在或为空（非空视为简称占用）。
    3. 移动 nursery 下全部条目到归档目录，nursery 清空后保留目录本身。
    4. 归档后校验源已清空，任一条目残留则以非零码退出。

退出码: 0 成功；1 前置检查失败或残留；2 简称清洗后为空。
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# 允许出现在目录名中的字符：Unicode 字词（含中文）、空格、点、括号、下划线、横线。
# 其余字符（斜杠、反斜杠、冒号等）在清洗时替换为 '-'。
_ILLEGAL = re.compile(r"[^\w .()_-]+", re.UNICODE)


def sanitize(name: str) -> str:
    """把任务简称清洗为单个安全的路径组件。"""
    name = (name or "").replace("\\", "/").split("/")[-1]  # 若误带路径，仅取最后一段
    name = name.strip()
    name = re.sub(r"\s+", "-", name)  # 空白折叠为 '-'
    name = _ILLEGAL.sub("-", name)  # 非法字符替换为 '-'
    name = re.sub(r"-+", "-", name)  # 合并连续 '-'
    name = name.strip("-._")  # 去掉首尾的点/横线/下划线，避免歧义或隐藏名
    return name


def _entries(directory: Path) -> list[Path]:
    return sorted(p for p in directory.iterdir())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="把 nursery 的产物归档到 archive/<任务简称>/")
    parser.add_argument("name", help="任务简称，用于命名归档目录")
    parser.add_argument("--nursery", default=".pome/nursery", help="来源目录（默认 .pome/nursery）")
    parser.add_argument("--archive-root", default=".pome/archive", help="归档根目录（默认 .pome/archive）")
    parser.add_argument("--dry-run", action="store_true", help="只打印将执行的动作，不实际移动")
    args = parser.parse_args(argv)

    short = sanitize(args.name)
    if not short:
        print("错误：任务简称清洗后为空，请提供非空的简称。", file=sys.stderr)
        return 2

    nursery = Path(args.nursery)
    archive_root = Path(args.archive_root)

    if not nursery.is_dir():
        print(f"错误：nursery 目录不存在：{nursery}", file=sys.stderr)
        return 1

    entries = _entries(nursery)
    if not entries:
        print(f"错误：nursery 目录为空，无可归档产物：{nursery}", file=sys.stderr)
        return 1

    target = archive_root / short
    if target.exists() and not target.is_dir():
        print(f"错误：目标路径已存在且不是目录：{target}", file=sys.stderr)
        return 1
    if target.is_dir() and any(target.iterdir()):
        print(f"错误：目标归档目录已存在且非空：{target}", file=sys.stderr)
        print("该任务简称可能已被占用；请换一个简称，或与用户确认是否覆盖/合并。", file=sys.stderr)
        return 1

    print(f"任务简称：{short}")
    print(f"来源目录：{nursery}")
    print(f"归档目录：{target}")
    print(f"待归档 {len(entries)} 个条目：")
    for entry in entries:
        print(f"  - {entry.name}")

    if args.dry_run:
        print("[dry-run] 未执行任何移动。")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        shutil.move(str(entry), str(target / entry.name))

    remaining = _entries(nursery)
    if remaining:
        print(f"错误：归档后 nursery 仍有残留条目：{[p.name for p in remaining]}", file=sys.stderr)
        return 1

    print(f"已归档 {len(entries)} 个条目到 {target}")
    print("校验通过：nursery 已清空。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
