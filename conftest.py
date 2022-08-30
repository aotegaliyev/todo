import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tasks.models import Task
from users.models import Profile


@pytest.fixture
def new_user_factory(db):
    def create_app_user(
        username: str,
        password: str = 'Todo1234',
        first_name: str = 'FirstName',
        last_name: str = 'LastName',
        middle_name: str = 'MiddleName',
        email: str = 'aotegaliyev@gmail.com',
        is_staff: bool = True,
        is_superuser: bool = False,
        is_active: bool = True,
        role: str = 'employee',
        phone: str = None,
    ):

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )

        user.set_password(password)
        user.save()

        Profile.objects.create(
            user=user, middle_name=middle_name, role=role, phone=phone
        )
        return user

    return create_app_user


@pytest.fixture
def admin_user_token(db, new_user_factory, get_token):
    admin = new_user_factory(username='admin', role='admin')
    return admin, get_token(admin)


@pytest.fixture
def employee_user_token(db, new_user_factory, get_token):
    employee = new_user_factory(username='employee', role='employee')
    return employee, get_token(employee)


@pytest.fixture
def second_employee_user_token(db, new_user_factory, get_token):
    employee = new_user_factory(username='employee2', role='employee')
    return employee, get_token(employee)


@pytest.fixture
def client_user_token(db, new_user_factory, get_token):
    client = new_user_factory(username='client', role='client')
    return client, get_token(client)


@pytest.fixture
def get_token():
    def access_token(user):
        client = APIClient()
        response = client.post(
            '/api/v1/token',
            {'username': user.username, 'password': 'Todo1234'},
            format='json',
        )
        return response.data['access']

    return access_token


@pytest.fixture
def task_by_employee(employee_user_token):
    return Task.objects.create(
        author=employee_user_token[0],
        title='Employee task',
        description='Employee task description',
    )


@pytest.fixture
def task_by_second_employee(second_employee_user_token):
    return Task.objects.create(
        author=second_employee_user_token[0],
        title='Second employee task',
        description='Second employee task description',
    )
