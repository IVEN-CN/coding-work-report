# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

此项目用于扫描指定路径下的所有代码仓库在指定日期（默认当天）指定提交人的所有提交。

## Environment

- Python 3.12+
- Package manager: uv (pyproject.toml)

## Common Commands

- Run the project: `uv run main.py`
- Run tests: `uv run pytest`
- Type check: `uv run mypy main.py`
- Format code: `uv run ruff format .`
- Lint code: `uv run ruff check .`

## Architecture

Currently a single-file project. `main.py` is the entry point. No external dependencies yet.
