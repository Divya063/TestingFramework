

# How to add new tests?

- The structure which is should maintained while adding new tests is as follows:
```
 TestingFramework
 ├── tests
 │   ├── testfolder
 │       └── test_testname.py

 ```
- All the tests should be self contained amd executable, and each test should have main function.
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

Append the new parameters into the relevant list given in [check_input_validity function](https://github.com/Divya063/TestingFramework/blob/c951f29802d90380a03b841c0f8752bcfe9cf737/run.py#L56) according to their types.
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
  