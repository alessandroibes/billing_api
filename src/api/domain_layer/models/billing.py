import logging

from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Type
from uuid import UUID

logger = logging.getLogger("billing_api." + __name__)


class Billing(BaseModel):
    name: str
    governmentId: str
    email: EmailStr
    debtAmount: float
    debtDueDate: date
    debtId: UUID

    @classmethod
    async def process_billing(
        cls,
        billing_data: dict,
        using_billing_service: Type["BillingService"],
        using_communication_service: Type["CommunicationService"]
    ):
        logger.info(f"Processing billing for {billing_data['name']} with amount {billing_data['debtAmount']}.")

        billing = Billing(**billing_data)

        if (await using_billing_service.generate_billing(billing)):
            await using_communication_service.send_message(
                to = billing.name,
                message = f"Boleto gerado com sucesso, acesse http://kanastra/boleto/{str(billing.debtId)}."
            )
