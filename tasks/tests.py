import json
from rest_framework.test import APIClient


class TestTasksEndpoints:

    endpoint = '/api/v1/tasks'
    client = APIClient()
    create_request_data = {
        'title': 'Play music',
        'description': 'Learn to play guitar',
        'deadline': '2021-10-21 12:12:00',
        'priority': 'important',
    }

    update_request_data = {
        'title': 'Play tennis',
        'description': 'Learn to play tennis',
        'deadline': '2021-10-22 12:12:00',
        'priority': 'urgent',
    }

    def test_admin_can_get_list_of_tasks(self, admin_user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_user_token[1])
        admin_response = self.client.get(self.endpoint)

        assert admin_response.status_code == 200

    def test_employee_can_get_list_of_tasks(self, employee_user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + employee_user_token[1])
        employee_response = self.client.get(self.endpoint)

        assert employee_response.status_code == 200

    def test_client_can_get_list_of_tasks(self, client_user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + client_user_token[1])
        client_response = self.client.get(self.endpoint)

        assert client_response.status_code == 200

    def test_employee_can_create_a_task(self, employee_user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + employee_user_token[1])

        response = self.client.post(
            self.endpoint, data=self.create_request_data, format='json'
        )

        assert response.status_code == 201
        assert json.loads(response.content)['id'] == 1

    def test_admin_can_not_create_a_task(self, admin_user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_user_token[1])
        response = self.client.post(
            self.endpoint, data=self.create_request_data, format='json'
        )

        assert response.status_code == 403

    def test_client_can_not_create_a_task(self, client_user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + client_user_token[1])
        response = self.client.post(
            self.endpoint, data=self.create_request_data, format='json'
        )

        assert response.status_code == 403

    def test_admin_can_update_any_task(self, task_by_employee, admin_user_token):
        url = f'{self.endpoint}/{task_by_employee.id}'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_user_token[1])
        response = self.client.put(url, self.update_request_data, format='json')

        assert response.status_code == 200
        assert (
            json.loads(response.content)['title'] == self.update_request_data['title']
        )

    def test_employee_cant_update_another_task(
        self, task_by_second_employee, employee_user_token
    ):
        url = f'{self.endpoint}/{task_by_second_employee.id}'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + employee_user_token[1])
        response = self.client.put(url, self.update_request_data, format='json')

        assert response.status_code == 403

    def test_employee_can_update_own_task(self, task_by_employee, employee_user_token):
        url = f'{self.endpoint}/{task_by_employee.id}'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + employee_user_token[1])
        response = self.client.put(url, self.update_request_data, format='json')

        assert response.status_code == 200
        assert (
            json.loads(response.content)['title'] == self.update_request_data['title']
        )

    def test_employee_cant_delete_another_task(
        self, task_by_second_employee, employee_user_token
    ):
        url = f'{self.endpoint}/{task_by_second_employee.id}'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + employee_user_token[1])
        response = self.client.delete(url)

        assert response.status_code == 403

    def test_employee_can_delete_own_task(self, task_by_employee, employee_user_token):
        url = f'{self.endpoint}/{task_by_employee.id}'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + employee_user_token[1])
        response = self.client.delete(url)

        assert response.status_code == 204

    def test_admin_can_delete_any_task(self, task_by_second_employee, admin_user_token):
        url = f'{self.endpoint}/{task_by_second_employee.id}'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_user_token[1])
        response = self.client.delete(url)

        assert response.status_code == 204
