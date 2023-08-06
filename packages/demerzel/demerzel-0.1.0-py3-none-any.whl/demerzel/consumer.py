import functools
import logging
from typing import Callable, Dict

from .enums import State
from .queues import priority_queues, queues
from .task import Task
from .utils.asyncio import PriorityQueue, Queue

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}

    def queue(
        self,
        name: str,
        *,
        max_retries: int = None,
        retry_delay: float = None,
        workers: int = 1,
    ) -> Callable:
        """Register a function to receive items from a Queue.

        Should be used as a decorator for a sync or async function at the "outer-most"
        level as `_queue_wrapper` returns the wrapped function and not `queue_callable`
        (which doesn't take any args or kwargs anyways).

        On shutdown, the Task will keep running until the Queue is empty.

        Args:
            name (str): The Queue's name.
            workers (int, optional): The number of asynchronous workers to run
                concurrently. N Tasks will be registered for the service. Defaults to 1.

        Returns:
            Callable: A callable that wraps a function.
        """
        if name not in queues:
            logger.debug(f"Creating Queue('{name}')")
            queues[name] = Queue()

        def _queue_wrapper(func: Callable) -> Callable:
            """Registers Tasks for the Consumer object."""
            for i in range(workers):
                task_id = len(self.tasks)

                @functools.wraps(func)
                async def _queue_callable(task_id=task_id) -> None:
                    """Awaits a Queue and runs the wrapped function."""
                    q = queues[name]
                    task = self.tasks[task_id]

                    stop_states = [State.STOPPING, State.STOPPED, State.FAILED]
                    while task.state not in stop_states or not q.empty():
                        logger.debug(f"Awaiting Queue('{name}')")
                        res = await q.get()
                        async for _ in task.run_wrapped(res):
                            pass

                task_name = f"{func.__name__}_{i + 1}" if workers > 1 else None
                task = Task(
                    _queue_callable,
                    name=task_name,
                    max_retries=max_retries,
                    retry_delay=retry_delay,
                )
                self.tasks[task_id] = task

            return func

        return _queue_wrapper

    def priority_queue(
        self,
        name: str,
        *,
        max_retries: int = None,
        retry_delay: float = None,
        workers: int = 1,
    ) -> Callable:
        if name not in priority_queues:
            logger.debug(f"Creating PriorityQueue('{name}')")
            priority_queues[name] = PriorityQueue()

        def _priority_queue_wrapper(func: Callable) -> Callable:

            for i in range(workers):
                task_id = len(self.tasks)

                @functools.wraps(func)
                async def _priority_queue_callable(task_id=task_id) -> None:
                    pq = priority_queues[name]
                    task = self.tasks[task_id]

                    stop_states = [State.STOPPING, State.STOPPED, State.FAILED]
                    while task.state not in stop_states or not pq.empty():
                        logger.debug(f"Awaiting PriorityQueue('{name}')")
                        priority, res = await pq.get()
                        async for _ in task.run_wrapped(priority, res):
                            pass

                task_name = f"{func.__name__}_{i + 1}" if workers > 1 else None
                task = Task(
                    _priority_queue_callable,
                    name=task_name,
                    max_retries=max_retries,
                    retry_delay=retry_delay,
                )
                self.tasks[task_id] = task

            return func

        return _priority_queue_wrapper
