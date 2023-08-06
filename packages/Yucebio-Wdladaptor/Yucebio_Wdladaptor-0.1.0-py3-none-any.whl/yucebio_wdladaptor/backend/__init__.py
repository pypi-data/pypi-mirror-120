from yucebio_wdladaptor.backend.base import BaseAdaptor, PLACEHOLDER_GLOBAL_PATH, PLACEHOLDER_SIMG_PATH
from yucebio_wdladaptor.backend.sge import Adaptor as SgeAdaptor
from yucebio_wdladaptor.backend.bcs import Adaptor as BcsAdaptor
from yucebio_wdladaptor.backend.aws import Adaptor as AwsAdaptor


SUPPORTTED_BACKENDS = {
    SgeAdaptor.PLATFORM.lower(): SgeAdaptor,
    BcsAdaptor.PLATFORM.lower(): BcsAdaptor,
    AwsAdaptor.PLATFORM.lower(): AwsAdaptor
}

def create_adaptor(backend_alias: str= None) -> BaseAdaptor:
    baseAdaptor = BaseAdaptor()
    server_config = baseAdaptor.server_config()

    if not backend_alias or backend_alias not in server_config:
        return baseAdaptor

    # 支持配置别名
    backend_config: dict = server_config[backend_alias]
    backend = backend_config.get('platform', backend_alias)
    if backend not in SUPPORTTED_BACKENDS:
        raise RuntimeError(f"无效云平台类型，仅支持{list(SUPPORTTED_BACKENDS)}")
    cls: type[BaseAdaptor] = SUPPORTTED_BACKENDS[backend]
    return cls(config_alias=backend_alias)