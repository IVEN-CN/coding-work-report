# coding-work-report

扫描指定路径下的所有 Git 仓库，列出指定提交人在指定日期的所有提交。

## 安装

### 通过 uvx 直接运行（推荐）

无需安装：

```bash
uvx coding-work-report --help
```

> 如果国内 PyPI 镜像未同步最新版本，可强制走官方源：
> ```bash
> uvx --index-url https://pypi.org/simple coding-work-report --help
> ```

### 本地开发

```bash
uv sync
uv run generate_work_report/cli.py --help
```

## 使用

```bash
# 扫描当前目录下所有仓库，查找当天指定作者的提交
uvx coding-work-report --author "IVEN"

# 指定路径和日期
uvx coding-work-report --path "E:\code" --author "IVEN" --date 2026-05-16

# 保存为 Markdown 文件
uvx coding-work-report --author "IVEN" --output report.md

# 不显示代码 diff（仅提交信息）
uvx coding-work-report --author "IVEN" --no-detail
```

### 参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--path` | `-p` | 扫描路径 | `.` (当前目录) |
| `--date` | `-d` | 指定日期 (YYYY-MM-DD) | 当天 |
| `--author` | `-a` | 提交人 (name 或 email) | **必填** |
| `--output` | `-o` | 保存 Markdown 报告的文件路径 | 输出到终端 |
| `--detail` / `--no-detail` | 无 | 显示详细代码变更 | 开启 |

## 发布

推送 git tag 时，GitHub Actions 会自动构建并发布到 PyPI。

### 发布流程

```bash
# 1. 确保代码已 push 到 main
git push origin main

# 2. 打 tag（版本号与 tag 一致）
git tag v0.1.2

# 3. 推送 tag，触发自动发布
git push origin v0.1.2
```

### 配置 PyPI Token

1. 在 GitHub 仓库设置 -> Secrets and variables -> Actions 中
2. 添加 `New repository secret`
3. Name: `PYPI_TOKEN`
4. Secret: 你的 PyPI API token（以 `pypi-` 开头）

获取 token: https://pypi.org/manage/account/#api-tokens
