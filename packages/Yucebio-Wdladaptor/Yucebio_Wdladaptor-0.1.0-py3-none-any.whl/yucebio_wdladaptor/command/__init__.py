from .config import cli as config_cli
from .monitor import cli as monitor_cli
from .adaptor import cli as adaptor_cli
from .login import login
# from yucebio_wdladaptor.util.config import Config
from .base import AliasedGroup
import click


@click.group(cls=AliasedGroup)
def cli():
    """WDL 适配器，初次使用时必须先登录

    - 转换通用WDL到特定平台\n
    - 任务查看、管理
    """
    pass

cli.add_command(login, 'login')
cli.add_command(config_cli, 'config')
cli.add_command(monitor_cli, 'monitor')
cli.add_command(adaptor_cli, 'adaptor')

@cli.command()
def version():
    """显示版本信息
    """
    from yucebio_wdladaptor.version import __version__
    print("Version: ", __version__)



