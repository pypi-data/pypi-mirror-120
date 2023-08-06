from typing import Dict

from .utils.asyncio import PriorityQueue, Queue

queues: Dict[str, Queue] = {}
priority_queues: Dict[str, PriorityQueue] = {}
