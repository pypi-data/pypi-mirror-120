import functools
import logging
from datetime import datetime
from typing import Callable, List

from croniter import croniter
from pytz import timezone

from .enums import State
from .task import Task

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.tasks: List[Task] = []

    def cron(
        self,
        stmt: str,
        *,
        tz: str = "UTC",
        eager: bool = False,
        max_retries: int = None,
        retry_delay: float = None,
    ) -> Callable:
        def _cron_wrapper(func: Callable) -> Callable:

            task: Task = None  # type: ignore[assignment]

            @functools.wraps(func)
            async def _cron_callable() -> None:
                if eager:
                    logger.debug(f"Running {task} eagerly")
                    async for _ in task.run_wrapped():
                        pass

                while task.state not in [State.STOPPING, State.STOPPED, State.FAILED]:
                    # Calculate sleep seconds
                    dt_now = datetime.now(tz=timezone(tz))
                    cron_iter = croniter(stmt, dt_now)
                    while True:
                        next_dt = cron_iter.get_next(datetime)
                        sleep_sec = (next_dt - dt_now).seconds
                        if sleep_sec > 0:
                            break

                    await task.sleep(sleep_sec)
                    async for _ in task.run_wrapped():
                        pass

            task = Task(
                _cron_callable, max_retries=max_retries, retry_delay=retry_delay
            )
            self.tasks.append(task)

            return func

        return _cron_wrapper

    def timer(
        self,
        interval: float,
        *,
        eager: bool = False,
        max_retries: int = None,
        retry_delay: float = None,
    ) -> Callable:
        def _timer_wrapper(func: Callable) -> Callable:

            task: Task = None  # type: ignore[assignment]

            @functools.wraps(func)
            async def _timer_callable() -> None:
                if eager:
                    logger.debug(f"Running {task} eagerly")
                    async for _ in task.run_wrapped():
                        pass

                while task.state not in [State.STOPPING, State.STOPPED, State.FAILED]:
                    await task.sleep(interval)
                    async for _ in task.run_wrapped():
                        pass

            task = Task(
                _timer_callable, max_retries=max_retries, retry_delay=retry_delay
            )
            self.tasks.append(task)

            return func

        return _timer_wrapper
