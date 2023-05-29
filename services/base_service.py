# encoding=utf-8
import uuid
from loguru import logger


class BackendConnectionException(Exception):
    """后端服务连接异常"""
    pass


class RemoteServer(object):
    """远程服务器基类"""
    def __init__(self, **kwargs):
        self.logger = logger

    def ping(self) -> bool:
        """ping，用于探活"""
        raise NotImplementedError()

    def connect(self) -> bool:
        """连接客户端"""
        raise NotImplementedError()

    def _maybe_reconnect(self):
        """自动判断当前连接是否需要重连"""
        raise NotImplementedError()

    def get_log_id(self) -> str:
        """生成日志id"""
        return 'logid-{}'.format(str(uuid.uuid1()))

    def __repr__(self) -> str:
        raise NotImplementedError()


