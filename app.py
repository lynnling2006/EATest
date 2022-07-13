import os
import pytest

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
LOG_PATH = os.path.join(BASE_DIR, "logs")
