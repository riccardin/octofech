from abc import ABC, abstractmethod
from typing import List, Dict

class BaseConnector(ABC):
    def __init__(self, config: Dict):
        self.config = config

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def fetch(self, **kwargs) -> List[Dict]:
        """Return a list of dicts representing items to be normalized."""
        ...