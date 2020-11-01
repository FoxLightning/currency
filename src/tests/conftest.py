from account.models import User

import pytest


@pytest.fixture(autouse=True, scope="function")
def enable_db_access_for_all_tests(db):
    """
    give access to database for all tests
    """


@pytest.fixture(scope='function')
def admin():
    user = User.objects.create(
        username='admin',
        email='a@mai.com',
        is_staff=True,
        is_active=True,
        is_superuser=True,
    )
    yield user
