import functools
import inspect
import logging
from typing import Callable

from .queues import priority_queues, queues
from .utils.asyncio import PriorityQueue, Queue

logger = logging.getLogger(__name__)


class Producer:
    def queue(self, name: str) -> Callable:
        if name not in queues:
            logger.debug(f"Creating Queue('{name}')")
            queues[name] = Queue()

        def _queue_wrapper(func: Callable) -> Callable:
            @functools.wraps(func)
            async def _queue_callable(*args, **kwargs) -> None:
                q = queues[name]

                if inspect.iscoroutinefunction(func):
                    res = await func(*args, **kwargs)
                    logger.debug(f"Adding item to Queue('{name}')")
                    await q.put(res)
                elif inspect.isasyncgenfunction(func):
                    async for res in func(*args, **kwargs):
                        logger.debug(f"Adding item to Queue('{name}')")
                        await q.put(res)
                elif inspect.isfunction(func):
                    res = func(*args, **kwargs)
                    logger.debug(f"Adding item to Queue('{name}')")
                    await q.put(res)

            return _queue_callable

        return _queue_wrapper

    def priority_queue(self, name: str, *, priority: int) -> Callable:
        if name not in priority_queues:
            priority_queues[name] = PriorityQueue()

        def _wrapper(func: Callable) -> Callable:
            @functools.wraps(func)
            async def _producer_wrapper(*args, **kwargs) -> None:
                pq = priority_queues[name]

                if inspect.iscoroutinefunction(func):
                    res = await func(*args, **kwargs)
                    await pq.put((priority, res))
                elif inspect.isasyncgenfunction(func):
                    async for res in func(*args, **kwargs):
                        logger.debug(f"Adding priority {priority} item to '{name}'")
                        await pq.put((priority, res))
                elif inspect.isfunction(func):
                    res = func(*args, **kwargs)
                    await pq.put((priority, res))

            return _producer_wrapper

        return _wrapper
