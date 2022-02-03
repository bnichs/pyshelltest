# PyShellTest

[![Build/Test](https://github.com/bnichs/pyshelltest/actions/workflows/python-test.yml/badge.svg)](https://github.com/bnichs/pyshelltest/actions/workflows/python-test.yml)

Generate python test cases for shell commands based on simple configuration. Allows you to seemlessly test commands that need to be run from a shell but within the python testing framework. 

We all need to write more tests and including outside commands allows for more coverage. 
For instance:
* Add linkchecker to your integ runs for a django project
* Ensure tools in `bin/` have a `--help` 


# Installation
```bash
pip install pyshelltest
```

# Integration
Add this to you test files where you see fit: 
```python 
generator = PyShellTestGenerator.from_json("sample-config.json")
generator = PyShellTestGenerator.from_toml("sample-config.toml")
test_class = generator.generate()
```

You can then run your tests like you would normally and PyShellTest will generate tests based on your conifg.json
```
python -m pytest tests/
```


#  Configuration
See `sample-config/` as well as `tests/test-config.toml`

## Toml config
Example configuration for a command:
```toml
[[command]]
 name = "the-command-name"

# The command to run
command = ["path/to/script.sh"]

# How long to wait before timing out
timeout = 30

# Print the output of the ocmmand to stdout
print_output = true

# Expect this in stdout, fail otherwise
stdout_contains = "bar" 
  
# Expect this in stderr, fail otherwise
stderr_contains = "bar"

    # Set this dict if you expect errors from the command
    [command.error] 
    # Expect an error
    expect = true
    
    # Expect an error with this class
    error_class = "FileNotFoundError"
```


## Json config
Example configuration for a command: 
```json
{
    "command": [
         {
            "_comment":  "# The command name",
            "name": "the-command-name",
            
            "_comment":  "# The command to run",
            "command": ["path/to/script.sh"], 
            
            "_comment":  "# How long to wait before timing out",
            "timeout": 30, 
            
            "_comment":  "# Print the output of the command to stdout",
            "print_output": true,
            
            "_comment":  "# Expect this in stdout, fail otherwise",
            "stdout_contains": "bar" ,
              
            "_comment":  "# Expect this in stderr, fail otherwise",
            "stderr_contains": "bar",
            
            "_comment":  "# Set this dict if you expect errors from the command",
            "error": { 
                "_comment":  "# Expect an error",
                "expect": true,
                
                "_comment":  "# Expect an error with this class",
                "error_class": "FileNotFoundError"
            }
        }
    ]
}
```


# Development 

## Testing
How to test this project


```bash
poetry run python -m pytest 
```