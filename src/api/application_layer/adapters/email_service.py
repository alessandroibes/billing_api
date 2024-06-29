import logging

from api.domain_layer.ports.communication_service import CommunicationService

logger = logging.getLogger("billing_api." + __name__)


class EmailService(CommunicationService):
    @classmethod
    async def send_message(cls, to: str, message: str):
        logger.info(f"Sending message '{message}' to {to}.")
