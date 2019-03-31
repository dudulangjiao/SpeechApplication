import click
from flask import Flask
from flask.cli import FlaskGroup

def create_app(param):
    return Flask(__name__)

@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    click.echo('运行临时命令')


@cli.command()
def flask_test():
    click.echo('第1个命令')


if __name__ == '__main__':
    cli()