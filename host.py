from abc import ABC, abstractmethod
from datetime import datetime
from config import REFRESH_TIME_OK, REFRESH_TIME_FAIL, PULL_TIME_OK, PULL_TIME_FAIL

class GitHost(ABC):
    next_pulls: dict[str, datetime]
    next_refreshes: dict[str, datetime]

    def __init__(self) -> None:
        super().__init__()
        self.next_pulls = {}
        self.next_refreshes = {}
        self._reload()

    def should_refresh(self, id: str) -> bool:
        if id not in self.next_refreshes:
            return True
        return self.next_refreshes[id] <= datetime.now()

    def should_pull(self, id: str) -> bool:
        if id not in self.next_pulls:
            return True
        return self.next_pulls[id] <= datetime.now()

    def report_refresh(self, id: str, success: bool) -> None:
        if success:
            self.next_refreshes[id] = datetime.now() + REFRESH_TIME_OK
        else:
            self.next_refreshes[id] = datetime.now() + REFRESH_TIME_FAIL

    def report_pull(self, id: str, success: bool) -> None:
        if success:
            self.next_pulls[id] = datetime.now() + PULL_TIME_OK
        else:
            self.next_pulls[id] = datetime.now() + PULL_TIME_FAIL

    def _reload(self) -> None:
        pass

    def _should_serialize(self, k: str) -> bool:
        return k[0] != "_"

    def __getstate__(self) -> dict:
        dict = {
            "__version": self.data_version(),
        }

        for k, v in self.__dict__.items():
            if not self._should_serialize(k):
                continue
            dict[k] = v

        return dict

    def __setstate__(self, dict: dict) -> None:
        if dict["__version"] != self.data_version():
            raise ValueError(f"Wrong version (expected={self.data_version()}, actual={dict['__version']})")

        for k, v in dict.items():
            if not self._should_serialize(k):
                continue
            setattr(self, k, v)
        self._reload()

    @abstractmethod
    def refresh(self, force: bool = False) -> bool:
        pass

    @abstractmethod
    def pull(self, force: bool = False) -> bool:
        pass
    
    @staticmethod
    @abstractmethod
    def name(*args) -> str:
        pass

    @staticmethod
    def data_version(*args) -> int:
        return 3
