from abc import ABC

from api.domain_layer.models.billing import Billing


class BillingService(ABC):
    @classmethod
    async def generate_billing(cls, billing: Billing) -> bool:
        raise NotImplementedError
