from os import environ

from litestar.__main__ import run_cli as run_litestar_cli


def run_cli():
    environ.setdefault("LITESTAR_APP", "prolog_backend.app:app")

    run_litestar_cli()


if __name__ == "__main__":
    run_cli()
