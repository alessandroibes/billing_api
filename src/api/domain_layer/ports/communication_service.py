from abc import ABC


class CommunicationService(ABC):
    @classmethod
    async def send_message(cls, to: str, message: str):
        raise NotImplementedError