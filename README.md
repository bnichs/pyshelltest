

# PyShellTest


Generate test cases for shell commands based on simple configuration. Allows you to seemlessly test commands that need to be run from a shell but within the python testing framework. 

We all need to write more tests and including outside commands allows for more coverage. 
For instance:
* Add linkchecker to your integ runs for a django project
* Ensure tools in `bin/` have a `--help` 


# Installation
TODO

# Integration
Add this to you test files where you see fit: 
```python 
generator = PyShellTestGenerator.from_json("sample-config.json")
test_class = generator.generate()
```



#  Configuration
See sample-config.json