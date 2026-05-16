import datetime
import os
import subprocess

import click


def find_git_repos(root: str) -> list[str]:
    repos = []
    for dirpath, dirnames, _ in os.walk(root):
        if ".git" in dirnames:
            repos.append(dirpath)
            dirnames.remove(".git")
    return repos


def get_commit_hashes(repo_path: str, author: str, target_date: datetime.date) -> list[str]:
    since = target_date.strftime("%Y-%m-%d 00:00:00")
    until = target_date.strftime("%Y-%m-%d 23:59:59")

    result = subprocess.run(
        [
            "git",
            "-C",
            repo_path,
            "log",
            f"--since={since}",
            f"--until={until}",
            f"--author={author}",
            "--pretty=format:%H",
            "--no-merges",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return [h.strip() for h in result.stdout.strip().splitlines() if h.strip()]


def get_commit_detail(repo_path: str, hash_: str, detail: bool = True) -> dict:
    msg_result = subprocess.run(
        ["git", "-C", repo_path, "log", "-1", "--format=%B", hash_],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    message = msg_result.stdout.strip()

    ts_result = subprocess.run(
        ["git", "-C", repo_path, "log", "-1", "--format=%ci", hash_],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    timestamp = ts_result.stdout.strip()

    patch = ""
    if detail:
        patch_result = subprocess.run(
            ["git", "-C", repo_path, "show", "-p", "--format=", hash_],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        patch = patch_result.stdout.strip()

    return {"hash": hash_, "message": message, "timestamp": timestamp, "patch": patch}


def colorize_diff_line(line: str) -> str:
    if line.startswith("+") and not line.startswith("+++"):
        return click.style(line, fg="green")
    if line.startswith("-") and not line.startswith("---"):
        return click.style(line, fg="red")
    if line.startswith("@@"):
        return click.style(line, fg="cyan")
    if line.startswith("diff --git") or line.startswith("index "):
        return click.style(line, fg="bright_black")
    if line.startswith("--- ") or line.startswith("+++ "):
        return click.style(line, fg="bright_black")
    return line


@click.command()
@click.option("--path", "-p", default=".", help="扫描路径")
@click.option(
    "--date", "-d",
    default=lambda: datetime.date.today().isoformat(),
    help="指定日期 (YYYY-MM-DD，默认当天)",
)
@click.option("--author", "-a", required=True, help="提交人 (name 或 email)")
@click.option(
    "--output", "-o",
    default=None,
    help="保存 Markdown 报告的文件路径",
)
@click.option(
    "--detail/--no-detail",
    default=True,
    help="显示详细代码变更 (默认开启)",
)
def main(path: str, date: str, author: str, output: str | None, detail: bool) -> None:
    target_date = datetime.date.fromisoformat(date)
    repos = find_git_repos(path)

    if not repos:
        click.echo("未找到任何 Git 仓库。", err=True)
        return

    lines: list[str] = []
    lines.append("# 工作报告")
    lines.append("")
    lines.append(f"> **日期:** {target_date}")
    lines.append(f"> **作者:** {author}")
    lines.append("")

    found_any = False
    for repo in repos:
        hashes = get_commit_hashes(repo, author, target_date)
        if not hashes:
            continue

        found_any = True
        lines.append("---")
        lines.append("")
        lines.append(f"## 仓库: `{repo}`")
        lines.append("")

        for hash_ in hashes:
            c = get_commit_detail(repo, hash_, detail=detail)
            first_line = c["message"].splitlines()[0] if c["message"] else ""
            lines.append(f"### `{c['hash'][:8]}` {first_line}")
            lines.append("")
            lines.append(f"- **时间:** {c['timestamp']}")
            lines.append("")

            if c["message"]:
                lines.append("**提交信息:**")
                lines.append("")
                for msg_line in c["message"].splitlines():
                    lines.append(msg_line)
                lines.append("")

            if c["patch"]:
                lines.append("**代码变更:**")
                lines.append("")
                lines.append("```diff")
                for patch_line in c["patch"].splitlines():
                    if output:
                        lines.append(patch_line)
                    else:
                        lines.append(colorize_diff_line(patch_line))
                lines.append("```")
                lines.append("")

    if not found_any:
        lines.append(f"未找到 {author} 在 {target_date} 的提交。")

    report = "\n".join(lines)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(report)
        click.echo(f"报告已保存至: {output}")
    else:
        click.echo(report)


if __name__ == "__main__":
    main()
