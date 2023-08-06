import multiprocessing
from .cache_backend import CacheInterface
from typing import Dict, List
from linetimer import CodeTimer
from .cache_logger import CacheLoggerHandler
import logging
import uuid
from enum import Enum


class Progress(str, Enum):
    # str mixin, to be able to compare enums to strings. cool trick! see https://stackoverflow.com/a/63028809/12438690
    QUEUED = "queued"
    DRAIN_ORDERED = "drain"
    DRAIN_READY = "drained"
    LOADING = "load"
    COMPLETE = "complete"


class WorkerBase(multiprocessing.Process):
    cache_backend: CacheInterface = None
    cache_backend_params: Dict = None

    def __init__(self):
        super(WorkerBase, self).__init__()
        self.tags: List[str] = []
        self.params: Dict = {}
        self.timer: CodeTimer = CodeTimer(silent=True, unit="s")
        self.cache: CacheInterface = None
        self.id: str = uuid.uuid4().hex
        self.progress: Progress = Progress.QUEUED

    def run(self):
        pass

    def get_logger(self) -> logging.Logger:
        if self.cache:
            logging.basicConfig(level=logging.INFO, handlers=[])
            log = logging.getLogger(self.name)
            log.addHandler(CacheLoggerHandler(self.cache))
            return log
        else:
            raise KeyError(
                "WorkerBase self.cache is None. Initate cache backed first before call 'get_logger'"
            )


class WorkerPlaceHolder:
    """In some cases/systems joined and closed processes are still counted into ulimit. We need to delete the worker complettly to prevent this.
    But as we want to track closed workers and pull out some informations from them we create a copy from the workers interessing data before deleting.
    This class is the datawrapper/placeholder for these informations.
    """

    @classmethod
    def from_worker(cls, worker: WorkerBase):
        return cls(worker)

    def __init__(self, worker: WorkerBase):
        self.tags: List[str] = worker.tags
        self.params: Dict = worker.params
        self.timer = worker.timer
        self.id: str = worker.id
        self.progress = worker.progress
        if hasattr(worker, "set_meta"):
            self.set_meta = worker.set_meta
