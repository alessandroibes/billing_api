import os
import pytest

from unittest import mock

from api.application_layer.use_cases.upload import ProcessFileException, UploadUseCase
from api.domain_layer.models.billing import Billing
from api.presentation_layer.utils import Utils

module_dir = os.path.dirname(os.path.abspath(__file__))
file_with_content = os.path.join(module_dir, '..', '..', '..', 'resources', 'file_with_content.csv')


@mock.patch.object(Utils, "read_csv")
@mock.patch.object(Billing, "process_billing")
@pytest.mark.asyncio
async def test_process_file_must_end_successfully_when_success(
    process_billing_mock,
    read_csv_mock
):
    read_csv_mock.return_value = [{
        "name":"John Doe",
        "governmentId":"11111111111",
        "email":"johndoe@kanastra.com.br",
        "debtAmount":1000000.00,
        "debtDueDate":"2022-10-12",
        "debtId":"1adb6ccf-ff16-467f-bea7-5f05d494280f"
    }]
    process_billing_mock.return_value = None
    
    with open(file_with_content, "rb") as file:
        data = file.read()
        await UploadUseCase.process_file(data=data)

    read_csv_mock.assert_called_once()
    process_billing_mock.assert_called_once()


@mock.patch.object(Utils, "read_csv")
@mock.patch.object(Billing, "process_billing")
@pytest.mark.asyncio
async def test_process_file_must_raise_process_file_exception_when_read_csv_raise_exception(
    process_billing_mock,
    read_csv_mock
):
    read_csv_mock.side_effect = Exception("Generic exception")
    process_billing_mock.return_value = None

    with pytest.raises(
        ProcessFileException,
        match="Generic exception",
    ):
        with open(file_with_content, "rb") as file:
            data = file.read()
            await UploadUseCase.process_file(data=data)


@mock.patch.object(Utils, "read_csv")
@mock.patch.object(Billing, "process_billing")
@pytest.mark.asyncio
async def test_process_file_must_end_successfully_when_process_billing_raise_exception(
    process_billing_mock,
    read_csv_mock
):
    read_csv_mock.return_value = [{
        "name":"John Doe",
        "governmentId":"11111111111",
        "email":"johndoe@kanastra.com.br",
        "debtAmount":1000000.00,
        "debtDueDate":"2022-10-12",
        "debtId":"1adb6ccf-ff16-467f-bea7-5f05d494280f"
    }]
    process_billing_mock.side_effect = Exception("Generic exception")
    
    with open(file_with_content, "rb") as file:
        data = file.read()
        await UploadUseCase.process_file(data=data)

    read_csv_mock.assert_called_once()
    process_billing_mock.assert_called_once()
