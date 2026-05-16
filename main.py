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


def get_commit_detail(repo_path: str, hash_: str) -> dict:
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

    patch_result = subprocess.run(
        ["git", "-C", repo_path, "show", "-p", "--format=", hash_],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    patch = patch_result.stdout.strip()

    return {"hash": hash_, "message": message, "timestamp": timestamp, "patch": patch}


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
        hashes = get_commit_hashes(repo, author, target_date)
        if not hashes:
            continue

        found_any = True
        click.echo(f"\n[仓库] {repo}")
        for hash_ in hashes:
            c = get_commit_detail(repo, hash_)
            click.echo(f"\n  [{c['hash'][:8]}]  {c['timestamp']}")
            if c["message"]:
                for line in c["message"].splitlines():
                    click.echo(f"  {line}")
            if c["patch"]:
                click.echo("")
                for line in c["patch"].splitlines():
                    click.echo(f"  {line}")

    if not found_any:
        click.echo(f"\n未找到 {author} 在 {target_date} 的提交。")


if __name__ == "__main__":
    main()
