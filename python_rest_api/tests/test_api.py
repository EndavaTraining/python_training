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
