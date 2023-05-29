from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base_service import RemoteServer, BackendConnectionException


class SqlalchemyServer(RemoteServer):
    """SQL Server"""
    def __init__(self, url: str, **kwargs):
        """Init

        Args:
            url: url
            **kwargs: 其余参数
        """
        super().__init__()

        self.url = url

        self.connect()
        self.ping()

    def __repr__(self) -> str:
        return f"sqlalchemy: {self.url}"

    def connect(self) -> bool:
        try:
            self.stub = create_engine(self.url, pool_size=8, pool_recycle=60*30)
        except Exception as ex:
            self.stub = None

            self.logger.error('failed to connect {}: {}'.format(self, ex))
            return False
        else:
            return True

    def _maybe_reconnect(self):
        if self.stub is None and not self.connect():
            raise BackendConnectionException()

    def ping(self) -> bool:
        try:
            self._maybe_reconnect()

            return True
        except:
            return False

    def session(self):
        """获取session对象"""
        self._maybe_reconnect()

        Session = sessionmaker(bind=self.stub)
        session = Session()

        return session

    def create_all(self, base):
        """创建数据库"""
        self._maybe_reconnect()

        base.metadata.create_all(self.stub)


import yaml
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import Table


with open("./conf/http.yml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
ss = SqlalchemyServer(url=data["hubble_service"]["url"])
session = ss.session()

Base = declarative_base()
metadata = Base.metadata
metadata.bind = ss.stub


class DBBase(Base):
    __table__ = Table("online_task", metadata, autoload=True)


a = session.query(DBBase).limit(1).all()
print(a)

