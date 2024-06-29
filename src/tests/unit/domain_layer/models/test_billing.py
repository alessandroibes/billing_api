import pytest

from unittest.mock import Mock

from api.domain_layer.models.billing import Billing
from api.domain_layer.ports.billing_service import BillingService
from api.domain_layer.ports.communication_service import CommunicationService


@pytest.fixture()
def boleto_service_mock():
    class BoletoService(BillingService):
        @classmethod
        async def generate_billing(cls, billing: Billing) -> bool:
            if (billing.governmentId == "22222222222"):
                return False
            
            return True
        
    return Mock(wraps=BoletoService)


@pytest.fixture()
def email_service_mock():
    class EmailService(CommunicationService):
        @classmethod
        async def send_message(cls, to: str, message: str):
            return
        
    return Mock(wraps=EmailService)


@pytest.mark.asyncio
async def test_process_billing_must_generate_billing_and_send_email_when_success(
    boleto_service_mock,
    email_service_mock
):
    billing_data_dict = {
        "name":"John Doe",
        "governmentId":"11111111111",
        "email":"johndoe@kanastra.com.br",
        "debtAmount":1000000.00,
        "debtDueDate":"2022-10-12",
        "debtId":"1adb6ccf-ff16-467f-bea7-5f05d494280f"
    }

    await Billing.process_billing(
        billing_data=billing_data_dict,
        using_billing_service=boleto_service_mock,
        using_communication_service=email_service_mock
    )

    boleto_service_mock.generate_billing.assert_called_once()
    email_service_mock.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_process_billing_must_not_send_email_when_generate_billing_return_false(
    boleto_service_mock,
    email_service_mock
):
    billing_data_dict = {
        "name":"John Doe",
        "governmentId":"22222222222",
        "email":"johndoe@kanastra.com.br",
        "debtAmount":1000000.00,
        "debtDueDate":"2022-10-12",
        "debtId":"1adb6ccf-ff16-467f-bea7-5f05d494280f"
    }

    await Billing.process_billing(
        billing_data=billing_data_dict,
        using_billing_service=boleto_service_mock,
        using_communication_service=email_service_mock
    )

    boleto_service_mock.generate_billing.assert_called_once()
    email_service_mock.send_message.assert_not_called()
