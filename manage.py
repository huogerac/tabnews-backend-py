#!/usr/bin/env python

import click
import json

from flask.cli import FlaskGroup


from app import create_app
from services import users as users_service


def flask_app(info):
    return create_app()


@click.group(cls=FlaskGroup, create_app=flask_app)
def cli():
    """This is a management script"""


@cli.command()
@click.option("--name", prompt=True, required=True)
@click.option("--email", prompt=True, required=True)
@click.password_option(help="Password.")
def create_user(name, email, password):
    """Create User from the command line"""
    try:
        new_user = users_service.create_user(name, email, password)
        print(json.dumps(new_user, indent=2))
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    cli()
