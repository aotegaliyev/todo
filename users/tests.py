import logging

logger = logging.getLogger('django-info')


def test_user_is_admin(admin_user_token):
    admin, _ = admin_user_token
    assert admin.profile.role == 'admin'


def test_user_is_employee(employee_user_token):
    employee, _ = employee_user_token
    assert employee.profile.role == 'employee'


def test_user_is_client(client_user_token):
    client, _ = client_user_token
    assert client.profile.role == 'client'
