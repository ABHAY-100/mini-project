from typing import Dict, List
from .models import MemoryItem
from .crypto import verify_item
import logging


class LongTermMemory:
    def __init__(self, agent_public_key):
        self._items: Dict[str, MemoryItem] = {}
        self._agent_public_key = agent_public_key
        logging.debug("LongTermMemory initialized")

    def add(self, item: MemoryItem):
        if item.tier != "LONGTERM":
            raise ValueError("Only long-term items allowed")

        if item.signature is None:
            raise ValueError("Unsigned memory cannot enter long-term storage")

        if not verify_item(item, self._agent_public_key):
            raise ValueError("Signature verification failed")

        self._items[item.id] = item
        logging.debug(f"Added long-term item: {item}")

    def get(self, memory_id: str) -> MemoryItem:
        item = self._items[memory_id]
        logging.debug(f"Getting long-term item: {item}")
        if not verify_item(item, self._agent_public_key):
            raise ValueError("Memory integrity check failed")
        return item

    def get_all_verified(self) -> List[MemoryItem]:
        verified = []
        logging.debug("Getting all verified long-term items")
        for item in self._items.values():
            if verify_item(item, self._agent_public_key):
                verified.append(item)
        return verified
