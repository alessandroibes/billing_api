import os

module_dir = os.path.dirname(os.path.abspath(__file__))
file_with_content = os.path.join(module_dir, '..', 'resources', 'file_with_content.csv')
file_without_content = os.path.join(module_dir, '..', 'resources', 'file_without_content.csv')
file_with_missing_content = os.path.join(module_dir, '..', 'resources', 'file_with_missing_content.csv')


def test_upload_file_must_return_200_when_file_is_valid(client):
    with open(file_with_content, "rb") as file:
        response = client.post("/upload/", files={"file": file})

    assert response.status_code == 200
    assert response.json() == {"detail": "File received, processing started."}


def test_upload_file_must_return_400_when_no_file(client):
    response = client.post("/upload/", files={"file": None})

    assert response.status_code == 400
    assert response.json() == {"detail": "There was an error parsing the body"}


def test_upload_file_must_return_200_with_log_message_when_file_is_empty(client, caplog):
    with open(file_without_content, "rb") as file:
        response = client.post("/upload/", files={"file": file})

    assert response.status_code == 200
    assert "No data: empty file." in caplog.text


def test_upload_file_must_return_200_with_log_message_when_process_file_raise_key_error(client, caplog):
    with open(file_with_missing_content, "rb") as file:
        response = client.post("/upload/", files={"file": file})

    assert response.status_code == 200
    assert "Missing 'debtId'" in caplog.text