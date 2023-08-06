import click
import datetime
from click.types import DateTime

from .base import AliasedGroup
from yucebio_wdladaptor.util.config import Config
from yucebio_wdladaptor.util.monitor import Monitor

@click.group('monitor', cls=AliasedGroup)
def cli():
    """作业监控"""
    pass


@cli.command()
@click.option('--page', '-p', help="分页页码", type=int, default=1, show_default=True)
@click.option('--pageSize', '-ps', help="每页查询的数据量", type=int, default=10, show_default=True)
def ls(**kw):
    """查看本人提交的任务最新状态"""

    monitor = Monitor()
    # monitor.list_local_jobs()
    monitor.list_jobs(kw)


@cli.command()
@click.option('--proxy', '-p', help="数据库类型", default="mongo")
@click.option('--uri', '-u', help="数据库地址，格式为： mongodb://[user:pass@]host[:port][/[defaultauthdb][?options]]", required=True)
@click.option('--dbname', '-d', help="数据库名称", default="yucebio_wdl", show_default=True)
@click.option('--collection_name', '-n', help="表或集合名称", default="wdl_metadata", show_default=True)
def set_mongo(**kw):
    """配置数据持久化地址：当前仅支持mongo
    
    参考 https://docs.mongodb.com/manual/reference/connection-string/
    """
    config = Config()

    config.set("persist", kw)
    config.pp(config.get('persist'))


@cli.command()
@click.option('--server', help="cromwell server 配置名称", required=True)
@click.option('--id', '-j', help="cromwell 作业编号")
@click.option('--name', '-n', help="cromwell 流程名称")
@click.option('--status', '-s', help="cromwell 作业状态", type=click.Choice(['Submitted', 'Running', 'Aborting', 'Failed', 'Succeeded', 'Aborted']))
@click.option('--start', '-st', help="cromwell 开始时间", type=DateTime())
@click.option('--submission', '-su', help="cromwell 提交时间", type=DateTime())
@click.option('--page', '-p', help="分页页码", type=int)
@click.option('--pageSize', '-ps', help="每页查询的数据量", type=int)
def query(**kw):
    """基于Cromwell API接口查询所有任务基本信息

    参考: https://cromwell.readthedocs.io/en/stable/api/RESTAPI/#workflowqueryparameter
    """
    server = kw.pop('server')
    params = {k:v for k,v in kw.items() if v}
    for k in ['start', 'submission']:
        if not kw[k]:
            continue
        t: datetime.datetime = kw[k]
        params[k] = t.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    if not params:
        ctx = click.get_current_context()
        click.secho('请至少指定一种参数', fg='red')
        print(ctx.get_help())
        return

    monitor = Monitor()
    data = monitor.query(params, server)

    total, results = data['totalResultsCount'], data['results']
    click.secho(f"总数据量：{total}", fg="green")

    for job in results:
        try:
            cromwell_job = monitor.get(job['id'], server)
        except Exception as e:
            click.secho(f"{job['id']}\t{server}\t获取metadata失败：{e}")
            continue
        cromwell_job.format()

@cli.command()
@click.option('--server', '-s', help="cromwell server 配置名称", required=True)
@click.argument("cromwell_id", nargs=-1)
def add_job(**kw):
    """添加本人通过其他方式提交的任务

    CROMWELL_ID 当前Server下的1个或多个作业编号
    """
    config = Config()
    
    monitor = Monitor()
    for cromwell_id in kw['cromwell_id']:
        try:
            cromwell_job = monitor.get(cromwell_id, kw['server'])
        except Exception as e:
            click.secho(f"{cromwell_id}\t{kw['server']}\t获取metadata失败：{e}")
            continue
        cromwell_job.format()
        config.add_job(cromwell_id, kw["server"])