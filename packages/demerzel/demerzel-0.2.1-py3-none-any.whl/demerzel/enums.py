from enum import Enum


class State(str, Enum):
    STARTING = "STARTING"
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    RETRYING = "RETRYING"
    SLEEPING = "SLEEPING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


class ServiceEvent(str, Enum):
    STARTUP = "startup"
    SHUTDOWN = "shutdown"
