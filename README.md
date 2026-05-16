# coding-work-report

扫描指定路径下的所有 Git 仓库，列出指定提交人在指定日期的所有提交。

## 安装

### 通过 uvx 直接运行（推荐）

无需安装，直接运行：

```bash
uvx coding-work-report --author "你的名字"
```

### 本地开发

```bash
uv sync
```

## 使用

```bash
# 扫描当前目录下所有仓库，查找当天指定作者的提交
uvx coding-work-report --author "你的名字"

# 指定路径和日期
uvx coding-work-report --path "E:\code" --author "IVEN" --date 2026-05-16

# 保存为 Markdown 文件
uvx coding-work-report --author "IVEN" --output report.md

# 不显示代码 diff（仅提交信息）
uvx coding-work-report --author "IVEN" --no-detail

# 查看帮助
uvx coding-work-report --help
```

### 参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--path` | `-p` | 扫描路径 | `.` (当前目录) |
| `--date` | `-d` | 指定日期 (YYYY-MM-DD) | 当天 |
| `--author` | `-a` | 提交人 (name 或 email) | **必填** |
| `--output` | `-o` | 保存 Markdown 报告的文件路径 | 输出到终端 |
| `--detail` / `--no-detail` | 无 | 显示详细代码变更 | 开启 |
