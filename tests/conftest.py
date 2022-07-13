# conftest.py
import pytest
import logging


@pytest.fixture(autouse=True, scope="function")
def log_request(request):
    logger = logging.getLogger()
    logger.info(f"Starting test {request.function.__name__}")
    yield
    logger.info(f"{request.function.__name__} is done!")
