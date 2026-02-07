from __future__ import annotations

import argparse

from client import ApiClient
from commands.login import run_login
from commands.repo import register_repo
from commands.run import create_run
from commands.session import create_session
from config import CliConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bg-agent")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("login")

    session_parser = sub.add_parser("session")
    session_parser.add_argument("repo_id")

    run_parser = sub.add_parser("run")
    run_parser.add_argument("session_id")
    run_parser.add_argument("prompt")

    repo_parser = sub.add_parser("repo")
    repo_parser.add_argument("url")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    client = ApiClient(CliConfig())

    if args.command == "login":
        run_login()
        return
    if args.command == "session":
        create_session(client, args.repo_id)
        return
    if args.command == "run":
        create_run(client, args.session_id, args.prompt)
        return
    if args.command == "repo":
        register_repo(client, args.url)
        return

    parser.print_help()


if __name__ == "__main__":
    main()

