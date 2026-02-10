from typing import List
from .models import MemoryItem
import logging


class ScratchMemory:
    def __init__(self):
        self._items: List[MemoryItem] = []
        logging.debug("ScratchMemory initialized")

    def add(self, item: MemoryItem):
        if item.tier != "SCRATCH":
            raise ValueError("Only scratch items allowed")
        self._items.append(item)
        logging.debug(f"Added scratch item: {item}")

    def get_all(self) -> List[MemoryItem]:
        logging.debug("Getting all scratch items")
        return list(self._items)

    def clear(self):
        self._items.clear()
        logging.debug("Cleared scratch items")
