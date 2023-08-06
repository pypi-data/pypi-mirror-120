import asyncio
import functools
import importlib
import inspect
import logging
import signal
import threading
from typing import Callable, List

import uvloop

# from .queues import priority_queues, queues
from .consumer import Consumer
from .enums import ServiceEvent, State
from .producer import Producer
from .scheduler import Scheduler
from .task import Task

logger = logging.getLogger(__name__)


class App:
    def __init__(self, config):
        self.config = config

        self.scheduler = Scheduler()
        self.consumer = Consumer()
        self.producer = Producer()

        self.should_exit: bool = False
        self.force_exit: bool = False

        self.on_startup_funcs: List[Callable] = []
        self.on_shutdown_funcs: List[Callable] = []

    @property
    def tasks(self) -> List[Task]:
        return self.scheduler.tasks + list(self.consumer.tasks.values())

    def on_event(self, event: ServiceEvent) -> Callable:
        def _wrapped_on_event(func: Callable) -> Callable:
            @functools.wraps(func)
            async def _callable_on_event() -> None:
                await func()

            if event == ServiceEvent.STARTUP:
                self.on_startup_funcs.append(_callable_on_event)
            elif event == ServiceEvent.SHUTDOWN:
                self.on_shutdown_funcs.append(_callable_on_event)

            return func

        return _wrapped_on_event

    def run(self) -> None:
        uvloop.install()
        asyncio.run(self.serve())

    async def serve(self) -> None:
        self.install_signal_handlers()

        await self.startup()
        await self.main_loop()
        await self.shutdown()

    async def startup(self) -> None:
        self.register_tasks()

        for func in self.on_startup_funcs:
            if inspect.iscoroutinefunction(func):
                await func()
            elif inspect.isfunction(func):
                func()

            if self.should_exit:
                return

        for task in self.tasks:
            task.state = State.STARTING

    async def main_loop(self) -> None:
        self.create_tasks()

        counter = 0
        while not self.should_exit:
            counter += 1
            counter = counter % 864000

            # Check if all Tasks are finished, once per second
            if counter % 10 == 0:
                all_tasks_finished = True
                for task in self.tasks:
                    if task.state not in [State.STOPPED, State.FAILED]:
                        all_tasks_finished = False
                        break
                if all_tasks_finished:
                    self.should_exit = True
                    break

            await asyncio.sleep(0.1)

    async def shutdown(self):
        logger.info("Shutting down")

        # Wait for Tasks to finish
        if not self.force_exit:
            logger.info("Waiting for Tasks to finish. (CTRL+C to force quit)")
            while not self.force_exit:
                all_tasks_finished = True

                for task in self.tasks:
                    if task.state in [State.STOPPED, State.FAILED]:
                        continue
                    elif task.state == State.STOPPING:
                        all_tasks_finished = False
                    else:
                        all_tasks_finished = False
                        task.stop()
                if all_tasks_finished:
                    break
                await asyncio.sleep(0.1)

        # TODO: Wait for `shutdown` sequence
        if not self.force_exit:
            logger.info(
                "Waiting for shutdown sequence to finish. (CTRL+C to force quit)"
            )  # noqa: E501
            for func in self.on_shutdown_funcs:
                if inspect.iscoroutinefunction(func):
                    await func()
                elif inspect.isfunction(func):
                    func()

                if self.should_exit:
                    return

    def register_tasks(self) -> None:
        # Load Tasks from all modules in `autodiscover`
        if self.config.autodiscover is not None:
            for module_path in self.config.autodiscover:
                importlib.import_module(module_path)

        # # Update event loops for any Queues and PriorityQueues
        # loop = asyncio.get_event_loop()
        # for queue in list(queues.values()) + list(priority_queues.values()):
        #     if queue._loop != loop:
        #         queue._loop = loop

    def create_tasks(self):
        def _log_aio_task_exception(aio_task: asyncio.Task) -> None:
            """Log exception stack trace."""
            try:
                aio_task.result()
            except asyncio.CancelledError:
                pass  # Task cancellation should not be logged
            except Exception:
                logger.exception(f"Exception rasied by task: {aio_task}")

        for task in self.tasks:
            aio_task: asyncio.Task = asyncio.create_task(task())
            aio_task.add_done_callback(_log_aio_task_exception)
            task.aio_task = aio_task

    def install_signal_handlers(self) -> None:
        if threading.current_thread() is not threading.main_thread():
            logger.warning("Signals can only be listened to from the main thread")
            return
        loop = asyncio.get_event_loop()
        for sig in [signal.SIGINT, signal.SIGTERM]:
            loop.add_signal_handler(sig, self.handle_exit, sig, None)

    def handle_exit(self, sig, frame):
        if self.should_exit:
            self.force_exit = True
        else:
            self.should_exit = True
