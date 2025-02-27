import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_devops_lab.settings")

import django
django.setup()

from rest_framework.test import APIClient
from django.core.management import call_command

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    pass

@pytest.fixture(scope='function', autouse=True)
def clear_db(django_db_blocker):
    with django_db_blocker.unblock():
        call_command("flush", "--noinput")

@pytest.fixture
def api_client():
    return APIClient()