import pytest
from unittest.mock import mock_open, patch


@pytest.fixture
def file_mock():
    local_mock = mock_open()
    with patch('order_api.file_repo.open', local_mock):
        yield local_mock
