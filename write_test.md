

## How to add new tests?

- The structure which is should maintained while adding new tests is as follows:
```
 TestingFramework
 ├── tests
 │   ├── testfolder
 │       └── test_testname.py

 ```
- All the tests should be self contained amd executable, and each test should have a main function.
- Make sure you inherit the parent class `Test` and import the `TestBase.py` file in every test file, this parent class
implements the output configuration. 

- Each test file should return an exit code. 
   
- Every parameter should be added in the yaml file, the structure is given below.

Structure of yaml file

```yaml
directory_name: # Directory containing the test file
    test_name: # if test file is test_docker.py use "docker" as test_name
        parameters: # Should be same as provided in the constructor
        
```

Append the new parameters into the relevant list given in [check_input_validity function](https://github.com/Divya063/TestingFramework/blob/c951f29802d90380a03b841c0f8752bcfe9cf737/run.py#L56) present in run.py file according to their types.
For instance, if the parameter type is string, append the parameter to the list `string_val`

- While writing tests (which are meant to be run inside containers) for new components, make sure you register the test_name inside the main function present in [run.py](https://github.com/Divya063/TestingFramework/blob/c951f29802d90380a03b841c0f8752bcfe9cf737/run.py#L128) file
  . For instance, if test_name is "cernbox", add the following lines inside main function:
  
  ```python
   if test_name == "cernbox":
        docker_cp_to_container(container)
        docker_exec(container, test_name)
        docker_cp_from_container(container, ":/")
  ```
  In this way all the relevant files will be copied to the target container, and the test file will be executed.
  
  ### Output configuration
  ```yaml
  output:
  logfile:
    logging: True
  grafana:
    push : False
    hostname: ''
    port: '80'
    modules: ['Throughput']
    namespace: 'swan.testingframework'
  ```
  - By default stdout would be true and logs would be visible on the terminal.
  - Configuration can be changed in the yaml file.
  ## Logging
  **types of messages for logging** <br>
  ```
  "parameters": "[PARAMS] ",
  "info": "[INFO] ",
  "performance": "[PERF] ",
  "consistency": "[INTEGRITY] ",
  "warning": "[WARNING] ",
  "error": "[ERROR] ",
  ```
  For instance, if you want to log a message related to performance, you can use - self.log.write("performance", msg)
  
  ### Grafana
 
  Grafana is an open source metric analytics & visualization suite. To push metrics to grafana, make sure you add the name of class (whose metrics are needed) in the **modules** field(test.yaml).
  In the test file:
  - In case of successful execution use - self.stats[self.ref_test_name].set_success(), here is self.ref_test_name is test name defined in the constructor.
  - In case of failure use -self.stats[self.ref_test_name].set_error("error message")
  - If you want to store the metrics you can use - self.stats[self.ref_test_name].set_performance(value)
  - At last after collecting metrics call the check_test_class function - self.check_test_class(self)
  
  
