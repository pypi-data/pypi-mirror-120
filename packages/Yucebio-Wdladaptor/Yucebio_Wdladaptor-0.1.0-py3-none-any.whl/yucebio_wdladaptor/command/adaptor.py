import json
import click
from .base import AliasedGroup
from yucebio_wdladaptor.util.config import Config
from yucebio_wdladaptor.backend import SUPPORTTED_BACKENDS, create_adaptor, PLACEHOLDER_SIMG_PATH, PLACEHOLDER_GLOBAL_PATH, BaseAdaptor


@click.group('adaptor', cls=AliasedGroup)
def cli():
    """WDL适配器"""
    pass


@cli.command()
@click.option("--input", "-i", required=False, help="input json file include project information")
@click.option("--platform_alias", "-p", required=True, type=str, help="平台配置名称")
@click.option("--submit", "-s", is_flag=True, default=False, help="auto submit to cromwell server")
@click.option('--runtimes', '-r', help=f"配置需要自动添加到task.runtime中的属性", type=str)
@click.argument("wdl")
def convert(**kw):
    """根据不同平台具有的基础设施转换通用WDL，并自动适配json和task
    """
    adaptor = create_adaptor(kw['platform_alias'])
    adaptor.parse(wdl_path=kw['wdl'], input_path=kw['input'], runtimes=kw["runtimes"])

    adaptor.convert()

    if not kw['submit']:
        adaptor.generate_file()
    else:
        jobid = adaptor.submit()
        click.secho(f"submit success: {jobid}", fg="green")

        adaptor._config.add_job(jobid, kw["platform_alias"])

@cli.command()
@click.option("--access_id", "-i", help="阿里云ACCESS KEY ID")
@click.option('--access_secrect', '-s', help="阿里云ACCESS KEY SECRECT")
def update_bcs_instance(access_id, access_secrect):
    """更新阿里云可用类型
    """
    import batchcompute, datetime
    bNeedUpdateAccess = True
    # adaptor = BaseAdaptor()
    config = Config()
    if not (access_id and access_secrect):
        # 从配置文件中获取
        # cfg = adaptor.config("bcs_access", {})
        cfg = config.get("bcs_access", {})
        if not cfg:
            click.secho("请提供ACCESS_KEY_ID和ACCESS_KEY_SECRECT", fg='yellow')
            return
        access_id, access_secrect = cfg.get("access_id", ""), cfg.get("access_secrect", "")
        bNeedUpdateAccess = True

    if not (access_id and access_secrect):
        return

    try:
        client = batchcompute.Client(batchcompute.CN_SHENZHEN, access_id, access_secrect)
        response = client.get_available_resource()
    except Exception as e:
        click.secho(f"Error: {e.code} 请检查ACCESS_KEY_ID[{repr(access_id)}]和ACCESS_KEY_SECRECT[{repr(access_secrect)}]是否正确", fg='red')
        return

    if bNeedUpdateAccess:
        config.set("bcs_access", {"access_id": access_id, "access_secrect": access_secrect})
    data = response.content
    data['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d")
    config.set("available_bcs_rescource", data)
    click.secho("阿里云可用实例类型更新完毕！")



if __name__ == "__main__":
    cli()
