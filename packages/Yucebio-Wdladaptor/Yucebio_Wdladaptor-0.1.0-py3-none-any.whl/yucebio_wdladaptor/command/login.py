import click
from yucebio_wdladaptor.util.config import Config


@click.command()
@click.option("--gitlab_host", "-g", help="自建或公共Gitlab API地址", default="http://gitlab.yucebio.com")
@click.option("--username", '-u', help="用户名", required=True, type=str)
@click.option("--owner", '-o', help="投递分析任务时的属主信息(默认与用户名保持一致)", type=str)
@click.password_option("--password", '-p', help="密码")
@click.option("--sync", '-s', is_flag=True, default=False, help="是否需要自动同步配置到本地", show_default=True)
# @click.option("--grant_type", help="OAuth2认证类型。", type=click.Choice(["password"]), default="password", show_default=True)
def login(**kw):
    """基于gitlab api v4实现登录认证。登录成功后可以根据需要执行初次配置同步
    """
    config = Config(check_login=False)
    config.set_sync_config(kw['username'], kw['password'], kw['gitlab_host'], grant_type='password')

    if kw['sync'] or not config.servers:
        try:
            # 尝试进行一次配置同步，若配置不存在，则保持沉默
            url = config.download_config(silent=True)
        except Exception as e:
            click.secho(f"下载配置异常: {e}", fg='red')
            return
        if url:
            click.secho(f"download success from {url}", fg='green')

    # 更新owner信息
    owner = kw['owner']
    if not owner:
        owner = kw['username'].split('@')[0]
    if not config.get('owner'):
        config.set('owner', owner)
    # config.set('owner', owner)

    click.secho(f"Hi {owner}! Welcome to Yucebio WDL!!!", fg='green')