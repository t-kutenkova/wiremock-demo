import logging
import os
import sys

sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/..")

import pytest
from colorama import Fore, Style

from helpers.http_helper import HTTPHelper
from helpers.mocker import Mocker

log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def mocker():
    return Mocker()


@pytest.fixture(scope="session")
def http():
    return HTTPHelper(host="localhost", protocol=HTTPHelper.HTTP, port=8080)


def log_info_blue(msg):
    log.info(f"\n{Fore.BLUE}{Style.BRIGHT}{msg}{Style.RESET_ALL}")


def log_info_magenta(msg):
    log.info(f"\n{Fore.MAGENTA}{Style.BRIGHT}{msg}{Style.RESET_ALL}")
