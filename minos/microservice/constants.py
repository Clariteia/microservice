"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from os import getenv
from pathlib import Path

DEFAULT_CONFIGURATION_FILE_PATH = Path(getenv("MINOS_CONFIGURATION_FILE_PATH", "./config.yml"))
