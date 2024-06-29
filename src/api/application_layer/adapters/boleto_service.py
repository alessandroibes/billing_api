import logging

from api.domain_layer.models.billing import Billing
from api.domain_layer.ports.billing_service import BillingService

logger = logging.getLogger("billing_api." + __name__)


class BoletoService(BillingService):
    @classmethod
    async def generate_billing(cls, billing: Billing) -> bool:
        logger.info(f"Generating boleto for {billing.name} with amount {billing.debtAmount}.")
        return True
