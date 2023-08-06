import json
from typing import Any, TypedDict
from yucebio_config import Config as BaseConfig

from yucebio_wdladaptor.util.gist import Gist


class ServerConfig(TypedDict):
    platform: str
    host: str
    global_path: str
    simg_path: str
    runtimes: str

class WorkflowJob(TypedDict):
    cromwell_id: str
    server: str

class Config(BaseConfig):
    SNIPPET_TITLE = "Yucebio Wdladaptor Config"
    SNIPPET_FILE_NAME = "yucebio_wdladaptor_config.json"

    def __init__(self, name: str = "wdladaptor", path: str = None, check_login = True) -> None:
        super().__init__(name=name, path=path)
        self.load()
        self.check_version()

        self.sync_config = BaseConfig("sync_credentials")
        if check_login:
            self.validate_login()

    # TODO: 判断配置是否有效
    

    @property
    def servers(self) -> dict[str, ServerConfig]:
        """管理Cromwell Server配置项"""
        return self._config.get('server', {})

    def add_server(self, platform_alias: str = None, new_config: dict = None) -> dict:
        """查询或更新服务器配置:  cromwell api地址， 公共目录以及simg目录必须配置
        1. 查询              c = adaptor.config()
        2. 查询指定配置      c  = adaptor.config('aws')
        3. 更新指定配置       adaptor.config('aws', {...})
        """
        server_config = self.servers

        if platform_alias:
            platform_alias = platform_alias.lower()
            if new_config:
                server_config[platform_alias] = new_config
                self.set('server', server_config)
            return server_config.get(platform_alias, {})
        return self.servers

    def get_server(self, server_alias: str) -> ServerConfig:
        return self.servers.get(server_alias, {})

    def del_server(self, server_alias: str):
        servers = self.servers
        if server_alias in servers:
            del servers[server_alias]
        self.set('server', servers)

    @property
    def jobs(self) -> list[WorkflowJob]:
        """管理已投递的所有作业"""
        return self._config.get("workflows", [])

    def add_job(self, jobid: str, server_alias: str):
        jobs = self.jobs
        jobs.append({
            "cromwell_id": jobid, "server": server_alias
        })
        self.set('workflows', jobs)
        return jobs

    def set(self, key: str, value: Any, quiet=True):
        self._config[key] = value
        self.reload()
        self.upload_config()

    def get(self, key: str, default = None):
        return self.config.get(key, default)

    def check_version(self):
        """检查配置版本信息。并根据需要自动完成配置升级
        """
        config_version = self.get("version", 1)
        if config_version > 1:
            return config_version

        # 避免循环引入，直接在函数内导入所需模块
        from yucebio_wdladaptor.backend import SUPPORTTED_BACKENDS

        server_config = self.servers
        for backend_name in SUPPORTTED_BACKENDS:
            if backend_name in self._config:
                backend_config = self._config.pop(backend_name)
                backend_config['platform'] = backend_name
                server_config[backend_name] = backend_config
        self._config['server'] = server_config
        self._config['version'] = 2
        self.reload()
        return 2

    def pp(self, obj: Any = None):
        if obj == None:
            obj = self._config
        print(json.dumps(obj, indent=2, default=str))

    def set_sync_config(self, username: str, password: str, api: str, grant_type: str="password"):
        current_config = self.sync_config.config

        current_config.update({
            "username": username,
            "password": password,
            "api": api,
            "grant_type": grant_type
        })
        self.sync_config.init(current_config)

    def validate_login(self):
        """为了准确识别使用者身份，强制要求使用之提供认证信息
        """
        current_config = self.sync_config.config
        if not current_config:
            raise RuntimeError("未登录")
        self.get_gist(False)

    def get_gist(self, silent: bool = True) -> Gist:
        username = self.sync_config('username')
        password = self.sync_config('password')
        grant_type = self.sync_config('grant_type')
        api = self.sync_config('api')
        if not all([username, password, grant_type, api]):
            if not silent:
                raise RuntimeError("缺少Gitlab必要配置内容")
            return
        gist = Gist(username, password, api)
        if grant_type != 'password':
            if not silent:
                raise RuntimeError("仅支持通过用户名和密码的方式使用Gitlab")
            return

        gist.validate_api()
        return gist

    def get_exist_snippet(self, gist: Gist):
        title, file_name = self.SNIPPET_TITLE, self.SNIPPET_FILE_NAME
        # gist没有去重的逻辑，需要自己处理查重
        snippets = gist.query({"title": title, "file_name": file_name})
        if not snippets:
            return
        return snippets[0]

    def upload_config(self) -> str:
        """上传配置, 成功时返回配置链接
        """
        gist = self.get_gist()
        if not gist:
            return
        content = json.dumps(self._config, indent=2)
        exist = self.get_exist_snippet(gist)
        if exist:
            gist.update(exist, content)
        else:
            exist = gist.create(self.SNIPPET_TITLE, self.SNIPPET_FILE_NAME, content)
        return f"{gist.api}/snippets/{exist['id']}"

    def download_config(self, silent = False):
        """下载配置，成功时，返回下载地址
        """
        gist = self.get_gist(silent=False)
        exist = self.get_exist_snippet(gist) 
        if not exist:
            if not silent:
                raise RuntimeError("没有找到可用的配置")
            return
        content: dict = json.loads(gist.get_content(exist['id']))
        self.init(content)
        return f"{gist.api}/snippets/{exist['id']}"


