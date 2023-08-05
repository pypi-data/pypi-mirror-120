"""Support Peewee ORM with asyncio."""


__version__ = "0.6.0"


from .model import AIOModel as Model  # noqa
from .manager import Manager  # noqa
