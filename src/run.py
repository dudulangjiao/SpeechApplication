import sys
# 把项目目录加入系统路径，否则在ssh终端运行程序时将提示找不到模块
sys.path.append('/vagrant/SpeechApplication/')

import click
from flask.cli import FlaskGroup
from src import app


def create_app():
    # other setup

    return app

@click.group(cls=FlaskGroup, create_app=create_app)
def cli():

    """Management script for the Wiki application."""
    pass

@cli.command()
def tmp_command():
    click.echo('这是第1行临时命令')

# python3 /vagrant/SpeechApplication/src/run.py tmp-command
if __name__ == '__main__':
    cli()

