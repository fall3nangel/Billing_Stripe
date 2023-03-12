import asyncio
from functools import lru_cache

import aio_pika
import backoff
from aio_pika.abc import AbstractRobustConnection
from fastapi import Depends

from core.config import settings
from services.queue import QueueService

rabbitmq: AbstractRobustConnection | None = None


@backoff.on_exception(backoff.expo, aio_pika.exceptions.AMQPConnectionError)
async def get_rabbitmq():
    rabbitmq = await aio_pika.connect_robust(
        host=settings.rabbitmq.server,
        port=settings.rabbitmq.port,
        login=settings.rabbitmq.user,
        password=settings.rabbitmq.password,
        loop=asyncio.get_event_loop(),
    )
    return rabbitmq


async def close_rabbitmq():
    await rabbitmq.close()


@lru_cache()
def get_queue_service(
    rabbit: AbstractRobustConnection = Depends(get_rabbitmq),
) -> QueueService:
    return QueueService(rabbit)
