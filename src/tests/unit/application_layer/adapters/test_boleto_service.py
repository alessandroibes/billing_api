import pytest

from datetime import date
from uuid import uuid4

from api.application_layer.adapters.boleto_service import BoletoService
from api.domain_layer.models.billing import Billing


@pytest.mark.asyncio
async def test_generate_billing(caplog):
    boleto = Billing(
        name="John Doe",
        governmentId="11111111111",
        email="johndoe@kanastra.com.br",
        debtAmount=1000000.00,
        debtDueDate=date(2022, 10, 12),
        debtId=uuid4())
    
    boleto_service = BoletoService()
    result = await boleto_service.generate_billing(boleto)

    assert result is True
    assert f"Generating boleto for {boleto.name} with amount {boleto.debtAmount}." in caplog.text
