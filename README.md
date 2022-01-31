# PyShellTest

[![Build/Test](https://github.com/bnichs/pyshelltest/actions/workflows/python-test.yml/badge.svg)](https://github.com/bnichs/pyshelltest/actions/workflows/python-test.yml)

Generate python test cases for shell commands based on simple configuration. Allows you to seemlessly test commands that need to be run from a shell but within the python testing framework. 

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

You can then run your tests like you would normally and PyShellTest will generate tests based on your conifg.json
```
python -m pytest tests/
```



#  Configuration
See sample-config.json as well as tests/test-config.json

Example configuration for a command: 
```
{
    "the-command-name": {
        # The command to run
        "command": ["path/to/script.sh"], 
        
        # How long to wait before timing out
        "timeout": 30, 
        
        # Print the output of the ocmmand to stdout
        "print_output": true,
        
        # Expect this in stdout, fail otherwise
        "stdout_contains": "bar" 
          
        # Expect this in stderr, fail otherwise
        "stderr_contains": "bar"
        
        # Set this dict if you expect errors from the command
        "error": { 
            # Expect an error
            "expect": true, 
            
            # Expect an error with this class
            "error_class": "FileNotFoundError"
        },
    }
}
```


# Development 

## Testing
How to test this project


```bash
poetry run python -m pytest 
```