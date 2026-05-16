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


def get_commits(repo_path: str, author: str, target_date: datetime.date) -> list[dict]:
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
            "--pretty=format:%H|%s|%ci",
            "--no-merges",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    commits = []
    for line in result.stdout.strip().splitlines():
        if "|" not in line:
            continue
        hash_, subject, timestamp = line.split("|", 2)
        commits.append({"hash": hash_, "subject": subject, "timestamp": timestamp})
    return commits


@click.command()
@click.option("--path", "-p", default=".", help="扫描路径")
@click.option(
    "--date", "-d",
    default=lambda: datetime.date.today().isoformat(),
    help="指定日期 (YYYY-MM-DD，默认当天)",
)
@click.option("--author", "-a", required=True, help="提交人 (name 或 email)")
def main(path: str, date: str, author: str) -> None:
    target_date = datetime.date.fromisoformat(date)
    repos = find_git_repos(path)

    if not repos:
        click.echo("未找到任何 Git 仓库。", err=True)
        return

    found_any = False
    for repo in repos:
        commits = get_commits(repo, author, target_date)
        if not commits:
            continue

        found_any = True
        click.echo(f"\n[仓库] {repo}")
        for c in commits:
            click.echo(f"  {c['hash'][:8]}  {c['subject']}  ({c['timestamp']})")

    if not found_any:
        click.echo(f"\n未找到 {author} 在 {target_date} 的提交。")


if __name__ == "__main__":
    main()
