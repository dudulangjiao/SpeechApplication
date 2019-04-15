#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
# 把项目目录加入系统路径，否则在ssh终端运行程序时将提示找不到模块
sys.path.append('/vagrant/SpeechApplication/')

import click
#from flask.cli import AppGroup
from flask.cli import FlaskGroup
from src import app
#from src.application.database import Speech_sheet

def create_app():
    # other setup

    return app

# 第一种运行方式
@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""
    click.echo('flask group stuff...')
    pass

@cli.command()
def tmp_command():
    click.echo('这是第1行临时命令')
    tmp_sentence_list = [[], []]
    tmp_sentence_list[0].append(3)
    tmp_sentence_list[0].append(2)

    tmp_sentence_list[1].append(2)
    tmp_sentence_list[1].append(2)
    print(tmp_sentence_list)
@cli.command()
def flask_test2():
    click.echo('这是第2行临时命令')

if __name__ == '__main__':
    cli()
# 运行临时命令
# python3 /vagrant/SpeechApplication/src/run.py tmp-command
# 运行主程序
# python3 /vagrant/SpeechApplication/src/run.py run --host=192.168.0.199 --debugger
# 运行sh脚本，进行mysql操作
# /vagrant/software/entermysql.sh



""" 第二种运行方式

command_g = AppGroup('tmp_command_group')

@command_g.command('no_1')
@click.argument('name')
def create_user(name):
    click.echo('第一个临时命令' + name)

@command_g.command('no_2')
@click.argument('name')
def create_user(name):
    click.echo('第二个临时命令' + name)

app.cli.add_command(command_g)

"""


# python3 /vagrant/SpeechApplication/src/run.py tmp-command

# 以下是启动命令
# cd /vagrant/SpeechApplication
# export FLASK_APP=/vagrant/SpeechApplication/src/run
# export FLASK_RUN_HOST=192.168.0.199
# flask run

# 以调试模式运行
# FLASK_ENV=development flask run --host 192.168.0.199
# 以生产模式运行（默认）
# FLASK_ENV=production flask run --host 192.168.0.199

# 运行临时命令
# export FLASK_APP=/vagrant/SpeechApplication/src/run
# 运行第一个命令
# flask tmp_command_group no_1 demo
# 运行第二个命令
# flask tmp_command_group no_2 demo



