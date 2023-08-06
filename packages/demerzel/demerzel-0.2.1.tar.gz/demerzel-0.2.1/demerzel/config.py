import logging.config
from typing import Dict, List, Union

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}


class Config:
    def __init__(
        self,
        autodiscover: List[str] = None,
        log_config: Dict = None,
        log_level: Union[int, str] = None,
    ):
        self.autodiscover = autodiscover
        self.log_config = log_config
        self.log_level = log_level

        self.configure_logging()

    def configure_logging(self):
        if self.log_config is not None:
            logging.config.dictConfig(self.log_config)

        if self.log_level is not None:
            if isinstance(self.log_level, str):
                log_level = LOG_LEVELS[self.log_level.lower()]
            else:
                log_level = self.log_level
            logging.getLogger("oakcreek.service_gen.service").setLevel(log_level)
            logging.getLogger("oakcreek.service_gen.scheduler").setLevel(log_level)
            logging.getLogger("oakcreek.service_gen.consumer").setLevel(log_level)
            logging.getLogger("oakcreek.service_gen.producer").setLevel(log_level)
            logging.getLogger("oakcreek.service_gen.service_task").setLevel(log_level)
