from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Callable, Coroutine, Optional

from .enums import State

logger = logging.getLogger(__name__)


class Task:
    def __init__(
        self,
        func: Callable,
        *,
        name: str = None,
        max_retries: int = None,
        retry_delay: float = None,
    ):
        self.func = func
        self.name = name or func.__name__
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.state = State.STOPPED

        self.aio_task: Optional[asyncio.Task] = None

    def __call__(self) -> Coroutine:
        return self.func()

    def __repr__(self) -> str:
        return f"Task('{self.name}')"

    async def sleep(self, interval: float) -> None:
        logger.debug(f"{self} SLEEPING for {interval} seconds")
        self.state = State.SLEEPING
        await asyncio.sleep(interval)
        if self.state != State.STOPPING:
            logger.debug(f"{self} IDLE")
            self.state = State.IDLE

    async def run_wrapped(self, *args, **kwargs) -> Any:
        wrapped_func = self.func.__wrapped__  # type: ignore[attr-defined]

        logger.debug(f"{self} RUNNING")
        self.state = State.RUNNING

        retry_count = 1
        while True:
            # Run wrapped func
            try:
                if inspect.iscoroutinefunction(wrapped_func):
                    yield await wrapped_func(*args, **kwargs)
                elif inspect.isasyncgenfunction(wrapped_func):
                    async for res in wrapped_func(*args, **kwargs):
                        yield res
                elif inspect.isfunction(wrapped_func):
                    yield wrapped_func(*args, **kwargs)
                break

            except Exception as e:
                # No retries. Cancel asyncio Task
                if self.max_retries is None:
                    logger.exception(f"{self} FAILED. Reason: {e}")
                    self.state = State.FAILED
                    return

                # Max retries met. Cancel asyncio Task
                elif retry_count > self.max_retries:
                    logger.exception(f"{self} FAILED (Max retries met). Reason: {e}")
                    self.state = State.FAILED
                    return

                # Update retry count and sleep
                else:
                    logger.info(f"{self} RETRYING (attempt {retry_count}). Reason: {e}")
                    self.state = State.RETRYING
                    retry_count += 1
                    if self.retry_delay is not None:
                        await asyncio.sleep(self.retry_delay)

        # On a successful call of `wrapped_func`, update the status of the Task
        # to 'IDLE' if it isn't already 'STOPPING'.
        if self.state != State.STOPPING:
            logger.debug(f"{self} IDLE")
            self.state = State.IDLE

    def stop(self):
        """Stop the Task from continuing future runs.

        This should only be called *outside* of the Task's `aio_task` context.
        """
        assert self.aio_task is not None, f"{self} has not started yet"

        # Immediately cancel the asyncio Task if the Task is STARTING, IDLE, or SLEEPING
        if self.state in [State.STARTING, State.IDLE, State.SLEEPING]:
            self.state = State.STOPPED
            self.aio_task.cancel()

        # Update Task status to STOPPING and add a callback to update status to STOPPED
        elif self.state in [State.RUNNING, State.RETRYING]:
            self.state = State.STOPPING

            def _update_task_state(aio_task: asyncio.Task) -> None:
                self.state = State.STOPPED

            self.aio_task.add_done_callback(_update_task_state)
