from os import environ

from litestar.__main__ import litestar_group
from litestar.__main__ import run_cli as run_litestar_cli

from prolog_backend.cli.database import database_group
from prolog_backend.cli.tenant import tenant_group


def run_cli():
    environ.setdefault("LITESTAR_APP", "prolog_backend.app:app")

    litestar_group.add_command(database_group)
    litestar_group.add_command(tenant_group)

    run_litestar_cli()


if __name__ == "__main__":
    run_cli()
