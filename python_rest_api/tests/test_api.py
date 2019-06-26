import json

from order_api.api import OrderApi


class TestOrderApi:

    def test_order_list_file_repo_success(self, file_mock):
        # arrange
        file_contents = '{"orders": [{"order_id": "12345", "user_id": 1, "items": [1, 2], "status": "CREATED"}]}'
        file_mock.return_value.read.return_value = file_contents
        payload = {}

        # act
        response = OrderApi(payload).list()

        # assert
        assert response['status_code'] == '200'
        assert response['body'] == '[{"order_id": "12345", "user_id": 1, "items": [1, 2], "status": "CREATED"}]'

    def test_add_order_file_repo_success(self, file_mock):
        # arrange
        file_contents = '{"orders": [{"order_id": "12345", "user_id": 1, "items": [1, 2], "status": "CREATED"}]}'
        file_mock.return_value.read.return_value = file_contents
        payload = {"user_id": 1, "items": [1, 2]}

        # act
        response = OrderApi(payload).add()

        # assert
        assert response['status_code'] == '200'
        response_dict = json.loads(response['body'])
        assert response_dict['order_id'] is not None
        assert response_dict['user_id'] == 1
        assert response_dict['items'] == [1, 2]
        assert response_dict['status'] == "CREATED"
