import logging

from pyshelltest import PyShellTestGenerator
from tests.config import CONFIG_FILE

logger = logging.getLogger(__name__)



# Generate our shell tests like a consumer would
generator = PyShellTestGenerator.from_toml(CONFIG_FILE)
test_class = generator.generate()

