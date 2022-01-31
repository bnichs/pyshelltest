from pyshelltest import PyShellTestGenerator


generator = PyShellTestGenerator.from_json("tests/test-config.json")
test_class = generator.generate()
